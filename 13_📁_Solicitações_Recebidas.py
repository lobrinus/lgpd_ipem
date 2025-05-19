import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore


# Verifica login do admin
if not st.session_state.get("logado", False):
    st.error("🚫 Acesso restrito. Faça login para visualizar as solicitações.")
    st.stop()

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("📁 Solicitações Recebidas")

# Consulta todas as solicitações ordenadas por data
solicitacoes_ref = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING)
solicitacoes = solicitacoes_ref.stream()

for i, doc in enumerate(solicitacoes, start=1):
    data = doc.to_dict()
    doc_id = doc.id
    st.markdown("---")
    st.subheader(f"📨 Solicitação #{i}")
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
        st.success(f"📝 Resposta enviada:\n\n{resposta}")
    else:
        st.warning("⏳ Ainda não respondido.")
        with st.expander("✍️ Responder Solicitação"):
            resposta_texto = st.text_area("Digite sua resposta", key=f"resposta_{doc_id}")
            if st.button("📨 Enviar Resposta", key=f"btn_{doc_id}"):
                data_resposta = datetime.now(pytz.timezone("America/Sao_Paulo"))
                db.collection("solicitacoes").document(doc_id).update({
                    "resposta": resposta_texto,
                    "data_resposta": data_resposta,
                    "respondido_por": st.session_state.get("admin_email", "funcionario@ipem.mg.gov.br")
                })
                st.success("✅ Resposta enviada com sucesso.")
                st.rerun()
