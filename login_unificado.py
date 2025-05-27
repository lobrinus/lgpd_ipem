import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pytz # Para fuso horário
import datetime # Para gerar protocolo único

# --- Configuração e Inicialização do Firebase ---

# Tenta carregar a configuração do Firebase Web SDK (Pyrebase) dos segredos
try:
    firebase_config_secrets = st.secrets["firebase"]
    firebaseConfig = {
        "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
        "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
        "projectId": "lgpd-ipem-mg-9f1a5",
        "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
        "messagingSenderId": "510388427771",
        "appId": "1:51038842771:web:fdcda6526f125892db8266",
        "databaseURL": ""
    }
    # Inicializa o Pyrebase (para autenticação e storage)
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()

except KeyError as e:
    st.error(f"⚠️ Erro ao carregar configuração do Firebase Web SDK dos segredos (st.secrets['firebase']): {e}. Verifique seu arquivo secrets.toml ou as configurações de segredos do Streamlit Cloud.")
    auth = None
    storage = None
except Exception as e: # Captura outras exceções de inicialização do Pyrebase
    st.error(f"⚠️ Erro inesperado ao inicializar Pyrebase: {e}")
    auth = None
    storage = None

# Inicializa o Firebase Admin SDK (para Firestore) - APENAS UMA VEZ
if not firebase_admin._apps:
    try:
        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        if isinstance(cred_value, str):
            import json
            cred_dict = json.loads(cred_value)
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
        else:
            raise ValueError("FIREBASE_CREDENTIALS nos segredos não é um dicionário nem uma string JSON válida.")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except KeyError as e:
        st.error(f"⚠️ Erro ao carregar FIREBASE_CREDENTIALS dos segredos: {e}. Verifique seu arquivo secrets.toml ou as configurações de segredos do Streamlit Cloud.")
        db = None
    except Exception as e:
        st.error(f"⚠️ Erro ao inicializar Firebase Admin SDK: {e}")
        db = None
else:
    db = firestore.client() # Pega a instância existente se já inicializado

# Fuso horário de Brasília
timezone_brasilia = pytz.timezone('America/Sao_Paulo')

# --- Funções de Autenticação e Usuário ---

def autenticar_usuario(email, senha):
    """Autentica um usuário com e-mail e senha, retornando também o nome."""
    if not auth:
        return False, "❌ Serviço de autenticação indisponível."
    if not db:
        return False, "❌ Serviço de banco de dados indisponível."

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
                "idToken": user_auth_info.get('idToken') # Retorna o idToken se necessário
            }
        else:
            # Caso o usuário exista no Auth mas não no Firestore (deve ser raro)
            return False, "❌ Usuário autenticado, mas informações complementares não encontradas no banco de dados."
    except Exception as e:
        error_message = str(e).upper() # Comparar em maiúsculas para abranger variações
        # Tenta capturar erros comuns do Firebase Auth via Pyrebase
        if "INVALID_LOGIN_CREDENTIALS" in error_message or \
           "INVALID_PASSWORD" in error_message or \
           "EMAIL_NOT_FOUND" in error_message or \
           "USER_NOT_FOUND" in error_message or \
           "INVALID_EMAIL" in error_message:
            return False, "❌ E-mail ou senha incorretos."
        # Você pode adicionar mais tratamentos de erro específicos aqui
        # st.error(f"Debug Auth Error: {e}") # Descomente para depuração
        return False, "❌ Erro durante a tentativa de login. Verifique suas credenciais ou tente mais tarde."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    """Registra um novo usuário no Firebase Authentication e no Firestore."""
    if not auth:
        return False, "❌ Serviço de autenticação indisponível para registro."
    if not db:
        return False, "❌ Serviço de banco de dados indisponível para registro."

    email_lower = email.lower()
    try:
        auth.create_user_with_email_and_password(email_lower, senha)
        db.collection("usuarios").document(email_lower).set({
            "email": email_lower,
            "nome": nome,
            "telefone": telefone,
            "cpf": cpf,
            "tipo": tipo,
            "data_registro": firestore.SERVER_TIMESTAMP # Adiciona data de registro
        })
        return True, "✅ Registro realizado com sucesso! Agora você pode fazer o login."
    except Exception as e:
        error_str = str(e).upper() # Comparar em maiúsculas
        if "EMAIL_EXISTS" in error_str or "EMAIL_ALREADY_IN_USE" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        elif "WEAK_PASSWORD" in error_str or "PASSWORD_SHOULD_BE_AT_LEAST_6_CHARACTERS" in error_str:
            return False, "❌ A senha é muito fraca. Deve ter pelo menos 6 caracteres."
        # st.error(f"Debug Register Error: {e}") # Descomente para depuração
        return False, f"❌ Erro no registro. Tente novamente ou verifique os dados informados."

# --- Funções Utilitárias ---

def upload_file_to_storage(file_object, destination_path_in_storage):
    """Faz upload de um arquivo para o Firebase Storage."""
    if not storage:
        st.error("⚠️ Serviço de armazenamento de arquivos (Storage) não está disponível.")
        return None
    if file_object is None:
        return None
    try:
        file_object.seek(0) # Garante que o ponteiro do arquivo está no início
        storage.child(destination_path_in_storage).put(file_object)
        # Obter URL pública. Para URLs privadas/com token, a lógica de get_url() precisa ser ajustada.
        url = storage.child(destination_path_in_storage).get_url(token=None)
        return url
    except Exception as e:
        st.error(f"⚠️ Erro no upload do arquivo '{file_object.name}': {e}")
        return None

def gerar_protocolo_unico():
    """Gera um protocolo único baseado na data/hora atual com milissegundos."""
    return f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S%f')[:-3]}"
