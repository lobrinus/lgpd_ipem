import streamlit as st
from login import exibir_login
import os

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# ✅ Garante que o estado 'logado' exista
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Exibe o login
exibir_login()

# Define as páginas públicas
paginas = {
    "🏠 Início": "1_🏠_Página_Principal.py",
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
