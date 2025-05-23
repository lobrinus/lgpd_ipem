import streamlit as st
import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def render():
    # Inicializa Firebase (uma vez)
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.title("⚙️ Painel de Administração - Solicitações LGPD")
    st.markdown("---")

    # --- Autenticação Simples (você pode adaptar a sua) ---
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    if st.session_state["usuario"] is None or st.session_state["usuario"].get("tipo") != "admin":
        st.error("❌ Acesso negado. Você precisa estar logado como admin.")
        st.stop()

    usuario = st.session_state["usuario"]
    st.success(f"👤 Logado como: {usuario['email']} (Admin)")

    if st.button("🚪 Logout"):
        st.session_state["usuario"] = None
        st.experimental_rerun()

    st.markdown("---")

    # Carregar todas as solicitações do Firestore
    solicitacoes = []
    try:
        docs = db.collection("solicitacoes").stream()
        for doc in docs:
            solicitacoes.append((doc.id, doc.to_dict()))
    except Exception as e:
        st.error(f"Erro ao carregar solicitações: {str(e)}")
        st.stop()

    if not solicitacoes:
        st.info("Nenhuma solicitação encontrada.")
        st.stop()

    # Ordenar por data_envio (mais recente primeiro)
    solicitacoes = sorted(solicitacoes, key=lambda x: x[1].get("data_envio", ""), reverse=True)

    for doc_id, data in solicitacoes:
        protocolo = data.get("protocolo", "Sem protocolo")
        tipo = data.get("tipo", "Não informado")
        status = data.get("status", "Pendente")
        descricao = data.get("descricao", "")
        resposta = data.get("resposta", "")

        with st.expander(f"Protocolo: {protocolo} | Tipo: {tipo} | Status: {status}"):
            st.markdown("### Descrição da solicitação (do cidadão):")
            st.text_area("Texto da solicitação", value=descricao, disabled=True, height=150)

            st.markdown("---")
            st.markdown("### Resposta do admin:")
            with st.form(f"form_resposta_{doc_id}"):
                resposta_input = st.text_area("Escreva sua resposta aqui:", value=resposta or "", height=150)
                enviar_resposta = st.form_submit_button("Enviar resposta")
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

            if st.button(f"🗑️ Excluir solicitação {protocolo}", key=f"del_{doc_id}"):
                try:
                    db.collection("solicitacoes").document(doc_id).delete()
                    st.success(f"Solicitação {protocolo} excluída com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir solicitação: {str(e)}")
