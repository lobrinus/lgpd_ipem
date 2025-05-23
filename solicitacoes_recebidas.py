from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from login_unificado import autenticar_usuario

def render():
    st.title("📁 Solicitações Recebidas")

    # --- Verifica login e tipo de usuário ---
    if not st.session_state.get("logado", False):
        st.subheader("🔐 Login LGPD")

        email = st.text_input("Usuário (email)", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", key="btn_entrar"):
            sucesso, dados = autenticar_usuario(email, senha)
            if sucesso:
                st.session_state["logado"] = True
                st.session_state["email"] = dados["email"]
                st.session_state["tipo_usuario"] = dados["tipo"]
                if dados["tipo"] == "admin":
                    st.session_state["admin_email"] = dados["email"]
                st.success(f"✅ Bem-vindo, {dados['tipo']}. Recarregando...")
                st.rerun()
            else:
                st.error(dados)
        return  # Para a execução até o login ser feito

    # --- Logout ---
    if st.button("🚪 Sair"):
        for key in ["logado", "email", "tipo_usuario", "admin_email"]:
            st.session_state.pop(key, None)
        st.success("Você saiu com sucesso.")
        st.rerun()

    # --- Se logado como cidadão, bloquear acesso ---
    if st.session_state.get("tipo_usuario") != "admin":
        st.warning("⚠️ Você não tem acesso de administrador.")
        return

    # --- Firebase ---
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    # --- Coleta e exibição das solicitações ---
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

    # --- Rodapé ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335<br>
        <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.
    </p>
    </div>
    """, unsafe_allow_html=True)
