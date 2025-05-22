import streamlit as st
from login_unificado import registrar_usuario, autenticar_usuario


# Inicializa estados de sessão
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False,
        "usuario": None
    })

# --- Seção de Boas-Vindas ---
st.title("📘 Bem-vindo ao Sistema LGPD do IPEM-MG")
st.markdown("---")
st.markdown("""
**O Instituto de Pesos e Medidas de Minas Gerais está comprometido com a proteção de dados pessoais em conformidade com a Lei Geral de Proteção de Dados (LGPD).**

🔐 Para acessar todo o conteúdo do portal e realizar solicitações ou reclamações:

1. Faça seu cadastro no sistema
2. Efetue o login com suas credenciais
3. Acesse todas as funcionalidades do portal

*"Promovendo transparência e segurança no tratamento de dados pessoais desde 2020"*
""")

# --- Barra Lateral para Login/Registro ---
with st.sidebar:
    st.markdown("## 🔐 Acesso ao Sistema")
    
    if not st.session_state.logado:
        aba = st.radio("Escolha uma opção:", ["Entrar", "Registrar"], horizontal=True)
        
        # Formulário de Login
        if aba == "Entrar":
            with st.form("login_form"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                
                if st.form_submit_button("Entrar"):
                    sucesso, resultado = autenticar_usuario(email, senha)
                    if sucesso:
                        st.session_state.logado = True
                        st.session_state.usuario = resultado
                        st.rerun()  # Força atualização para redirecionar
                    else:
                        st.error(resultado)
        
        # Formulário de Registro
        elif aba == "Registrar":
            with st.form("registro_form"):
                email_r = st.text_input("Novo E-mail")
                senha_r = st.text_input("Senha", type="password")
                senha2_r = st.text_input("Confirmar Senha", type="password")
                
                if st.form_submit_button("Registrar"):
                    if senha_r != senha2_r:
                        st.error("As senhas não coincidem!")
                    else:
                        sucesso, msg = registrar_usuario(email_r, senha_r)
                        if sucesso:
                            st.success("Registro realizado! Faça login.")
                        else:
                            st.error(msg)
    
    else:
        st.success(f"Bem-vindo(a), {st.session_state.usuario['email']}!")
        if st.button("Sair"):
            st.session_state.logado = False
            st.session_state.usuario = None
            st.rerun()

# --- Redirecionamento após Login ---
if st.session_state.logado:
    st.switch_page("pages/1_🏠_Pagina_Principal.py")

# --- Rodapé ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Todos os direitos reservados.<br>
    R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
    CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7134 / 08000 335 335
</div>
""", unsafe_allow_html=True)
