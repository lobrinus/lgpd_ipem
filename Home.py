import streamlit as st
from login_unificado import registrar_usuario, autenticar_usuario

# Configuração da página
st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# Inicializa estados de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Barra lateral - Login/Registro
with st.sidebar:
    st.markdown("## 🔐 Acesso")

    if st.session_state["usuario"] is None:
        aba = st.radio("Escolha uma opção:", ["Entrar", "Registrar"], horizontal=True, key="aba_login")

        if aba == "Entrar":
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                sucesso, resultado = autenticar_usuario(email, senha)
                if sucesso:
                    st.session_state["usuario"] = resultado
                    st.session_state["logado"] = True
                    st.session_state["tipo_usuario"] = resultado["tipo"]
                    st.session_state["email"] = resultado["email"]
                    if resultado["tipo"] == "admin":
                        st.session_state["admin_email"] = resultado["email"]
                    st.rerun()
                else:
                    st.error(resultado)
        elif aba == "Registrar":
            email_r = st.text_input("Novo E-mail")
            senha_r = st.text_input("Senha", type="password")
            senha2_r = st.text_input("Confirmar Senha", type="password")
            if st.button("Registrar"):
                if senha_r != senha2_r:
                    st.error("❌ As senhas não coincidem.")
                else:
                    sucesso, msg = registrar_usuario(email_r, senha_r)
                    if sucesso:
                        st.success(msg)
                        st.info("Agora você pode fazer login.")
                        st.session_state["aba_login"] = "Entrar"
                        st.rerun()
                    else:
                        st.error(msg)
    else:
        user = st.session_state.get("usuario", None)
        if isinstance(user, dict) and "email" in user and "tipo" in user:
            st.success(f"🔓 Logado como: {user['email']} ({user['tipo']})")
            if st.button("Sair"):
                for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                    st.session_state.pop(key, None)
                st.rerun()
        else:
            st.warning("⚠️ Sessão iniciada, mas os dados do usuário estão incompletos. Tente sair e entrar novamente.")
            if st.button("Forçar logout"):
                for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                    st.session_state.pop(key, None)
                st.rerun()

# --- INTEGRAÇÃO DA PÁGINA INICIAL ---
# Importa e executa o render() da sua página inicial
from pages._0_pagina_inicio import render  # O underline é necessário para importar arquivos iniciados por número

render()
