import streamlit as st

def exibir_login():
    # Cria um container DEDICADO no topo da sidebar
    with st.sidebar:
        st.markdown("## 🔐 Área Administrativa")

        # Agrupa tudo no início
        user = st.text_input("Usuário", key="login_user", label_visibility="visible")
        password = st.text_input("Senha", type="password", key="login_pass", label_visibility="visible")
        login_button = st.button("Entrar", key="login_btn")

        # Lógica de login
        if login_button:
            usuarios = st.secrets["auth"]
            if user in usuarios and usuarios[user] == password:
                st.session_state["logado"] = True
                st.success("✅ Login realizado com sucesso.")
            else:
                st.session_state["logado"] = False
                st.error("❌ Usuário ou senha inválidos.")

        # Mensagem fixa
        if st.session_state.get("logado"):
            st.markdown("✅ **Acesso de administrador ativo**")
        else:
            st.markdown("ℹ️ **Acesso público**")
