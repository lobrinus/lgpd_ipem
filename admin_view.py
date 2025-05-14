import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.set_page_config(page_title="Administração LGPD - IPEM-MG", page_icon="🔐")

# Verificação de login
if "logado" not in st.session_state or not st.session_state["logado"]:
    st.warning("🔒 Área restrita. Faça login na página do formulário.")
    st.stop()

st.title("📁 Solicitações LGPD Recebidas")

def carregar_solicitacoes():
    docs = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING).stream()
    lista = []
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        lista.append(dados)
    return lista

dados = carregar_solicitacoes()
df = pd.DataFrame(dados)

nome_filtro = st.text_input("🔍 Filtrar por nome")
cpf_filtro = st.text_input("🔍 Filtrar por CPF")

if nome_filtro:
    df = df[df["nome"].str.contains(nome_filtro, case=False)]

if cpf_filtro:
    df = df[df["cpf"].str.contains(cpf_filtro)]

st.dataframe(df[["nome", "cpf", "email", "mensagem", "data_envio"]])
