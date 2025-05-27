import streamlit as st
st.write("--- DEBUG: login_unificado.py - Início da Execução ---")
print("--- DEBUG: login_unificado.py - Início da Execução (LOGS) ---")

import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import pytz
import datetime

auth = None
storage = None
db = None
firebase_pyrebase_app = None

st.write("DEBUG: Variáveis globais (auth, storage, db) definidas como None inicialmente.")
print("DEBUG: Variáveis globais (auth, storage, db) definidas como None inicialmente. (LOGS)")

firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "510388427771",
    "appId": "1:510388427771:web:fdcda6526f125892db8266",
    "databaseURL": ""
}
st.write("DEBUG: firebaseConfig (para Pyrebase) definido diretamente no código.")
print("DEBUG: firebaseConfig (para Pyrebase) definido diretamente no código. (LOGS)")

try:
    st.write("DEBUG: Tentando pyrebase.initialize_app(firebaseConfig)...")
    print("DEBUG: Tentando pyrebase.initialize_app(firebaseConfig)... (LOGS)")
    firebase_pyrebase_app = pyrebase.initialize_app(firebaseConfig)
    st.write("DEBUG: pyrebase.initialize_app executado.")
    print("DEBUG: pyrebase.initialize_app executado. (LOGS)")

    auth = firebase_pyrebase_app.auth()
    storage = firebase_pyrebase_app.storage()

    if auth:
        st.write("DEBUG: Pyrebase 'auth' inicializado com SUCESSO.")
        print("DEBUG: Pyrebase 'auth' inicializado com SUCESSO. (LOGS)")
    else:
        st.error("⚠️ ERRO FATAL em login_unificado.py: Pyrebase 'auth' é None após initialize_app. Verifique as chaves em firebaseConfig no código ou problemas de conectividade com Firebase.")
        print("ERROR: Pyrebase 'auth' é None após initialize_app. (LOGS)")

    if storage:
        st.write("DEBUG: Pyrebase 'storage' inicializado com SUCESSO.")
        print("DEBUG: Pyrebase 'storage' inicializado com SUCESSO. (LOGS)")
    else:
        st.error("⚠️ ERRO FATAL em login_unificado.py: Pyrebase 'storage' é None após initialize_app. Verifique as chaves em firebaseConfig no código ou problemas de conectividade com Firebase.")
        print("ERROR: Pyrebase 'storage' é None após initialize_app. (LOGS)")

except Exception as e_pyrebase:
    st.error(f"⚠️ ERRO FATAL em login_unificado.py: Exceção ao inicializar Pyrebase (Auth/Storage) com firebaseConfig embutido: {str(e_pyrebase)}")
    print(f"ERROR: Exceção ao inicializar Pyrebase: {str(e_pyrebase)} (LOGS)")
    auth = None
    storage = None


