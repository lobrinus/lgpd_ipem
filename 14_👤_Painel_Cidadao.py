import streamlit as st
import datetime
from firebase_admin import firestore
import json
import os
import firebase_admin
from firebase_admin import credentials
from login_unificado import autenticar_usuario, registrar_usuario

# Inicialização Firebase Admin (se já não tiver sido feito)
if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_CREDENTIALS")  # pegar do ambiente
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Aqui você não coloca o login/registro, só exibe o painel se estiver logado

if "usuario" in st.session_state and st.session_state["usuario"] is not None:
    usuario = st.session_state["usuario"]
    
    if usuario.get("tipo") == "cidadao":
        st.sidebar.success(f"👤 Logado como: {usuario['email']}")
        
        st.header("📬 Minhas Solicitações")

        solicitacoes_ref = db.collection("solicitacoes")
        query = solicitacoes_ref.where("email", "==", usuario["email"])
        docs = query.stream()

        tem_solicitacoes = False
        for doc in docs:
            tem_solicitacoes = True
            data = doc.to_dict()
            with st.expander(f"📌 {data['mensagem']} ({data['data_envio']})"):
                if "resposta" in data:
                    st.success("💬 Resposta do IPEM:")
                    st.markdown(data["resposta"])
                    st.caption(f"🕒 Respondido em: {data.get('data_resposta', 'Data não registrada')}")
                else:
                    st.info("⏳ Ainda aguardando resposta do IPEM.")
        
        if not tem_solicitacoes:
            st.info("Nenhuma solicitação encontrada.")

        st.markdown("---")
        st.subheader("📨 Enviar Nova Solicitação")
        nova_msg = st.text_area("Digite sua solicitação", key="txt_nova_solicitacao")
        if st.button("Enviar Solicitação", key="btn_enviar_solicitacao"):
            if nova_msg.strip():
                db.collection("solicitacoes").add({
                    "email": usuario["email"],
                    "mensagem": nova_msg.strip(),
                    "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "lido": False
                })
                st.success("✅ Solicitação enviada com sucesso!")
                st.experimental_rerun()
            else:
                st.warning("Por favor, digite a mensagem antes de enviar.")
        
        if st.button("Sair", key="btn_sair_painel"):
            st.session_state["usuario"] = None
            st.experimental_rerun()

    else:
        st.warning("⚠️ Você não tem permissão para acessar o painel cidadão.")
else:
    st.warning("⚠️ Você precisa estar logado para acessar o painel cidadão. Por favor, faça login primeiro.")
