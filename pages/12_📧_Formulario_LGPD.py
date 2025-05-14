import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

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

# BOTÃO DE LOGIN (acesso restrito)
with st.expander("🔐 Administrador"):
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar como administrador")

    if login_button:
        usuarios = st.secrets["auth"]
        if user in usuarios and usuarios[user] == password:
            
            st.session_state["logado"] = True
            st.success("✅ Login realizado com sucesso.")
        else:
            st.error("❌ Usuário ou senha inválidos.")
# ÁREA ADMINISTRATIVA - Exibe dados após login
if st.session_state.get("logado"):
    st.markdown("---")
    st.subheader("📁 Solicitações Recebidas")

    docs = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING).stream()
    dados = []
    for doc in docs:
        registro = doc.to_dict()
        registro["id"] = doc.id
        dados.append(registro)

    if dados:
        import pandas as pd
        df = pd.DataFrame(dados)
        nome_filtro = st.text_input("🔍 Filtrar por nome")
        cpf_filtro = st.text_input("🔍 Filtrar por CPF")

        if nome_filtro:
            df = df[df["nome"].str.contains(nome_filtro, case=False)]

        if cpf_filtro:
            df = df[df["cpf"].str.contains(cpf_filtro)]

        st.dataframe(df[["nome", "cpf", "email", "mensagem", "data_envio"]])
    else:
        st.info("Nenhuma solicitação registrada ainda.")
