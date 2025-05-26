from login_unificado import autenticar_usuario
import streamlit as st
import datetime
from firebase_admin import firestore


def render():
    db = firestore.client()

    # Verificação de login
    if "usuario" not in st.session_state or st.session_state["usuario"] is None:
        st.subheader("🔐 Login do Administrador")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            sucesso, retorno = autenticar_usuario(email, senha)
            if sucesso and retorno["tipo"] == "admin":
                st.session_state["usuario"] = retorno
                st.rerun()
        return

    # Botão de logout
    if st.button("Sair"):
        st.session_state["usuario"] = None
        st.rerun()

    st.markdown("## 🔍 Filtro de Solicitações")
    filtro_tipo = st.selectbox("Buscar por:", ["Todos", "CPF", "Nome", "Protocolo"])
    termo_busca = ""
    if filtro_tipo != "Todos":
        termo_busca = st.text_input(f"Digite o {filtro_tipo}:")

    docs = db.collection("solicitacoes").stream()
    solicitacoes = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        solicitacoes.append(data)

    if filtro_tipo != "Todos" and termo_busca:
        solicitacoes = [
            s for s in solicitacoes
            if termo_busca.lower() in str(s.get(filtro_tipo.lower(), "")).lower()
        ]

    solicitacoes.sort(key=lambda x: x.get("data_envio", ""), reverse=True)

    if not solicitacoes:
        st.info("Nenhuma solicitação encontrada.")
        return

    for s in solicitacoes:
        protocolo = s.get("protocolo", "---")
        status = s.get("status", "Pendente")
        cor_status = {"Pendente": "🟡", "Respondido": "🟢", "Resolvido": "⚪"}.get(status, "⚪")
        historico = s.get("historico", [])
        respostas = s.get("respostas", [])
        data_envio = s.get("data_envio", "")

        try:
            dt = datetime.datetime.fromisoformat(data_envio)
            data_part = dt.strftime('%d/%m/%Y')
            hora_part = dt.strftime('%H:%M')
        except:
            data_part, hora_part = "Data inválida", "Hora inválida"

        with st.expander(f"{cor_status} Protocolo: {protocolo} | Status: {status} | Data: {data_part}"):
            st.markdown(f"**👤 Nome:** {s.get('nome', '---')}")
            st.markdown(f"**📧 E-mail:** {s.get('email', '---')}")
            st.markdown(f"**🪪 CPF:** {s.get('cpf', '---')}")
            st.markdown(f"**📅 Data:** {data_part} | 🕒 Hora: {hora_part}")
            st.markdown(f"**🧾 Protocolo:** {protocolo}")

            st.subheader("📨 Texto da solicitação:")
            st.markdown(s.get("descricao", "_Sem descrição_"))

            st.subheader("📬 Histórico de respostas:")
            if not respostas:
                st.info("Nenhuma resposta ainda.")
            else:
                for r in respostas:
                    autor = r.get("autor", "Desconhecido")
                    texto = r.get("texto", "")
                    data_resp = r.get("data", "").replace("T", " ").split(".")[0]
                    st.markdown(f"**{autor}** em `{data_resp}`:")
                    st.markdown(f"> {texto}")

            st.subheader("📜 Histórico da Conversa:")
            for h in historico:
                autor = h.get("autor", "Desconhecido")
                texto = h.get("texto", "")
                data_msg = h.get("data", "").replace("T", " ").split(".")[0]
                st.markdown(f"**{autor}** em `{data_msg}`:")
                st.info(f"{texto}")

            if status != "Resolvido":
                st.subheader("➕ Enviar nova resposta")
                nova_resposta = st.text_area("Digite sua resposta:", key=f"resp_{s['id']}")

                if st.button("Enviar resposta", key=f"btn_{s['id']}"):
                    if nova_resposta.strip() == "":
                        st.warning("Digite uma resposta antes de enviar.")
                    else:
                        nova_entry = {
                            "autor": st.session_state["usuario"]["nome"],
                            "texto": nova_resposta.strip(),
                            "data": datetime.datetime.now().isoformat()
                        }
                        novas_respostas = respostas + [nova_entry]
                        historico.append(nova_entry)
                        db.collection("solicitacoes").document(s["id"]).update({
                            "respostas": novas_respostas,
                            "historico": historico,
                            "status": "Respondido"
                        })
                        st.success("Resposta enviada.")
                        st.rerun()

