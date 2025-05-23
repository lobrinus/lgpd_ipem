import streamlit as st
import datetime
from firebase_admin import firestore

def render():
    db = firestore.client()

    # Autenticação do Admin
    if "usuario" not in st.session_state or st.session_state["usuario"] is None:
        st.subheader("🔐 Login do Administrador")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            from login_unificado import autenticar_usuario
            sucesso, retorno = autenticar_usuario(email, senha)
            if sucesso and retorno["tipo"] == "admin":
                st.session_state["usuario"] = retorno
                st.rerun()
            elif sucesso:
                st.error("❌ Acesso restrito. Seu perfil não é de administrador.")
            else:
                st.error(retorno)
        st.stop()

    if st.session_state["usuario"].get("tipo") != "admin":
        st.error("🔒 Acesso negado. Apenas administradores podem acessar este painel.")
        st.stop()

    usuario = st.session_state["usuario"]
    st.title("📂 Painel de Solicitações - Admin")
    st.success(f"👤 Logado como: {usuario['email']}")

    if st.button("🚪 Logout"):
        st.session_state["usuario"] = None
        st.rerun()

    # Filtro
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

    # Exibir solicitações
    for s in solicitacoes:
        status = s.get("status", "Pendente")
        cor_status = {"Pendente": "🟡", "Respondido": "🟢", "Resolvido": "⚪"}.get(status, "⚪")

        data_envio = s.get("data_envio", "")
        try:
            data_part, hora_part = data_envio.split("T")
            hora_part = hora_part[:5]
        except:
            data_part, hora_part = "Data inválida", "Hora inválida"

        with st.expander(f"{cor_status} Protocolo: {s.get('protocolo', '---')} | Data: {data_part}"):
            st.markdown(f"**👤 Nome:** {s.get('nome', '')}")
            st.markdown(f"**📧 E-mail:** {s.get('email', '')}")
            st.markdown(f"**📅 Data:** {data_part} | 🕒 Hora: {hora_part}")
            st.markdown(f"**🪪 CPF:** {s.get('cpf', '')}")
            st.markdown(f"**🧾 Protocolo:** {s.get('protocolo', '')}")

            st.markdown("---")
            st.subheader("📨 Texto da solicitação:")
            st.markdown(s.get("descricao", "_Sem descrição_"))

            st.markdown("---")
            st.subheader("📬 Histórico de respostas:")

            respostas = s.get("respostas", [])
            if not respostas:
                st.info("Nenhuma resposta ainda.")
            else:
                for r in respostas:
                    autor = r.get("autor", "Desconhecido")
                    texto = r.get("texto", "")
                    data_resp = r.get("data", "").replace("T", " ").split(".")[0]
                    st.markdown(f"**{autor}** em `{data_resp}`:")
                    st.markdown(f"> {texto}")

            if status != "Resolvido":
                st.markdown("---")
                with st.form(f"resposta_{s['id']}"):
                    nova_resposta = st.text_area("✍️ Escreva sua resposta", height=150)
                    enviar = st.form_submit_button("📨 Enviar resposta")
                    if enviar and nova_resposta.strip():
                        nova_entry = {
                            "autor": "Admin",
                            "texto": nova_resposta.strip(),
                            "data": datetime.datetime.now().isoformat()
                        }
                        novas_respostas = respostas + [nova_entry]
                        db.collection("solicitacoes").document(s["id"]).update({
                            "respostas": novas_respostas,
                            "status": "Respondido"
                        })
                        st.success("Resposta enviada com sucesso.")
                        st.rerun()

                if st.button("✅ Marcar como Resolvido", key=f"resolver_{s['id']}"):
                    db.collection("solicitacoes").document(s["id"]).update({
                        "status": "Resolvido"
                    })
                    st.success("Solicitação marcada como resolvida.")
                    st.rerun()
            else:
                st.warning("🔒 Esta solicitação foi marcada como *Resolvida*. Não é possível responder.")
