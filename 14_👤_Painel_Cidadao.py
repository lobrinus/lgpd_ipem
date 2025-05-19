import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
# 🔐 Firebase Web Config (API Key)
if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_CREDENTIALS")  # pega a variável secreta do Streamlit Cloud
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Inicializa Pyrebase (Web)
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firestore.client()

# -------------------- Funções --------------------
def registrar_usuario(email, senha):
    try:
        auth.create_user_with_email_and_password(email, senha)
        return True, "✅ Registro realizado com sucesso."
    except Exception as e:
        return False, f"Erro no registro: {e}"

def autenticar_usuario(email, senha):
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        return True, user['email']
    except Exception:
        return False, "Erro no login: verifique o e-mail e senha."

# -------------------- Login/Registro --------------------
if "cidadao_email" not in st.session_state:
    st.session_state["cidadao_email"] = None

st.header("👤 Acesso do Cidadão")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔐 Login")
    email = st.text_input("E-mail", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    if st.button("Entrar"):
        sucesso, usuario = autenticar_usuario(email, senha)
        if sucesso:
            st.session_state["cidadao_email"] = usuario
            st.success("✅ Login realizado com sucesso.")
            st.rerun()
        else:
            st.error(usuario)

with col2:
    st.subheader("🆕 Registro")
    email_r = st.text_input("E-mail", key="reg_email")
    senha_r = st.text_input("Senha", type="password", key="reg_senha")
    senha2_r = st.text_input("Confirme a senha", type="password", key="reg_senha2")
    if st.button("Registrar"):
        if senha_r != senha2_r:
            st.error("❌ As senhas não coincidem.")
        else:
            sucesso, msg = registrar_usuario(email_r, senha_r)
            if sucesso:
                st.success(msg)
            else:
                st.error(msg)

# -------------------- Painel do Cidadão --------------------
if st.session_state["cidadao_email"]:
    st.sidebar.success(f"👤 Logado como: {st.session_state['cidadao_email']}")

    st.header("📬 Minhas Solicitações")

    solicitacoes_ref = db.collection("solicitacoes")
    query = solicitacoes_ref.where("email", "==", st.session_state["cidadao_email"])
    docs = query.stream()

    for doc in docs:
        data = doc.to_dict()
        with st.expander(f"📌 {data['mensagem']} ({data['data_envio']})"):
            if "resposta" in data:
                st.success("💬 Resposta do IPEM:")
                st.markdown(data["resposta"])
                st.caption(f"🕒 Respondido em: {data.get('data_resposta', 'Data não registrada')}")
            else:
                st.info("⏳ Ainda aguardando resposta do IPEM.")

    st.markdown("---")
    st.subheader("📨 Enviar Nova Solicitação")
    nova_msg = st.text_area("Digite sua solicitação")
    if st.button("Enviar Solicitação"):
        if nova_msg.strip():
            db.collection("solicitacoes").add({
                "email": st.session_state["cidadao_email"],
                "mensagem": nova_msg.strip(),
                "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "lido": False
            })
            st.success("✅ Solicitação enviada com sucesso!")
            st.rerun()
        else:
            st.warning("Por favor, digite a mensagem antes de enviar.")

    if st.button("Sair"):
        st.session_state["cidadao_email"] = None
        st.rerun()
