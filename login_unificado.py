import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pytz
import datetime

# --- Configuração e Inicialização do Firebase ---
auth = None
storage = None
db = None
firebase_pyrebase_app = None

# Configuração do Firebase Web SDK (Pyrebase) diretamente no código
# Estes são os valores que você forneceu no seu arquivo login_unificado (6).py
firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "510388427771",
    "appId": "1:510388427771:web:fdcda6526f125892db8266",
    "databaseURL": ""
}

try:
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()
except Exception as e:
    # Este st.error aparecerá na interface se a inicialização do Pyrebase falhar
    st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha ao inicializar Pyrebase (Auth/Storage) com firebaseConfig: {e}")
    # auth e storage permanecem None

# Inicializa o Firebase Admin SDK (para Firestore) - APENAS UMA VEZ
if not firebase_admin._apps:
    try:
        # Esta parte DEPENDE da configuração correta de [FIREBASE_CREDENTIALS]
        # nos seus "Secrets" do Streamlit Cloud, conforme sua captura de tela.
        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        if isinstance(cred_value, str):
            import json
            cred_dict = json.loads(cred_value)
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
        else:
            raise ValueError("O segredo 'FIREBASE_CREDENTIALS' não é um dicionário nem uma string JSON válida.")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except KeyError as e:
        # Este st.error aparecerá se 'FIREBASE_CREDENTIALS' não for encontrado nos segredos
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Chave 'FIREBASE_CREDENTIALS' não encontrada nos segredos: {e}. Verifique suas configurações de segredos no Streamlit Cloud.")
        # db permanece None
    except Exception as e:
        # Este st.error aparecerá para outros erros na inicialização do Admin SDK
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha ao inicializar Firebase Admin SDK (Firestore): {e}")
        # db permanece None
else:
    db = firestore.client()

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

def autenticar_usuario(email, senha):
    if not auth:
        return False, "❌ Serviço de autenticação indisponível (auth não inicializado)."
    if not db: # Adicionado para consistência, embora o erro principal seja no auth
        return False, "❌ Serviço de banco de dados indisponível (db não inicializado)."

    email_lower = email.lower()
    try:
        user_auth_info = auth.sign_in_with_email_and_password(email_lower, senha)
        doc_ref = db.collection("usuarios").document(email_lower)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            return True, {
                "email": email_lower,
                "tipo": user_data.get("tipo", "cidadao"),
                "nome": user_data.get("nome", ""),
                "idToken": user_auth_info.get('idToken')
            }
        else:
            return False, "❌ Usuário autenticado, mas informações de perfil não encontradas."
    except Exception as e:
        error_message = str(e).upper()
        if any(code in error_message for code in ["INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND", "USER_NOT_FOUND", "INVALID_EMAIL"]):
            return False, "❌ E-mail ou senha incorretos."
        return False, "❌ Erro durante a tentativa de login. Verifique suas credenciais ou tente mais tarde."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    if not auth:
        return False, "❌ Serviço de autenticação indisponível para registro (auth não inicializado)."
    if not db:
        return False, "❌ Serviço de banco de dados indisponível para registro (db não inicializado)."

    email_lower = email.lower()
    try:
        auth.create_user_with_email_and_password(email_lower, senha)
        db.collection("usuarios").document(email_lower).set({
            "email": email_lower,
            "nome": nome,
            "telefone": telefone,
            "cpf": cpf,
            "tipo": tipo,
            "data_registro": firestore.SERVER_TIMESTAMP
        })
        return True, "✅ Registro realizado com sucesso! Agora você pode fazer o login."
    except Exception as e:
        error_str = str(e).upper()
        if "EMAIL_EXISTS" in error_str or "EMAIL_ALREADY_IN_USE" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        elif "WEAK_PASSWORD" in error_str or "PASSWORD_SHOULD_BE_AT_LEAST_6_CHARACTERS" in error_str:
            return False, "❌ A senha é muito fraca. Deve ter pelo menos 6 caracteres."
        return False, f"❌ Erro no registro. Tente novamente ou verifique os dados informados."

def upload_file_to_storage(file_object, destination_path_in_storage):
    if not storage:
        st.error("⚠️ Serviço de armazenamento de arquivos (Storage) não está disponível (storage não inicializado).")
        return None
    if file_object is None:
        return None
    try:
        file_object.seek(0)
        storage.child(destination_path_in_storage).put(file_object)
        url = storage.child(destination_path_in_storage).get_url(token=None)
        return url
    except Exception as e:
        st.error(f"⚠️ Erro no upload do arquivo '{file_object.name}': {e}")
        return None

def gerar_protocolo_unico():
    return f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S%f')[:-3]}"
