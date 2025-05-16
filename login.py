import streamlit as st

def exibir_login():
    st.markdown("""
    <style>
        #login-container {
            position: fixed;
            top: 0;
            left: 0;
            background-color: #f0f2f6;
            padding: 8px 10px;
            border-bottom-right-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05);
            z-index: 10000;
            width: 110px;
            font-size: 12px;
        }
        #login-container label {
            font-size: 11px;
        }
        #login-container input {
            font-size: 12px !important;
            height: 28px !important;
            padding: 2px 6px !important;
        }
        #login-container button {
            font-size: 12px !important;
            padding: 4px 0 !important;
            margin-top: 4px;
        }
        #login-container div.stAlert {
            margin-top: 4px;
            font-size: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

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

