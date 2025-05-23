import streamlit as st
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario  # Função exige email e senha

def render():
    st.title("📁 Solicitações Recebidas")

    # 🔐 Login
    if "usuario_autenticado" not in st.session_state:
        with st.form("login_form"):
            st.subheader("🔐 Login do Administrador")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")

            if submit:
                try:
                    usuario, tipo = autenticar_usuario(email, senha)
                    if tipo == "admin":
                        st.session_state.usuario_autenticado = True
                        st.session_state.email = email
                        st.session_state.tipo_usuario = tipo
                        st.success("✅ Login realizado com sucesso.")
                        st.experimental_rerun()
                    else:
                        st.error("🚫 Acesso negado. Você não tem permissão de administrador.")
                except Exception as e:
                    st.error(f"Erro na autenticação: {e}")

    if st.session_state.get("tipo_usuario") != "admin":
        st.error("🚫 Você não tem acesso de administrador.")
        return

    # 🔥 Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    filtro = st.text_input("🔍 Buscar por protocolo, CPF ou nome:")

    solicitacoes_ref = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING)
    solicitacoes = solicitacoes_ref.stream()

    resultados = []
    for doc in solicitacoes:
        dados = doc.to_dict()
        if filtro:
            if filtro.lower() not in str(dados.get("cpf", "")).lower() \
            and filtro.lower() not in str(dados.get("nome", "")).lower() \
            and filtro.lower() not in str(dados.get("protocolo", "")).lower():
                continue
        resultados.append((doc.id, dados))

    if not resultados:
        st.info("Nenhuma solicitação encontrada.")
        return

    for i, (doc_id, data) in enumerate(resultados, 1):
        st.markdown("---")
        st.subheader(f"📨 Solicitação #{i}")
        st.write(f"**Protocolo:** `{data.get('protocolo', 'N/A')}`")
        st.write(f"**Nome:** {data.get('nome')}")
        st.write(f"**Telefone:** {data.get('telefone')}")
        st.write(f"**Email:** {data.get('email')}")
        st.write(f"**CPF:** {data.get('cpf')}")

        data_envio = data.get("data_envio")
        if isinstance(data_envio, datetime):
            data_envio = data_envio.astimezone(pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y às %H:%M')
        st.write(f"**Enviado em:** {data_envio}")

        # STATUS visual
        resolvido = data.get("resolvido", False)
        if resolvido:
            st.markdown(
                '<div style="background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;">✔️ Resolução Confirmada</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background-color: #FFC107; color: black; padding: 8px; border-radius: 5px;">⏳ Aguardando resposta</div>',
                unsafe_allow_html=True
            )

        # Histórico de mensagens
        mensagens = data.get("mensagens", [])
        st.markdown("**Histórico de mensagens:**")
        for msg in mensagens:
            dt = msg.get("data")
            if isinstance(dt, datetime):
                dt = dt.astimezone(pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y %H:%M')
            st.write(f"{dt} - **{msg.get('de').capitalize()}**: {msg.get('texto')}")

        if not resolvido:
            with st.expander("✍️ Enviar nova resposta"):
                resposta_texto = st.text_area("Digite sua resposta", key=f"resposta_{doc_id}")
                if st.button("📨 Enviar Resposta", key=f"btn_{doc_id}"):
                    if resposta_texto.strip():
                        nova_msg = {
                            "de": "admin",
                            "texto": resposta_texto,
                            "data": datetime.now(pytz.timezone("America/Sao_Paulo"))
                        }
                        mensagens.append(nova_msg)
                        db.collection("solicitacoes").document(doc_id).update({
                            "mensagens": mensagens
                        })
                        st.success("✅ Resposta enviada com sucesso.")
                        st.rerun()
                    else:
                        st.warning("Digite uma resposta antes de enviar.")

            if st.button("✔️ Marcar como resolvido", key=f"resolver_{doc_id}"):
                db.collection("solicitacoes").document(doc_id).update({
                    "resolvido": True,
                    "data_resolvido": datetime.now(pytz.timezone("America/Sao_Paulo"))
                })
                st.success("✅ Solicitação marcada como resolvida.")
                st.rerun()

        if st.button("🗑️ Excluir Solicitação", key=f"excluir_{doc_id}"):
            db.collection("solicitacoes").document(doc_id).delete()
            st.success("🗑️ Solicitação excluída.")
            st.rerun()
