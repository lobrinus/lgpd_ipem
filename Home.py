import streamlit as st
from login_unificado import registrar_usuario, autenticar_usuario

# Configuração inicial
st.set_page_config(
    page_title="LGPD - IPEM-MG",
    page_icon="🏠",
    layout="wide"
)

# Estado de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Função de login/registro
def exibir_login():
    with st.sidebar:
        st.markdown("## 🔐 Acesso")
        if not st.session_state["usuario"]:
            aba = st.radio("Escolha:", ["Entrar", "Registrar"], horizontal=True, key="aba_login")
            if aba == "Entrar":
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                if st.button("Entrar"):
                    sucesso, resultado = autenticar_usuario(email, senha)
                    if sucesso:
                        st.session_state.update({
                            "logado": True,
                            "usuario": resultado
                        })
                        st.rerun()
            elif aba == "Registrar":
                email_r = st.text_input("Novo E-mail")
                senha_r = st.text_input("Senha", type="password")
                senha2_r = st.text_input("Confirmar Senha", type="password")
                if st.button("Registrar") and senha_r == senha2_r:
                    sucesso, msg = registrar_usuario(email_r, senha_r)
                    if sucesso:
                        st.success("Registro realizado! Faça login.")
        else:
            user = st.session_state["usuario"]
            if isinstance(user, dict):
                st.success(f"🔓 Logado como: {user['email']}")
                if st.button("Sair"):
                    for k in ["usuario", "logado"]:
                        st.session_state[k] = None
                    st.rerun()

# Exibir login
exibir_login()

# Conteúdo principal após login
if st.session_state.get("logado"):
    # Importa e chama a render() da sua página principal
    from pages.pagina_principal import render
    from pages.painel_cidadao import render
    render()
else:
    # Página de boas-vindas
    st.title("📘 Sistema LGPD - IPEM-MG")
    st.markdown("""
    Bem-vindo ao sistema de apoio à adequação à Lei Geral de Proteção de Dados (LGPD) do IPEM-MG.
    Faça login na barra lateral para acessar o conteúdo completo.
    """)
