import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import pytz
import datetime
import json

# --- Variáveis globais ---
auth = None
storage = None
db = None
firebase_pyrebase_app = None

# --- Leitura dos Segredos Firebase ---
try:
    firebaseConfig = st.secrets["firebase"]  # Para Pyrebase
except Exception as e:
    st.error(f"❌ Erro ao carregar [firebase] do Secrets: {e}")
    st.stop()

try:
    cred_value = st.secrets["FIREBASE_CREDENTIALS"]
except Exception as e:
    st.error(f"❌ Erro ao carregar FIREBASE_CREDENTIALS do Secrets: {e}")
    st.stop()

# --- Inicialização Pyrebase (Auth e Storage) ---
try:
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()
except Exception as e_pyre:
    st.error(f"❌ Erro na inicialização do Pyrebase (Auth/Storage): {e_pyre}")
    st.stop()

# --- Inicialização Firebase Admin SDK (Firestore) ---
try:
    if not firebase_admin._apps:
        # Trata diferentes formatos de entrada do secrets
        if isinstance(cred_value, str):
            cred_dict = json.loads(cred_value)
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
        else:
            cred_dict = dict(cred_value)

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

except Exception as e_admin:
    st.error(f"❌ Erro na inicialização do Firebase Admin SDK (Firestore): {e_admin}")
    st.stop()

# --- Timezone Brasil ---
timezone_brasilia = pytz.timezone('America/Sao_Paulo')

# =====================================================================
# === Funções de Autenticação e Usuário ==============================
# =====================================================================

def autenticar_usuario(email, senha):
    if not auth or not db:
        return False, "⚠️ Serviços Firebase não disponíveis."

    try:
        user_auth_info = auth.sign_in_with_email_and_password(email.lower(), senha)
        doc_ref = db.collection("usuarios").document(email.lower())
        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            return True, {
                "email": email.lower(),
                "tipo": user_data.get("tipo", "cidadao"),
                "nome": user_data.get("nome", ""),
                "idToken": user_auth_info.get('idToken')
            }
        else:
            return False, "⚠️ Usuário autenticado, mas sem dados no Firestore."
    except Exception as e:
        error_str = str(e).upper()
        if any(code in error_str for code in ["INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND", "USER_NOT_FOUND"]):
            return False, "❌ E-mail ou senha incorretos."
        return False, f"❌ Erro inesperado no login: {e}"

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    if not auth or not db:
        return False, "⚠️ Serviços Firebase não disponíveis para registro."

    try:
        auth.create_user_with_email_and_password(email.lower(), senha)
        db.collection("usuarios").document(email.lower()).set({
            "email": email.lower(),
            "nome": nome,
            "telefone": telefone,
            "cpf": cpf,
            "tipo": tipo,
            "data_registro": firestore.SERVER_TIMESTAMP
        })
        return True, "✅ Registro realizado com sucesso! Faça o login."
    except Exception as e:
        error_str = str(e).upper()
        if "EMAIL_EXISTS" in error_str or "EMAIL_ALREADY_IN_USE" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        if "WEAK_PASSWORD" in error_str or "PASSWORD_SHOULD_BE_AT_LEAST_6_CHARACTERS" in error_str:
            return False, "❌ A senha deve ter pelo menos 6 caracteres."
        return False, f"❌ Erro no registro: {e}"

# =====================================================================
# === Funções de Storage (Upload de Arquivos) ========================
# =====================================================================

def upload_file_to_storage(file_object, destination_path_in_storage):
    if not storage:
        st.error("⚠️ Serviço de armazenamento (Storage) não disponível.")
        return None
    if file_object is None:
        return None

    try:
        file_object.seek(0)
        storage.child(destination_path_in_storage).put(file_object)
        url = storage.child(destination_path_in_storage).get_url(token=None)
        return url
    except Exception as e:
        st.error(f"❌ Erro no upload do arquivo '{file_object.name}': {e}")
        return None

# =====================================================================
# === Geração de Protocolo Único ======================================
# =====================================================================

def gerar_protocolo_unico():
    return f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S%f')[:-3]}"

# =====================================================================
# === Debug (Opcional) ===============================================
# =====================================================================

# Ative para verificar se os serviços estão funcionando
    if __name__ == "__main__":
        st.title("🚀 Verificação Firebase")
        if auth:
            st.success("✅ Auth (Pyrebase) funcionando.")
        else:
            st.error("❌ Auth NÃO está funcionando.")
    
        if storage:
            st.success("✅ Storage (Pyrebase) funcionando.")
        else:
            st.error("❌ Storage NÃO está funcionando.")
    
        if db:
            st.success("✅ Firestore (Admin SDK) funcionando.")
        else:
            st.error("❌ Firestore NÃO está funcionando.")
