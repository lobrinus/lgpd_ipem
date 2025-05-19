import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore

# Login visível, mas não obrigatório nesta página
from login import exibir_login
exibir_login()

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("📨 Solicitação de Acesso a Dados Pessoais")

with st.form("formulario_lgpd"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone de contato")
    email = st.text_input("E-mail de contato")
    cpf = st.text_input("CPF")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("📩 Enviar Solicitação")

if enviado:
    if nome and telefone and email and cpf and mensagem:
        br_tz = pytz.timezone("America/Sao_Paulo")
        data_envio = datetime.now(br_tz)

        # Pega e-mail do cidadão autenticado, se houver
        email_autenticado = st.session_state.get("cidadao_email", email)

        db.collection("solicitacoes").add({
            "nome": nome,
            "telefone": telefone,
            "email": email_autenticado,
            "cpf": cpf,
            "mensagem": mensagem,
            "data_envio": data_envio,
            "resposta": None,
            "data_resposta": None,
            "lido": False
        })
        st.success("✅ Solicitação enviada com sucesso!")
    else:
        st.warning("⚠️ Preencha todos os campos.")

# Mostrar resposta se houver
doc_ref = db.collection("solicitacoes").where("email", "==", email_autenticado).order_by("data_envio", direction=firestore.Query.DESCENDING).limit(1)
docs = doc_ref.stream()

for doc in docs:
    data = doc.to_dict()
    if data.get("resposta"):
        st.markdown("### 📬 Resposta do IPEM-MG")
        st.success(data.get("resposta"))
        data_resposta = data.get("data_resposta")
        if isinstance(data_resposta, datetime):
            data_resposta = data_resposta.astimezone(pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y às %H:%M')
            st.caption(f"Enviado em: {data_resposta}")
