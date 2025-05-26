import streamlit as st
import datetime
from firebase_admin import firestore

def render():
    db = firestore.client()

    if "usuario" not in st.session_state or st.session_state["usuario"] is None:
        from login_unificado import autenticar_usuario
        st.subheader("🔐 Login do Administrador")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            sucesso, retorno = autenticar_usuario(email, senha)
            if sucesso and retorno["tipo"] == "admin":
                st.session_state["usuario"] = retorno
                st.rerun()
            elif sucesso:
                st.error("❌ Acesso restrito.")
            else:
                st.error(retorno)
        st.stop()

    if st.session_state["usuario"].get("tipo") != "admin":
        st.error("🔒 Acesso negado. Apenas administradores.")
        st.stop()

    usuario = st.session_state["usuario"]
    st.title("📂 Painel de Solicitações")
    st.success(f"👤 Logado como: {usuario['email']}")

    if st.button("🚪 Logout"):
        st.session_state["usuario"] = None
        st.rerun()

    docs = db.collection("solicitacoes").stream()
    solicitacoes = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        solicitacoes.append(data)

    solicitacoes.sort(key=lambda x: x.get("data_envio", ""), reverse=True)

    if not solicitacoes:
        st.info("Nenhuma solicitação encontrada.")
        return

    for s in solicitacoes:
        protocolo = s.get("protocolo", "---")
        status = s.get("status", "Pendente")
        historico = s.get("historico", [])
        data_envio = s.get("data_envio", "Data inválida")

        with st.expander(f"📄 Protocolo: {protocolo} | Status: {status}"):
            st.markdown(f"**👤 Nome:** {s.get('nome', '---')}")
            st.markdown(f"**📧 E-mail:** {s.get('email', '---')}")
            st.markdown(f"**🪪 CPF:** {s.get('cpf', '---')}")
            st.markdown(f"**📅 Data:** {data_envio}")

            st.subheader("📜 Histórico da Conversa:")
            for h in historico:
                autor = h.get("autor", "Desconhecido")
                texto = h.get("texto", "")
                data_msg = h.get("data", "").replace("T", " ").split(".")[0]
                st.markdown(f"**{autor}** em `{data_msg}`:")
                st.info(f"{texto}")

            if status != "Resolvido":
                with st.form(f"resposta_{s['id']}"):
                    nova_resposta = st.text_area("✍️ Escreva sua resposta", height=150)
                    enviar = st.form_submit_button("📨 Enviar resposta")
                    if enviar and nova_resposta.strip():
                        nova_entry = {
                            "autor": "Admin",
                            "texto": nova_resposta.strip(),
                            "data": datetime.datetime.now().isoformat()
                        }
                        historico.append(nova_entry)
                        db.collection("solicitacoes").document(s["id"]).update({
                            "historico": historico,
                            "status": "Respondido"
                        })
                        st.success("Resposta enviada.")
                        st.rerun()

                if st.button("✅ Marcar como Resolvido", key=f"resolver_{s['id']}"):
                    db.collection("solicitacoes").document(s["id"]).update({
                        "status": "Resolvido"
                    })
                    st.success("Marcada como resolvida.")
                    st.rerun()
            else:
                st.warning("🔒 Solicitação resolvida.")
