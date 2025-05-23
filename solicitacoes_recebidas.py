# painel_admin.py
import streamlit as st
import datetime
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

def render():
    # Inicializa o Firebase Admin
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["FIREBASE_CREDENTIALS"]))
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    # Autenticação
    if "usuario" not in st.session_state or st.session_state["usuario"] is None:
        st.error("🔒 Área restrita. Faça login como administrador.")
        st.stop()

    usuario = st.session_state["usuario"]
    if usuario.get("tipo") != "admin":
        st.error("🚫 Acesso negado. Esta área é exclusiva para administradores.")
        st.stop()

    st.title("📂 Painel de Administração - Solicitações LGPD")
    st.success(f"👤 Logado como: {usuario['email']} (Admin)")
    if st.button("🚪 Logout"):
        st.session_state["usuario"] = None
        st.experimental_rerun()

    st.markdown("---")

    # Filtro de pesquisa
    col1, col2 = st.columns([1, 2])
    with col1:
        filtro_tipo = st.selectbox("🔍 Filtrar por", ["Nenhum", "CPF", "Protocolo", "Nome completo"])
    with col2:
        termo_busca = st.text_input("Digite o termo de busca")

    # Carrega todas as solicitações
    solicitacoes = []
    try:
        docs = db.collection("solicitacoes").stream()
        for doc in docs:
            solicitacoes.append((doc.id, doc.to_dict()))
    except Exception as e:
        st.error(f"Erro ao carregar solicitações: {str(e)}")
        st.stop()

    # Ordenar por data_envio decrescente
    solicitacoes = sorted(solicitacoes, key=lambda x: x[1].get("data_envio", ""), reverse=True)

    # Aplicar filtro
    if filtro_tipo != "Nenhum" and termo_busca:
        termo_busca = termo_busca.strip().lower()
        def matches(data):
            campo = ""
            if filtro_tipo == "CPF":
                campo = data.get("cpf", "").lower()
            elif filtro_tipo == "Protocolo":
                campo = data.get("protocolo", "").lower()
            elif filtro_tipo == "Nome completo":
                campo = data.get("nome", "").lower()
            return termo_busca in campo
        solicitacoes = [(id, data) for id, data in solicitacoes if matches(data)]

    if not solicitacoes:
        st.info("Nenhuma solicitação encontrada.")
        st.stop()

    # Exibe as solicitações
    for doc_id, data in solicitacoes:
        nome = data.get("nome", "Desconhecido")
        email = data.get("email", "Não informado")
        cpf = data.get("cpf", "Não informado")
        protocolo = data.get("protocolo", "Sem protocolo")
        descricao = data.get("descricao", "Sem descrição.")
        resposta = data.get("resposta", "")
        data_envio = data.get("data_envio", "")[:10]
        hora_envio = data.get("data_envio", "")[11:16]
        status = data.get("status", "Pendente")

        cor_status = "🟨 Pendente" if status != "Respondido" else "🟩 Respondido"

        with st.expander(f"📄 Protocolo: {protocolo} | 📅 {data_envio} às {hora_envio} | {cor_status}"):
            st.markdown(f"**👤 Nome:** {nome}")
            st.markdown(f"**📧 E-mail:** {email}")
            st.markdown(f"**🆔 CPF:** {cpf}")
            st.markdown(f"**🗂️ Protocolo:** {protocolo}")
            st.markdown(f"**📅 Data de envio:** {data_envio}")
            st.markdown(f"**⏰ Hora:** {hora_envio}")
            st.markdown("#### ✉️ Texto da Solicitação:")
            st.markdown(f"> {descricao}", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 💬 Resposta do Administrador:")
            with st.form(f"form_resposta_{doc_id}"):
                resposta_input = st.text_area("Escreva sua resposta aqui:", value=resposta or "", height=150)
                colr1, colr2 = st.columns([2, 1])
                with colr1:
                    enviar_resposta = st.form_submit_button("📤 Enviar Resposta")
                with colr2:
                    encerrar = st.form_submit_button("✅ Encerrar Solicitação")

                if enviar_resposta:
                    try:
                        db.collection("solicitacoes").document(doc_id).update({
                            "resposta": resposta_input,
                            "status": "Respondido",
                            "data_resposta": datetime.datetime.now().isoformat()
                        })
                        st.success("Resposta enviada com sucesso!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Erro ao enviar resposta: {str(e)}")

                if encerrar:
                    try:
                        db.collection("solicitacoes").document(doc_id).update({
                            "status": "Encerrado",
                            "data_encerramento": datetime.datetime.now().isoformat()
                        })
                        st.success("Solicitação encerrada com sucesso!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Erro ao encerrar solicitação: {str(e)}")
