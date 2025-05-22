import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.subheader("🔐 Login LGPD")

    # Criar estado para controlar qual aba está ativa
    if "aba_login" not in st.session_state:
        st.session_state["aba_login"] = "login"  # valor inicial

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("Login"):
            st.session_state["aba_login"] = "login"
    with col2:
        if st.button("Registro"):
            st.session_state["aba_login"] = "registro"

    st.write("---")  # Linha divisória

    if st.session_state["aba_login"] == "login":
        email = st.text_input("Usuário (email)", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", key="btn_entrar"):
            sucesso, dados = autenticar_usuario(email, senha)
            if sucesso:
                st.session_state["logado"] = True
                st.session_state["email"] = dados["email"]
                st.session_state["tipo_usuario"] = dados["tipo"]
                if dados["tipo"] == "admin":
                    st.session_state["admin_email"] = dados["email"]
                st.success(f"✅ Bem-vindo, {dados['tipo']}")
                st.experimental_rerun()
            else:
                st.error(dados)

    else:  # Registro
        nome = st.text_input("Nome Completo", key="reg_nome")
        email = st.text_input("Email", key="reg_email")
        telefone = st.text_input("Telefone", key="reg_telefone")
        senha = st.text_input("Senha", type="password", key="reg_senha")
        senha2 = st.text_input("Confirme a senha", type="password", key="reg_senha2")

        if st.button("Registrar", key="btn_registrar"):
            if senha != senha2:
                st.error("❌ As senhas não coincidem.")
            else:
                sucesso, msg = registrar_usuario(email, senha, nome, telefone)
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)
