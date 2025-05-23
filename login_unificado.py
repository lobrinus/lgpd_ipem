# login_unificado.py
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Config Firebase
firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "510388427771",
    "appId": "1:51038842771:web:fdcda6526f125892db8266",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    if "FIREBASE_CREDENTIALS" not in st.secrets:
        st.error("❌ As credenciais do Firebase não foram encontradas nos secrets.")
        st.stop()

    try:
        cred = credentials.Certificate(dict(st.secrets["FIREBASE_CREDENTIALS"]))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"❌ Erro ao inicializar o Firebase Admin: {e}")
        st.stop()

db = firestore.client()

def autenticar_usuario(email, senha):
    email = email.lower()
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        doc = db.collection("usuarios").document(email).get()
        tipo = doc.to_dict().get("tipo", "cidadao") if doc.exists else "cidadao"
        return True, {"email": email, "tipo": tipo}
    except:
        return False, "❌ E-mail ou senha incorretos."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    email = email.lower()
    try:
        auth.create_user_with_email_and_password(email, senha)
        db.collection("usuarios").document(email).set({
            "email": email,
            "nome": nome,
            "telefone": telefone,
            "cpf": cpf,
            "tipo": tipo
        })
        return True, "✅ Registro realizado com sucesso."
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        return False, f"Erro no registro: {error_str}"
