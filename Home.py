import streamlit as st
from login import exibir_login
import os

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# ✅ Garante que o estado 'logado' exista
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Exibe o login ou identifica o usuário
with st.sidebar:
    st.markdown("## 🔐 Área Administrativa")
    if st.session_state.get("logado"):
        st.success("👤 Usuário administrador logado")
        if st.button("Sair"):
            st.session_state["logado"] = False
            st.experimental_rerun()
    else:
        user = st.text_input("Usuário", key="login_user", label_visibility="visible")
        password = st.text_input("Senha", type="password", key="login_pass", label_visibility="visible")
        login_button = st.button("Entrar", key="login_btn")

        if login_button:
            usuarios = st.secrets["auth"]
            if user in usuarios and usuarios[user] == password:
                st.session_state["logado"] = True
                st.success("✅ Login realizado com sucesso.")
                st.experimental_rerun()
            else:
                st.session_state["logado"] = False
                st.error("❌ Usuário ou senha inválidos.")

# Define as páginas públicas
paginas = {
    "🏠 Início": "1_🏠_Página_Principal.py",
    "🏠 Página Principal": "1_🏠_Página_Principal.py",
    "✅ Boas Práticas": "2_✅_Boas_Práticas.py",
    "📜 Política de Privacidade": "3_📜_Política_de_Privacidade.py",
    "🔍 Orientação de Dados Pessoais": "4_🔍_Orientação_de_Dados_Pessoais.py",
    "👥 Quem Lida com os Dados": "5_👥_Quem_Lida_com_os_Dados.py",
    "🛡️ Mitigação de Riscos": "6_🛡️_Mitigação_de_Riscos.py",
    "⚖️ Princípios Básicos": "7_⚖️_Princípios_Básicos.py",
    "✅❌ O Que Fazer e Não_Fazer": "8_✅❌_O_Que_Fazer_e_Não_Fazer.py",
    "🔄 Fluxo de Dados LGPD": "9_🔄_Fluxo_de_Dados_LGPD.py",
    "❓ FAQ": "10_❓_FAQ.py",
    "🔓 Solicitar Acesso Dados": "11_🔓_Solicitar_Acesso_Dados.py",
    "📨 Formulário LGPD": "12_📧_Formulario_LGPD.py"
}
# Se estiver logado, adiciona a página privada
if st.session_state["logado"]:
    paginas["📁 Solicitações Recebidas"] = "13_📁_Solicitações_Recebidas.py"

# Menu lateral (sem mostrar página privada para não logado)
pagina_escolhida = st.sidebar.radio("📄 Navegação", list(paginas.keys()))

# Executa a página escolhida
arquivo = paginas[pagina_escolhida]
if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        exec(f.read(), globals())
else:
    st.error(f"❌ Arquivo '{arquivo}' não encontrado. Verifique se ele está no diretório correto.")
