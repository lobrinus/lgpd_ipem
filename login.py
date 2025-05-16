import streamlit as st

def exibir_login():
    # Estilo fixo no canto superior esquerdo
    st.markdown("""
    <style>
        #login-container {
            position: fixed;
            top: 10px;
            left: 10px;
            background-color: #f0f2f6;
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            z-index: 9999;
            width: 250px;
        }
        #login-container input, #login-container button {
            width: 100%;
            margin-top: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Renderiza os inputs como blocos invisíveis com CSS no topo
    with st.container():
        st.markdown('<div id="login-container">', unsafe_allow_html=True)

        user = st.text_input("Usuário", key="login_user_top", label_visibility="visible")
        password = st.text_input("Senha", type="password", key="login_pass_top", label_visibility="visible")
        login_button = st.button("Entrar", key="login_btn_top")

        if login_button:
            usuarios = st.secrets["auth"]
            if user in usuarios and usuarios[user] == password:
                st.session_state["logado"] = True
                st.success("✅ Login realizado com sucesso.")
            else:
                st.session_state["logado"] = False
                st.error("❌ Usuário ou senha inválidos.")

        if st.session_state.get("logado"):
            st.markdown("✅ <strong>Admin logado</strong>", unsafe_allow_html=True)
        else:
            st.markdown("🔓 Visitante", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
