import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore

# Verifica se o usuário está autenticado
if "cidadao_email" not in st.session_state or not st.session_state["cidadao_email"]:
    st.warning("🔒 Você precisa estar logado para acessar o formulário de solicitação.")
    st.stop()

# Inicializar Firebase (se ainda não iniciado)
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

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
    nome = st.text_input("Nome completo", placeholder="Digite seu nome completo")
    telefone = st.text_input("Telefone de contato", placeholder="(xx) xxxxx-xxxx")
    email = st.text_input("E-mail de contato", placeholder="seuemail@exemplo.com")
    cpf = st.text_input("CPF", placeholder="Apenas números")
    mensagem = st.text_area("Mensagem", placeholder="Descreva sua solicitação")

    enviado = st.form_submit_button("📩 Enviar Solicitação")

# Validação
if enviado:
    erros = []
    if not nome.strip():
        erros.append("⚠️ O campo **Nome** é obrigatório.")
    if not telefone.strip():
        erros.append("⚠️ O campo **Telefone** é obrigatório.")
    if not email.strip():
        erros.append("⚠️ O campo **E-mail** é obrigatório.")
    elif "@" not in email or "." not in email:
        erros.append("❌ E-mail inválido.")
    if not cpf.strip():
        erros.append("⚠️ O campo **CPF** é obrigatório.")
    elif not cpf.isdigit() or len(cpf) != 11:
        erros.append("❌ CPF inválido. Deve conter 11 dígitos numéricos.")
    if not mensagem.strip():
        erros.append("⚠️ O campo **Mensagem** é obrigatório.")

    if erros:
        for erro in erros:
            st.error(erro)
    else:
        # Salva solicitação no Firestore
        br_tz = pytz.timezone("America/Sao_Paulo")
        data_envio = datetime.now(br_tz)
        email_autenticado = st.session_state.get("cidadao_email", email)

        db.collection("solicitacoes").add({
            "nome": nome.strip(),
            "telefone": telefone.strip(),
            "email": email_autenticado.strip(),
            "cpf": cpf.strip(),
            "mensagem": mensagem.strip(),
            "data_envio": data_envio,
            "resposta": None,
            "data_resposta": None,
            "lido": False
        })
        st.success("✅ Solicitação enviada com sucesso!")

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
