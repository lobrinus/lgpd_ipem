import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.set_page_config(page_title="Solicitação LGPD - IPEM-MG", page_icon="📨", layout="wide")

# FORMULÁRIO (acessível a todos)
st.title("📨 Formulário de Solicitação a Dados Pessoais - LGPD")

with st.form("formulario_lgpd"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone de contato")
    email = st.text_input("E-mail de contato")
    cpf = st.text_input("CPF")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("📩 Enviar Solicitação")

    if enviado:
        if nome and telefone and email and cpf and mensagem:
            db.collection("solicitacoes").add({
                "nome": nome,
                "telefone": telefone,
                "email": email,
                "cpf": cpf,
                "mensagem": mensagem,
                "data_envio": datetime.now()
            })
            st.success("✅ Solicitação enviada com sucesso!")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos.")

if st.session_state.get("logado"):
    st.markdown("---")
    st.subheader("📁 Solicitações Recebidas")

    docs = db.collection("solicitacoes").order_by("data_envio", direction=fs.Query.DESCENDING).stream()
    ...

