import streamlit as st
import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    # Inicialização Firebase (uma única vez)
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Controla o estado de login na sessão
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # Se não estiver logado, exibe formulário de login
    if st.session_state["usuario"] is None:
        st.title("🔐 Login - Painel do Cidadão")
        with st.form("login_form"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                sucesso, resultado = autenticar_usuario(email, senha)
                if sucesso:
                    st.session_state["usuario"] = resultado
                    st.success(f"Logado como: {resultado['email']}")
                    st.rerun()
                else:
                    st.error(resultado)
        st.info("Por favor, faça login para acessar o painel.")
        return  # Encerra aqui se não estiver logado

    # Se estiver logado, mostra mensagem de usuário logado
    usuario = st.session_state["usuario"]
    if usuario.get("tipo") in ["cidadao", "admin"]:
        st.sidebar.success(f"👤 Logado como: {usuario['email']}")
        st.header("📬 Minhas Solicitações")
        # Aqui seu código de consulta ao firestore, etc.
        # (mantém seu código original de consulta e envio de solicitações)
        # ...
        # (não esqueça de colocar o restante do seu código de painel aqui)
        # Exemplo:
        solicitacoes_ref = firestore.client().collection("solicitacoes")
        query = solicitacoes_ref.where("email", "==", usuario["email"])
        docs = query.stream()
        tem_solicitacoes = False
        for doc in docs:
            tem_solicitacoes = True
            data = doc.to_dict()
            with st.expander(f"📌 {data['mensagem']} ({data['data_envio']})"):
                if "resposta" in data:
                    st.success("💬 Resposta do IPEM:")
                    st.markdown(data["resposta"])
                    st.caption(f"🕒 Respondido em: {data.get('data_resposta', 'Data não registrada')}")
                else:
                    st.info("⏳ Ainda aguardando resposta do IPEM.")
        if not tem_solicitacoes:
            st.info("Nenhuma solicitação encontrada.")
        # ... restante do seu código de painel ...
        # (copie seu código de consulta/envio de solicitação aqui)
    else:
        st.warning("⚠️ Você não tem permissão para acessar o painel cidadão.")

# Chamada padrão
if __name__ == "__main__":
    render()

