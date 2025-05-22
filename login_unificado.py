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

try:
    cred_dict = st.secrets["FIREBASE_CREDENTIALS"]
except KeyError:
    st.error("❌ Credenciais do Firebase não configuradas nos secrets do Streamlit Cloud.")
    st.error("Verifique se você adicionou a seção [FIREBASE_CREDENTIALS] nos secrets.")
    st.stop()

def autenticar_usuario(email, senha):
    email = email.lower()
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        doc = db.collection("usuarios").document(email).get()
        tipo = doc.to_dict().get("tipo", "cidadao") if doc.exists else "cidadao"
        return True, {"email": email, "tipo": tipo}
    except:
        return False, "❌ E-mail ou senha incorretos."


def registrar_usuario(email, senha, nome, telefone, tipo="cidadao"):
    email = email.lower()
    try:
        # Cria usuário no Firebase Auth
        auth.create_user_with_email_and_password(email, senha)

        # Salva dados no Firestore
        db.collection("usuarios").document(email).set({
            "email": email,
            "nome": nome,
            "telefone": telefone,
            "tipo": tipo
        })

        return True, "✅ Registro realizado com sucesso."
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        return False, f"Erro no registro: {error_str}"



# 🔹 Função principal da interface de login
def render():
    st.subheader("🔐 Login LGPD")
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
