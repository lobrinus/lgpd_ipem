import streamlit as st

def exibir_login():
    # CSS fixo e compacto
    st.markdown("""
    <style>
        #custom-login {
            position: fixed;
            top: 0;
            left: 0;
            background-color: #f0f2f6;
            padding: 8px 12px;
            border-bottom-right-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            width: 220px;
            font-size: 12px;
        }
        #custom-login input, #custom-login button {
            font-size: 12px;
            width: 100%;
            margin: 4px 0;
            padding: 4px;
        }
    </style>
    <div id="custom-login">
        <form action="" method="post">
            <label>Usuário</label><br>
            <input type="text" name="usuario"><br>
            <label>Senha</label><br>
            <input type="password" name="senha"><br>
            <button type="submit">Entrar</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    # Recupera os valores usando parâmetros GET (não 100% seguro, mas funcional para painel simples)
    query_params = st.experimental_get_query_params()
    user_input = st.text_input("Usuário", key="login_user", label_visibility="collapsed")
    pass_input = st.text_input("Senha", type="password", key="login_pass", label_visibility="collapsed")

    if user_input and pass_input and not st.session_state.get("logado"):
        usuarios = st.secrets["auth"]
        if user_input in usuarios and usuarios[user_input] == pass_input:
            st.session_state["logado"] = True
            st.success("✅ Login realizado com sucesso.")
        else:
            st.session_state["logado"] = False
            st.error("❌ Usuário ou senha inválidos.")

    if st.session_state.get("logado"):
        st.markdown("<div style='position:fixed; top:4px; left:230px;'>🔐 Logado</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='position:fixed; top:4px; left:230px;'>🔓 Visitante</div>", unsafe_allow_html=True)
