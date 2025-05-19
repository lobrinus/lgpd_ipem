import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore

# Garante que apenas admins vejam essa página
if not st.session_state.get("logado", False):
    st.error("🚫 Acesso restrito. Faça login para visualizar as solicitações.")
    st.stop()

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("📁 Solicitações Recebidas")

# Buscar todas as solicitações
solicitacoes_ref = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING)
solicitacoes = solicitacoes_ref.stream()

count = 0
for doc in solicitacoes:
    data = doc.to_dict()
    count += 1
    st.markdown("---")
    st.subheader(f"📨 Solicitação #{count}")
    st.write(f"**Nome:** {data.get('nome')}")
    st.write(f"**Telefone:** {data.get('telefone')}")
    st.write(f"**Email:** {data.get('email')}")
    st.write(f"**CPF:** {data.get('cpf')}")
    st.write(f"**Mensagem:** {data.get('mensagem')}")
    
    data_envio = data.get("data_envio")
    if isinstance(data_envio, datetime):
        data_envio = data_envio.astimezone(pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y às %H:%M')
    st.write(f"**Enviado em:** {data_envio}")

    resposta = data.get("resposta")
    if resposta:
        st.success(f"📝 Resposta: {resposta}")
    else:
        st.warning("⏳ Ainda não respondido.")
