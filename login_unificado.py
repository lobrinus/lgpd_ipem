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
