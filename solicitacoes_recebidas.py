import streamlit as st
import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    # === Inicialização do Firebase (executa apenas uma vez) ===
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.markdown("<h1 style='text-align: center;'>🔐 Painel LGPD</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # === Estado de sessão ===
    if "modo_auth" not in st.session_state:
        st.session_state["modo_auth"] = "login"  # Pode ser "login" ou "registro"
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # === AUTENTICAÇÃO ===
    if st.session_state["usuario"] is None:
        st.subheader("Acesse ou crie sua conta")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login"):
                st.session_state["modo_auth"] = "login"
        with col2:
            if st.button("📝 Registro"):
                st.session_state["modo_auth"] = "registro"
        st.markdown("---")

        if st.session_state["modo_auth"] == "login":
            with st.form("form_login"):
                st.subheader("🔑 Login")
                email = st.text_input("E-mail*")
                senha = st.text_input("Senha*", type="password")
                login_submit = st.form_submit_button("Entrar")

                if login_submit:
                    if not email or not senha:
                        st.warning("Por favor, preencha todos os campos.")
                    else:
                        sucesso, resultado = autenticar_usuario(email, senha)
                        if sucesso:
                            st.session_state["usuario"] = resultado
                            st.success("✅ Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao fazer login: {resultado}")

        elif st.session_state["modo_auth"] == "registro":
            with st.form("form_registro"):
                st.subheader("📝 Registro")
                nome = st.text_input("Nome completo*")
                telefone = st.text_input("Telefone*")
                email_reg = st.text_input("E-mail*")
                senha_reg = st.text_input("Senha*", type="password")
                senha_conf = st.text_input("Confirme a senha*", type="password")
                registro_submit = st.form_submit_button("Registrar")

                if registro_submit:
                    if not all([nome.strip(), telefone.strip(), email_reg.strip(), senha_reg.strip(), senha_conf.strip()]):
                        st.warning("Por favor, preencha todos os campos obrigatórios.")
                    elif senha_reg != senha_conf:
                        st.error("As senhas não coincidem.")
                    elif len(senha_reg) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        try:
                            sucesso, msg = registrar_usuario(
                                email=email_reg,
                                senha=senha_reg,
                                nome=nome,
                                telefone=telefone,
                                tipo="cidadao"
                            )
                            if sucesso:
                                st.success("✅ Registro concluído! Agora você pode fazer login.")
                                st.session_state["modo_auth"] = "login"
                                st.rerun()
                            else:
                                st.error(f"Erro no registro: {msg}")
                        except Exception as e:
                            st.error(f"Erro inesperado: {str(e)}")

        st.stop()

    # === Conteúdo após login ===
    usuario = st.session_state["usuario"]
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👤 Logado como: {usuario['email']} ({usuario['tipo']})")
    with col2:
        if st.button("🚪 Sair"):
            st.session_state["usuario"] = None
            st.session_state["modo_auth"] = "login"
            st.rerun()

    # === Painel de Administração ===
    if usuario.get("tipo") == "admin":
        st.header("🛠️ Painel de Administração")

        # Exibir campo de texto do cidadão
        st.subheader("📝 Campo de Texto do Cidadão")
        docs = db.collection("solicitacoes").stream()
        for doc in docs:
            data = doc.to_dict()
            st.markdown(f"**Protocolo:** {data.get('protocolo', '')}")
            st.text_area("Descrição da Solicitação", value=data.get("descricao", ""), height=100)
            st.markdown("---")

    else:
        st.warning("🚫 Acesso negado. Você não tem permissão de administrador.")