if not firebase_admin._apps:
    try:
        st.write("DEBUG: Tentando inicializar Firebase Admin SDK (Firestore) via st.secrets...")
        print("DEBUG: Tentando inicializar Firebase Admin SDK (Firestore) via st.secrets... (LOGS)")

        if "FIREBASE_CREDENTIALS" not in st.secrets:
            st.error("⚠️ ERRO FATAL em login_unificado.py: A chave 'FIREBASE_CREDENTIALS' NÃO FOI ENCONTRADA nos seus 'Secrets' do Streamlit Cloud.")
            print("ERROR: Chave 'FIREBASE_CREDENTIALS' não encontrada em st.secrets. (LOGS)")
            raise KeyError("Chave 'FIREBASE_CREDENTIALS' não encontrada em st.secrets")

        cred_value = st.secrets["FIREBASE_CREDENTIALS"]
        st.write(f"DEBUG: st.secrets['FIREBASE_CREDENTIALS'] lido. Tipo: {type(cred_value)}")
        print(f"DEBUG: st.secrets['FIREBASE_CREDENTIALS'] lido. Tipo: {type(cred_value)} (LOGS)")

        if isinstance(cred_value, str):
            import json
            cred_dict = json.loads(cred_value)
            st.write("DEBUG: 'FIREBASE_CREDENTIALS' processado como string JSON.")
            print("DEBUG: 'FIREBASE_CREDENTIALS' processado como string JSON. (LOGS)")
        elif isinstance(cred_value, dict):
            cred_dict = cred_value
            st.write("DEBUG: 'FIREBASE_CREDENTIALS' processado como dicionário.")
            print("DEBUG: 'FIREBASE_CREDENTIALS' processado como dicionário. (LOGS)")
        else:
            st.error("⚠️ ERRO FATAL em login_unificado.py: O segredo 'FIREBASE_CREDENTIALS' não é um dicionário nem uma string JSON válida.")
            print("ERROR: 'FIREBASE_CREDENTIALS' não é dict nem str. (LOGS)")
            raise ValueError("O segredo 'FIREBASE_CREDENTIALS' não é um dicionário nem uma string JSON válida.")

        required_admin_keys = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id"]
        missing_admin_keys = [key for key in required_admin_keys if key not in cred_dict]
        if missing_admin_keys:
            st.error(f"⚠️ ERRO FATAL em login_unificado.py: Chave(s) ausente(s) no dicionário de 'FIREBASE_CREDENTIALS': {', '.join(missing_admin_keys)}.")
            print(f"ERROR: Chave(s) ausente(s) no dicionário de 'FIREBASE_CREDENTIALS': {', '.join(missing_admin_keys)}. (LOGS)")
            raise KeyError(f"Chave(s) ausente(s) no dicionário de 'FIREBASE_CREDENTIALS': {', '.join(missing_admin_keys)}")

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        if db:
            st.write("DEBUG: Firebase Admin SDK 'db' (Firestore) inicializado com SUCESSO.")
            print("DEBUG: Firebase Admin SDK 'db' (Firestore) inicializado com SUCESSO. (LOGS)")
        else:
            st.error("⚠️ ERRO FATAL em login_unificado.py: Firebase Admin SDK 'db' (Firestore) é None após initialize_app. Verifique 'FIREBASE_CREDENTIALS' nos seus segredos e logs.")
            print("ERROR: Firebase Admin SDK 'db' (Firestore) é None após initialize_app. (LOGS)")

    except KeyError as e_key_admin:
        st.error(f"⚠️ ERRO FATAL em login_unificado.py (KeyError Admin SDK): {str(e_key_admin)}. Verifique 'FIREBASE_CREDENTIALS' nos 'Secrets'.")
        print(f"ERROR: KeyError ao processar 'FIREBASE_CREDENTIALS': {str(e_key_admin)} (LOGS)")
        db = None
    except ValueError as e_value_admin:
        st.error(f"⚠️ ERRO FATAL em login_unificado.py (ValueError Admin SDK): {str(e_value_admin)}. Formato de 'FIREBASE_CREDENTIALS' pode estar incorreto.")
        print(f"ERROR: ValueError ao processar 'FIREBASE_CREDENTIALS': {str(e_value_admin)} (LOGS)")
        db = None
    except Exception as e_admin:
        st.error(f"⚠️ ERRO FATAL em login_unificado.py: Exceção geral ao inicializar Firebase Admin SDK (Firestore): {str(e_admin)}")
        print(f"ERROR: Exceção geral ao inicializar Firebase Admin SDK: {str(e_admin)} (LOGS)")
        db = None
else:
    db = firestore.client()
    st.write("DEBUG: Firebase Admin SDK (Firestore) já estava inicializado. DB 'db' obtido.")
    print("DEBUG: Firebase Admin SDK (Firestore) já estava inicializado. DB 'db' obtido. (LOGS)")


timezone_brasilia = pytz.timezone('America/Sao_Paulo')

def autenticar_usuario(email, senha):
    if not auth:
        return False, "❌ Serviço de autenticação (auth) não inicializado. Verifique os erros acima."
    if not db:
        return False, "❌ Serviço de banco de dados (db) não inicializado. Verifique os erros acima."
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
        print(f"DEBUG Auth Error: {e} (LOGS)")
        return False, "❌ Erro durante a tentativa de login."

def registrar_usuario(email, senha, nome, telefone, cpf, tipo="cidadao"):
    if not auth:
        return False, "❌ Serviço de autenticação (auth) não disponível para registro."
    if not db:
        return False, "❌ Serviço de banco de dados (db) não disponível para registro."
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
        return True, "✅ Registro realizado com sucesso! Faça o login."
    except Exception as e:
        error_str = str(e).upper()
        if "EMAIL_EXISTS" in error_str or "EMAIL_ALREADY_IN_USE" in error_str:
            return False, "❌ Este e-mail já está cadastrado."
        elif "WEAK_PASSWORD" in error_str or "PASSWORD_SHOULD_BE_AT_LEAST_6_CHARACTERS" in error_str:
            return False, "❌ A senha deve ter pelo menos 6 caracteres."
        print(f"DEBUG Register Error: {e} (LOGS)")
        return False, f"❌ Erro no registro."

def upload_file_to_storage(file_object, destination_path_in_storage):
    if not storage:
        st.error("⚠️ Serviço de armazenamento (storage) não disponível.")
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

st.write("--- DEBUG: login_unificado.py - Fim da Execução ---")
print("--- DEBUG: login_unificado.py - Fim da Execução (LOGS) ---")
