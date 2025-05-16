import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore

from login import exibir_login

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("📁 Solicitações Recebidas")

    # Conteúdo restrito
    br_tz = pytz.timezone("America/Sao_Paulo")
    data_inicio = st.date_input("Data inicial", value=datetime.now(br_tz).date())
    data_fim = st.date_input("Data final", value=datetime.now(br_tz).date())
    dt_inicio = datetime.combine(data_inicio, datetime.min.time()).astimezone(br_tz)
    dt_fim = datetime.combine(data_fim, datetime.max.time()).astimezone(br_tz)

    solicitacoes = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING).stream()

    for doc in solicitacoes:
        dados = doc.to_dict()
        data_envio = dados.get("data_envio")
        if isinstance(data_envio, datetime):
            if data_envio.tzinfo is None:
                data_envio = data_envio.replace(tzinfo=pytz.UTC)
            data_brasil = data_envio.astimezone(br_tz)
            if not (dt_inicio <= data_brasil <= dt_fim):
                continue

            with st.expander(f"{dados.get('nome')} - {data_brasil.strftime('%d/%m/%Y %H:%M')}"):
                st.markdown(f"📧 **E-mail:** {dados.get('email')}")
                st.markdown(f"📞 **Telefone:** {dados.get('telefone')}")
                st.markdown(f"🆔 **CPF:** {dados.get('cpf')}")
                st.markdown(f"💬 **Mensagem:** {dados.get('mensagem')}")
                st.markdown(f"📅 **Data de envio:** {data_brasil.strftime('%d/%m/%Y %H:%M')}")

                if st.button("🗑️ Deletar", key=f"del_{doc.id}"):
                    db.collection("solicitacoes").document(doc.id).delete()
                    st.rerun()
else:
    st.warning("🔐 Área restrita. Faça login para visualizar as solicitações.")
