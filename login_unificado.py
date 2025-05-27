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
firebase_pyrebase_app = None # Mantido para referência, caso necessário

# --- Configuração e Inicialização do Pyrebase (Auth e Storage) ---
# Usando as configurações diretamente no código, conforme seu arquivo login_unificado (6).py
firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "510388427771",
    "appId": "1:510388427771:web:fdcda6526f125892db8266",
    "databaseURL": "" # Geralmente vazio se não estiver usando Realtime Database ativamente
}

try:
    # st.write("DEBUG: Tentando inicializar Pyrebase com firebaseConfig...") # Descomente para debug na interface
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()
    if not auth:
        st.error("⚠️ Erro Crítico em login_unificado.py: Pyrebase 'auth' não foi inicializado após initialize_app. Verifique as chaves em firebaseConfig.")
    if not storage:
        st.error("⚠️ Erro Crítico em login_unificado.py: Pyrebase 'storage' não foi inicializado após initialize_app. Verifique as chaves em firebaseConfig.")
    # st.write(f"DEBUG: Pyrebase auth: {'Inicializado' if auth else 'FALHOU'}") # Descomente para debug
    # st.write(f"DEBUG: Pyrebase storage: {'Inicializado' if storage else 'FALHOU'}") # Descomente para debug

except Exception as e_pyrebase:
    st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha ao inicializar Pyrebase (Auth/Storage). Exceção: {e_pyrebase}")
    # auth e storage permanecem None, o que causará o erro "Serviço ... indisponível" nas outras páginas.

# --- Configuração e Inicialização do Firebase Admin SDK (Firestore) ---
if not firebase_admin._apps:
    try:
        # st.write("DEBUG: Tentando inicializar Firebase Admin SDK...") # Descomente para debug
        # Esta parte DEPENDE da configuração correta de [FIREBASE_CREDENTIALS]
        # nos seus "Secrets" do Streamlit Cloud.
        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        if isinstance(cred_value, str):
            import json
            cred_dict = json.loads(cred_value)
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
        else:
            # Este erro aparecerá se 'FIREBASE_CREDENTIALS' não for um dict ou JSON str
            raise ValueError("O segredo 'FIREBASE_CREDENTIALS' nos seus 'Secrets' do Streamlit Cloud não é um dicionário nem uma string JSON válida.")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        if not db:
            st.error("⚠️ Erro Crítico em login_unificado.py: Firebase Admin SDK 'db' (Firestore) não foi inicializado após initialize_app. Verifique as credenciais.")
        # st.write(f"DEBUG: Firebase Admin SDK db: {'Inicializado' if db else 'FALHOU'}") # Descomente para debug

    except KeyError as e_key_admin:
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Chave 'FIREBASE_CREDENTIALS' não encontrada nos seus 'Secrets' do Streamlit Cloud: {e_key_admin}. Verifique o nome e a existência da seção.")
        # db permanece None
    except ValueError as e_value_admin: # Captura o ValueError de formato inválido do segredo
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Formato inválido para 'FIREBASE_CREDENTIALS' nos seus 'Secrets' do Streamlit Cloud: {e_value_admin}")
        # db permanece None
    except Exception as e_admin:
        st.error(f"⚠️ Erro Crítico em login_unificado.py: Falha geral ao inicializar Firebase Admin SDK (Firestore). Exceção: {e_admin}")
        # db permanece None
else:
    # Se já inicializado (ex: por um rerun do Streamlit), apenas obtenha a instância
    db = firestore.client()
    # st.write(f"DEBUG: Firebase Admin SDK db (já inicializado): {'Disponível' if db else 'FALHOU'}") # Descomente para debug

# Fuso horário de Brasília
timezone_brasilia = pytz.timezone('America/Sao_Paulo')

# --- Funções de Autenticação e Usuário ---
# (As funções autenticar_usuario, registrar_usuario, upload_file_to_storage, gerar_protocolo_unico permanecem as mesmas da versão anterior - login_unificado_py_final_v3)
# Vou incluí-las aqui para o código ser completo:

def autenticar_usuario(email, senha):
    if not auth:
        return False, "❌ Serviço de autenticação Pyrebase (auth) não está disponível."
    if not db:
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
                "nome": user_data.get("nome", ""),
                "idToken": user_auth_info.get('idToken')
            }
        else:
            return False, "❌ Usuário autenticado, mas informações de perfil não encontradas no banco de dados."
    except Exception as e:
        error_message = str(e).upper()
        if any(code in error_message for code in ["INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND", "USER_NOT_FOUND", "INVALID_EMAIL"]):
            return False, "❌ E-mail ou senha incorretos."
        # Para depuração, veja os logs do Streamlit Cloud: print(f"Debug Auth Error: {e}")
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
        # Para depuração, veja os logs do Streamlit Cloud: print(f"Debug Register Error: {e}")
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
