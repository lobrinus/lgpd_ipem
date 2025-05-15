import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pytz

st.set_page_config(page_title="Solicitação LGPD - IPEM-MG", page_icon="📨", layout="wide")

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

# === FORMULÁRIO (acessível a todos) ===
st.title("📨 Formulário de Solicitação a Dados Pessoais - LGPD")

with st.form("formulario_lgpd"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone de contato")
    email = st.text_input("E-mail de contato")
    cpf = st.text_input("CPF")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("📩 Enviar Solicitação")

if enviado:
    if nome and telefone and email and cpf and mensagem:
        br_tz = pytz.timezone("America/Sao_Paulo")
        data_envio = datetime.now(br_tz)

        db.collection("solicitacoes").add({
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "cpf": cpf,
            "mensagem": mensagem,
            "data_envio": data_envio
        })
        st.success("✅ Solicitação enviada com sucesso!")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos.")

# === VISUALIZAÇÃO ADMINISTRATIVA (restrita) ===
if st.session_state.get("logado"):
    st.markdown("---")
    st.subheader("📁 Solicitações Recebidas")

    br_tz = pytz.timezone("America/Sao_Paulo")

    # FILTRO POR DATA
    st.markdown("### 🔎 Filtrar por data")
    data_inicio = st.date_input("Data inicial", value=datetime.now(br_tz).date())
    data_fim = st.date_input("Data final", value=datetime.now(br_tz).date())

    dt_inicio = datetime.combine(data_inicio, datetime.min.time()).astimezone(br_tz)
    dt_fim = datetime.combine(data_fim, datetime.max.time()).astimezone(br_tz)

    # Busca e exibe solicitações
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

            with st.expander(f"🧾 Solicitação de {dados.get('nome')} em {data_brasil.strftime('%d/%m/%Y %H:%M')}"):
                st.markdown(f"**📧 E-mail:** {dados.get('email')}")
                st.markdown(f"**📞 Telefone:** {dados.get('telefone')}")
                st.markdown(f"**🆔 CPF:** {dados.get('cpf')}")
                st.markdown(f"**💬 Mensagem:** {dados.get('mensagem')}")
                st.markdown(f"**📅 Data de envio:** {data_brasil.strftime('%d/%m/%Y %H:%M')}")

                if st.button(f"🗑️ Deletar mensagem de {dados.get('nome')}", key=f"del_{doc.id}"):
                    db.collection("solicitacoes").document(doc.id).delete()
                    st.success("✅ Mensagem deletada com sucesso.")
                    st.rerun
else:
    st.info("🔐 Área restrita. Faça login como administrador para visualizar as solicitações.")
