import streamlit as st
from login import exibir_login
import os

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# ✅ Garante que o estado 'logado' exista
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Exibe o login
exibir_login()

# Páginas públicas e privadas
paginas_publicas = {
    "📨 Formulário LGPD": "12_📧_Formulario_LGPD (4)",
    "🏠 Início": "1_🏠_Página_Principal"
}

paginas_privadas = {
    "📁 Solicitações Recebidas": "13_📁_Solicitações_Recebidas"
}

# Junta as páginas disponíveis conforme login
paginas = paginas_publicas.copy()
if st.session_state["logado"]:
    paginas.update(paginas_privadas)

# Menu de navegação
pagina_escolhida = st.sidebar.selectbox("Selecione a página:", list(paginas.keys()))

# Executa a página selecionada com verificação
arquivo = paginas[pagina_escolhida] + ".py"
if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        exec(f.read(), globals())
else:
    st.error(f"❌ Arquivo '{arquivo}' não encontrado. Verifique se ele está no diretório correto.")
