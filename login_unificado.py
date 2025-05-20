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

email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    sucesso, dados = autenticar_usuario(email, senha)

    if sucesso:
        st.session_state["logado"] = True
        st.session_state["email"] = dados["email"]
        st.session_state["tipo_usuario"] = dados["tipo"] 
        
        if dados["tipo"] == "admin":
            st.session_state["admin_email"] = dados["email"]

        st.success(f"✅ Bem-vindo, {dados['tipo']}")
        st.rerun()
    else:
        st.error(dados)


def registrar_usuario(email, senha):
    email = email.lower()  # Normaliza para letras minúsculas
    try:
        auth.create_user_with_email_and_password(email, senha)
        db.collection("usuarios").document(email).set({
            "email": email,
            "tipo": "cidadao"  # padrão ao registrar
        })
        return True, "✅ Registro realizado com sucesso."
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        return False, f"Erro no registro: {error_str}"

def autenticar_usuario(email, senha):
    email = email.lower()  # Normaliza para letras minúsculas
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

