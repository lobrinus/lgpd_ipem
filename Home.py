import streamlit as st
from login_unificado import registrar_usuario, autenticar_usuario

# Configuração da página
st.set_page_config(
    page_title="LGPD - IPEM-MG",
    page_icon="🏠",
    layout="wide"
)

# Estado da sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# Barra lateral - Login/Registro
with st.sidebar:
    st.markdown("## 🔐 Acesso")
    
    if not st.session_state.logado:
        aba = st.radio("Escolha:", ["Entrar", "Registrar"], horizontal=True)
        
        if aba == "Entrar":
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                sucesso, resultado = autenticar_usuario(email, senha)
                if sucesso:
                    st.session_state.logado = True
                    st.session_state.usuario = resultado
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
        st.success(f"🔓 Logado como: {st.session_state.usuario['email']}")
        if st.button("Sair"):
            st.session_state.logado = False
            st.session_state.usuario = None
            st.rerun()

# Conteúdo da Página Principal
if st.session_state.logado:
    from pages.pagina_principal import render
    render()
else:
    st.title("📘 Sistema LGPD - IPEM-MG")
    st.markdown("""
    Bem-vindo ao sistema de apoio à adequação à Lei Geral de Proteção de Dados (LGPD) do IPEM-MG.
    Faça login para acessar o sistema.
    """)
