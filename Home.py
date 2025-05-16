import streamlit as st
from login import exibir_login
import os

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# ✅ Garante que o estado 'logado' exista
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Exibe o login
exibir_login()

# Executa diretamente a página conforme login
if st.session_state["logado"]:
    # Usuário logado visualiza solicitações recebidas
    arquivo = "13_📁_Solicitações_Recebidas.py"
else:
    # Usuário não logado visualiza o formulário
    arquivo = "12_📧_Formulario_LGPD.py"

# Executa a página correspondente com verificação
if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        exec(f.read(), globals())
else:
    st.error(f"❌ Arquivo '{arquivo}' não encontrado. Verifique se ele está no diretório correto.")
