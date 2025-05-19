import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# 🔧 Firebase Configuração Web
firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "XXXXXXXXXXXX",
    "appId": "1:XXXXXXXXXXXX:web:XXXXXXXXXXXX",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_CREDENTIALS")
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def registrar_usuario(email, senha):
    try:
        auth.create_user_with_email_and_password(email, senha)
        db.collection("usuarios").document(email).set({
            "email": email,
            "tipo": "cidadao"
        })
        return True, "✅ Registro realizado com sucesso."
    except Exception as e:
        return False, f"Erro no registro: {e}"

def autenticar_usuario(email, senha):
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        doc = db.collection("usuarios").document(email).get()
        if doc.exists:
            tipo = doc.to_dict().get("tipo", "cidadao")
        else:
            tipo = "cidadao"
        return True, {"email": email, "tipo": tipo}
    except:
        return False, "❌ E-mail ou senha incorretos."

# ---------------------- Interface ----------------------
st.set_page_config("Login LGPD - IPEM-MG", layout="centered")
st.title("🔐 Acesso ao Portal LGPD")

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

if st.session_state["usuario"] is None:
    aba = st.tabs(["Login", "Registrar"])
    
    with aba[0]:
        st.subheader("🔑 Entrar")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            ok, resultado = autenticar_usuario(email, senha)
            if ok:
                st.session_state["usuario"] = resultado
                st.success("✅ Login realizado com sucesso.")
                st.rerun()
            else:
                st.error(resultado)
    
    with aba[1]:
        st.subheader("📝 Criar Conta (Cidadão)")
        email_r = st.text_input("E-mail", key="email_reg")
        senha_r = st.text_input("Senha", type="password", key="senha_reg")
        senha2_r = st.text_input("Confirmar Senha", type="password", key="senha2_reg")
        if st.button("Registrar"):
            if senha_r != senha2_r:
                st.error("❌ As senhas não coincidem.")
            else:
                sucesso, msg = registrar_usuario(email_r, senha_r)
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)
else:
    usuario = st.session_state["usuario"]
    st.sidebar.success(f"🔓 Logado como: {usuario['email']} ({usuario['tipo']})")
    
    if st.button("Sair"):
        st.session_state["usuario"] = None
        st.rerun()

    if usuario["tipo"] == "admin":
        st.markdown("### 🛡️ Área Administrativa")
        st.info("Acesse a aba '📁 Solicitações Recebidas' no menu lateral.")
    else:
        st.markdown("### 👤 Painel do Cidadão")
        st.info("Você pode acessar o formulário LGPD e acompanhar suas solicitações na aba 'Painel do Cidadão'.")
