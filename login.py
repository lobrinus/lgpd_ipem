import streamlit as st

def exibir_login():
    with st.sidebar:
        st.markdown("## 🔐 Área Administrativa")
        user = st.text_input("Usuário", key="login_user")
        password = st.text_input("Senha", type="password", key="login_pass")
        login_button = st.button("Entrar", key="login_btn")

        if login_button:
            usuarios = st.secrets["auth"]
            if user in usuarios and usuarios[user] == password:
                st.session_state["logado"] = True
                st.success("✅ Login realizado com sucesso.")
            else:
                st.session_state["logado"] = False
                st.error("❌ Usuário ou senha inválidos.")

        if st.session_state.get("logado"):
            st.sidebar.success("✅ Logado")
        else:
            st.sidebar.info("ℹ️ Visitante")
