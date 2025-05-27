import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import pytz
import datetime
import json # Importar json no início do arquivo

auth = None
storage = None
db = None
firebase_pyrebase_app = None

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
    if not auth:
        st.error("Falha na inicialização do Pyrebase 'auth'. Verifique as chaves em firebaseConfig no código.")
    if not storage:
        st.error("Falha na inicialização do Pyrebase 'storage'. Verifique as chaves em firebaseConfig no código.")
except Exception as e_pyrebase:
    st.error(f"Falha ao inicializar Pyrebase (Auth/Storage) com firebaseConfig embutido. Exceção: {e_pyrebase}")

if not firebase_admin._apps:
    try:
        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        cred_dict = {}

        if hasattr(cred_value, 'to_dict'): # Método comum para converter AttrDict ou similar para dict
            cred_dict = cred_value.to_dict()
        elif isinstance(cred_value, dict): # Se já for um dict (ex: em desenvolvimento local com secrets.toml)
            cred_dict = cred_value
        elif isinstance(cred_value, str): # Se for uma string JSON
            try:
                cred_dict = json.loads(cred_value)
            except json.JSONDecodeError:
                raise ValueError("O segredo 'FIREBASE_CREDENTIALS' é uma string, mas não é um JSON válido.")
        else:
            # Se não for nenhum dos tipos esperados, tenta converter para dict diretamente.
            # Isso pode funcionar se for um AttrDict ou outro tipo mapping-like.
            try:
                cred_dict = dict(cred_value)
            except (TypeError, ValueError):
                 raise ValueError(f"O segredo 'FIREBASE_CREDENTIALS' (tipo: {type(cred_value)}) não pôde ser convertido para um dicionário.")

        required_admin_keys = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id"]
        missing_admin_keys = [key for key in required_admin_keys if key not in cred_dict]
        if missing_admin_keys:
            raise KeyError(f"Chave(s) ausente(s) no dicionário de 'FIREBASE_CREDENTIALS' após conversão: {', '.join(missing_admin_keys)}")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        if not db:
            st.error("Falha na inicialização do Firebase Admin SDK 'db' (Firestore). Verifique 'FIREBASE_CREDENTIALS' nos segredos.")
    except KeyError as e_key_admin:
        st.error(f"Chave não encontrada ou ausente em 'FIREBASE_CREDENTIALS' nos 'Secrets' do Streamlit Cloud ou em suas subchaves: {e_key_admin}.")
    except ValueError as e_value_admin:
        st.error(f"Formato ou valor inválido para 'FIREBASE_CREDENTIALS' nos 'Secrets' do Streamlit Cloud: {e_value_admin}")
    except Exception as e_admin:
        st.error(f"Falha geral ao inicializar Firebase Admin SDK (Firestore). Exceção: {e_admin}")
else:
    db = firestore.client()

timezone_brasilia = pytz.timezone('America/Sao_Paulo')

def autenticar_usuario(email, senha):
    if not auth:
        return False, "Serviço de autenticação (auth) não disponível."
    if not db:
        return False, "Serviço de banco de dados (db) não disponível."

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
            return False, "Usuário autenticado, mas informações de perfil não encontradas."
    except Exception as e:
        error_message = str(e).upper()
        if any(code in error_message for code in ["INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND", "USER_NOT_FOUND", "INVALID_EMAIL"]):
            return False, "E-mail ou senha incorretos."
        return False, "Erro durante a tentativa de login."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    if not auth:
        return False, "Serviço de autenticação (auth) não disponível para registro."
    if not db:
        return False, "Serviço de banco de dados (db) não disponível para registro."

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
        return True, "Registro realizado com sucesso! Faça o login."
    except Exception as e:
        error_str = str(e).upper()
        if "EMAIL_EXISTS" in error_str or "EMAIL_ALREADY_IN_USE" in error_str:
            return False, "Este e-mail já está cadastrado."
        elif "WEAK_PASSWORD" in error_str or "PASSWORD_SHOULD_BE_AT_LEAST_6_CHARACTERS" in error_str:
            return False, "A senha deve ter pelo menos 6 caracteres."
        return False, f"Erro no registro."

def upload_file_to_storage(file_object, destination_path_in_storage):
    if not storage:
        st.error("Serviço de armazenamento (storage) não disponível.")
        return None
    if file_object is None:
        return None
    try:
        file_object.seek(0)
        storage.child(destination_path_in_storage).put(file_object)
        url = storage.child(destination_path_in_storage).get_url(token=None)
        return url
    except Exception as e:
        st.error(f"Erro no upload do arquivo '{file_object.name}': {e}")
        return None

def gerar_protocolo_unico():
    return f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S%f')[:-3]}"
