import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pytz
import datetime

# --- Inicialização das variáveis de serviço ---
auth = None
storage = None
db = None
firebase_pyrebase_app = None

# --- Configuração e Inicialização do Pyrebase (Auth e Storage) ---
# Usando as configurações diretamente no código, conforme seu arquivo login_unificado (6).py
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
    # print("DEBUG: Tentando inicializar Pyrebase com firebaseConfig...") # Para logs no Streamlit Cloud
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()
    if not auth:
        # Esta mensagem aparecerá na interface se 'auth' não for criado.
        st.error("⚠️ Erro Crítico em login_unificado.py: Pyrebase 'auth' não foi inicializado após initialize_app. Verifique as chaves em firebaseConfig ou a conectividade com o Firebase.")
    if not storage:
        st.error("⚠️ Erro Crítico em login_unificado.py: Pyrebase 'storage' não foi inicializado após initialize_app. Verifique as chaves em firebaseConfig ou a conectividade com o Firebase.")
    # print(f"DEBUG: Pyrebase auth: {'Inicializado' if auth else 'FALHOU'}")
    # print(f"DEBUG: Pyrebase storage: {'Inicializado' if storage else 'FALHOU'}")

except Exception as e_pyrebase:
    st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha ao inicializar Pyrebase (Auth/Storage). Exceção: {e_pyrebase}")
    # auth e storage permanecem None

# --- Configuração e Inicialização do Firebase Admin SDK (Firestore) ---
if not firebase_admin._apps:
    try:
        # print("DEBUG: Tentando inicializar Firebase Admin SDK...")
        # Esta parte DEPENDE da configuração correta de [FIREBASE_CREDENTIALS]
        # nos seus "Secrets" do Streamlit Cloud.
        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        if isinstance(cred_value, str):
            import json
            cred_dict = json.loads(cred_value)
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
        else:
            raise ValueError("O segredo 'FIREBASE_CREDENTIALS' nos seus 'Secrets' do Streamlit Cloud não é um dicionário nem uma string JSON válida.")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        if not db:
            st.error("⚠️ Erro Crítico em login_unificado.py: Firebase Admin SDK 'db' (Firestore) não foi inicializado após initialize_app. Verifique as credenciais em [FIREBASE_CREDENTIALS] nos seus segredos.")
        # print(f"DEBUG: Firebase Admin SDK db: {'Inicializado' if db else 'FALHOU'}")

    except KeyError as e_key_admin:
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Chave 'FIREBASE_CREDENTIALS' não encontrada nos seus 'Secrets' do Streamlit Cloud: {e_key_admin}. Verifique o nome e a existência da seção.")
        # db permanece None
    except ValueError as e_value_admin:
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Formato inválido para 'FIREBASE_CREDENTIALS' nos seus 'Secrets' do Streamlit Cloud: {e_value_admin}")
        # db permanece None
    except Exception as e_admin:
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha geral ao inicializar Firebase Admin SDK (Firestore). Exceção: {e_admin}")
        # db permanece None
else:
    db = firestore.client()
    # print(f"DEBUG: Firebase Admin SDK db (já inicializado): {'Disponível' if db else 'FALHOU'}")

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

def autenticar_usuario(email, senha):
    if not auth:
        return False, "❌ Serviço de autenticação Pyrebase (auth) não está disponível."
    if not db: # Verifica se o Firestore foi inicializado
        return False, "❌ Serviço de banco de dados Firestore (db) não está disponível."

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
                "nome": user_data.get("nome", ""), # Retorna o nome do usuário
                "idToken": user_auth_info.get('idToken')
            }
        else:
            return False, "❌ Usuário autenticado, mas informações de perfil não encontradas no banco de dados."
    except Exception as e:
        error_message = str(e).upper()
        if any(code in error_message for code in ["INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND", "USER_NOT_FOUND", "INVALID_EMAIL"]):
            return False, "❌ E-mail ou senha incorretos."
        # Para depuração, veja os logs do Streamlit Cloud: print(f"DEBUG Auth Error: {e}")
        return False, "❌ Erro durante a tentativa de login. Verifique suas credenciais ou tente mais tarde."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    if not auth:
        return False, "❌ Serviço de autenticação Pyrebase (auth) não está disponível para registro."
    if not db:
        return False, "❌ Serviço de banco de dados Firestore (db) não está disponível para registro."

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
        # Para depuração, veja os logs do Streamlit Cloud: print(f"DEBUG Register Error: {e}")
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
