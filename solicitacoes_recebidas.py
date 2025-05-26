Você disse:
import streamlit as st
import datetime
import os
import pytz
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

# 🔥 Fuso horário de Brasília
timezone_brasilia = pytz.timezone('America/Sao_Paulo')

def render():
    # 🔧 Inicialização do Firebase
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.markdown("<h1 style='text-align: center;'>🔐 Painel LGPD</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 🔑 Controle de sessão
    if "modo_auth" not in st.session_state:
        st.session_state["modo_auth"] = "login"
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # 🔒 Autenticação
    if st.session_state["usuario"] is None:
        st.subheader("Acesse ou crie sua conta")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login"):
                st.session_state["modo_auth"] = "login"
        with col2:
            if st.button("📝 Registro"):
                st.session_state["modo_auth"] = "registro"
        st.markdown("---")

        # Login
        if st.session_state["modo_auth"] == "login":
            with st.form("form_login"):
                st.subheader("🔑 Login")
                email = st.text_input("E-mail*")
                senha = st.text_input("Senha*", type="password")
                login_submit = st.form_submit_button("Entrar")

                if login_submit:
                    if not email or not senha:
                        st.warning("Por favor, preencha todos os campos.")
                    else:
                        sucesso, resultado = autenticar_usuario(email, senha)
                        if sucesso:
                            st.session_state["usuario"] = resultado
                            st.success("✅ Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao fazer login: {resultado}")

        # Registro
        elif st.session_state["modo_auth"] == "registro":
            with st.form("form_registro"):
                st.subheader("📝 Registro")
                nome = st.text_input("Nome completo*")
                cpf = st.text_input("CPF*", max_chars=14)
                telefone = st.text_input("Telefone*")
                email_reg = st.text_input("E-mail*")
                senha_reg = st.text_input("Senha*", type="password")
                senha_conf = st.text_input("Confirme a senha*", type="password")
                registro_submit = st.form_submit_button("Registrar")

                if registro_submit:
                    if not all([nome.strip(), cpf.strip(), telefone.strip(), email_reg.strip(), senha_reg.strip(), senha_conf.strip()]):
                        st.warning("Por favor, preencha todos os campos obrigatórios.")
                    elif senha_reg != senha_conf:
                        st.error("As senhas não coincidem.")
                    elif len(senha_reg) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        try:
                            sucesso, msg = registrar_usuario(
                                email=email_reg,
                                senha=senha_reg,
                                nome=nome,
                                telefone=telefone,
                                cpf=cpf,
                                tipo="cidadao"
                            )
                            if sucesso:
                                st.success("✅ Registro concluído! Agora você pode fazer login.")
                                st.session_state["modo_auth"] = "login"
                                st.rerun()
                            else:
                                st.error(f"Erro no registro: {msg}")
                        except Exception as e:
                            st.error(f"Erro inesperado: {str(e)}")

        st.stop()

    # 🔍 Identificar tipo de usuário
    usuario = st.session_state["usuario"]
    tipo_usuario = usuario.get("tipo", "cidadao")

    st.markdown("---")

    # 📜 Função para gerar protocolo único
    def gerar_protocolo():
        return f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S')}"

    # ⏳ Status possíveis
    status_opcoes = {
        "pendente": "🕒 Aguardando Resposta",
        "respondido": "✅ Respondido",
        "resolvido": "✔️ Resolvido"
    }

    # ==============================
    # 🚻 PAINEL DO CIDADÃO
    # ==============================
    if tipo_usuario == "cidadao":
        st.subheader("📄 Minhas Solicitações LGPD")

        aba = st.selectbox("Escolha uma opção", ["📨 Nova Solicitação", "📜 Minhas Solicitações"])

        if aba == "📨 Nova Solicitação":
            with st.form("form_nova_solicitacao"):
                solicitacao = st.text_area("📝 Descreva sua solicitação*", height=150)
                enviar = st.form_submit_button("🚀 Enviar Solicitação")

                if enviar:
                    if not solicitacao.strip():
                        st.warning("Por favor, descreva sua solicitação.")
                    else:
                        protocolo = gerar_protocolo()
                        data_envio = datetime.datetime.now(timezone_brasilia)

                        dados = {
                            "nome": usuario["nome"],
                            "email": usuario["email"],
                            "cpf": usuario["cpf"],
                            "protocolo": protocolo,
                            "data": data_envio.isoformat(),
                            "status": "pendente",
                            "historico": [
                                {
                                    "remetente": "cidadao",
                                    "mensagem": solicitacao,
                                    "data": data_envio.isoformat()
                                }
                            ]
                        }

                        db.collection("solicitacoes_lgpd").document(protocolo).set(dados)
                        st.success(f"✅ Solicitação enviada com sucesso!\nSeu protocolo é: {protocolo}")

        elif aba == "📜 Minhas Solicitações":
            solicitacoes_ref = db.collection("solicitacoes_lgpd").where("cpf", "==", usuario["cpf"])
            solicitacoes = solicitacoes_ref.stream()

            for doc in solicitacoes:
                dados = doc.to_dict()
                st.markdown("### 🔖 Protocolo: " + dados["protocolo"])
                st.markdown(f"**📅 Data:** {dados['data']}")
                st.markdown(f"**🟢 Status:** {status_opcoes[dados['status']]}")
                st.markdown("---")

                for msg in dados.get("historico", []):
                    remetente = "👤 Você" if msg["remetente"] == "cidadao" else "🛠️ Admin"
                    data_msg = datetime.datetime.fromisoformat(msg["data"]).strftime('%d/%m/%Y %H:%M')
                    st.markdown(f"**{remetente} ({data_msg}):**")
                    st.markdown(f"> {msg['mensagem']}")
                    st.markdown("---")

                if dados["status"] != "resolvido":
                    with st.form(f"continuar_{dados['protocolo']}"):
                        nova_msg = st.text_area("📝 Enviar nova mensagem nesta solicitação", height=100)
                        enviar_nova = st.form_submit_button("📩 Enviar")

                        if enviar_nova:
                            if not nova_msg.strip():
                                st.warning("Digite sua mensagem antes de enviar.")
                            else:
                                nova_entrada = {
                                    "remetente": "cidadao",
                                    "mensagem": nova_msg,
                                    "data": datetime.datetime.now(timezone_brasilia).isoformat()
                                }
                                dados["historico"].append(nova_entrada)
                                dados["status"] = "pendente"
                                db.collection("solicitacoes_lgpd").document(dados["protocolo"]).set(dados)
                                st.success("✅ Mensagem enviada com sucesso!")
                                st.rerun()

                    if st.button(f"✔️ Marcar como Resolvido", key=f"resolvido_{dados['protocolo']}"):
                        dados["status"] = "resolvido"
                        db.collection("solicitacoes_lgpd").document(dados["protocolo"]).set(dados)
                        st.success("🟩 Solicitação marcada como resolvida.")
                        st.rerun()

                st.markdown("----")
                # 👨‍💼 PAINEL DO ADMIN
                elif tipo_usuario == "admin":
                    st.subheader("📥 Solicitações Recebidas")
            
                    solicitacoes_ref = db.collection("solicitacoes_lgpd")
                    solicitacoes = solicitacoes_ref.stream()
            
                    for doc in solicitacoes:
                        dados = doc.to_dict()
                        st.markdown("### 🔖 Protocolo: " + dados["protocolo"])
                        st.markdown(f"""
                            - 👤 **Nome:** {dados['nome']}
                            - 📧 **E-mail:** {dados['email']}
                            - 🪪 **CPF:** {dados['cpf']}
                            - 📅 **Data:** {dados['data']}
                            - 🟢 **Status:** {status_opcoes[dados['status']]}
                        """)
                        st.markdown("**🗒️ Histórico:**")
                        st.markdown("---")
            
                        for msg in dados.get("historico", []):
                            remetente = "👤 Cidadão" if msg["remetente"] == "cidadao" else "🛠️ Admin"
                            data_msg = datetime.datetime.fromisoformat(msg["data"]).strftime('%d/%m/%Y %H:%M')
                            st.markdown(f"**{remetente} ({data_msg}):**")
                            st.markdown(f"> {msg['mensagem']}")
                            st.markdown("---")
            
                        if dados["status"] != "resolvido":
                            with st.form(f"responder_{dados['protocolo']}"):
                                resposta = st.text_area("💬 Responder", height=100)
                                enviar_resp = st.form_submit_button("📤 Enviar Resposta")
            
                                if enviar_resp:
                                    if not resposta.strip():
                                        st.warning("Digite a resposta antes de enviar.")
                                    else:
                                        nova_entrada = {
                                            "remetente": "admin",
                                            "mensagem": resposta,
                                            "data": datetime.datetime.now(timezone_brasilia).isoformat()
                                        }
                                        dados["historico"].append(nova_entrada)
                                        dados["status"] = "respondido"
                                        db.collection("solicitacoes_lgpd").document(dados["protocolo"]).set(dados)
                                        st.success("✅ Resposta enviada com sucesso!")
                                        st.rerun()
            
                            if st.button(f"✔️ Marcar como Resolvido", key=f"resolver_{dados['protocolo']}"):
                                dados["status"] = "resolvido"
                                db.collection("solicitacoes_lgpd").document(dados["protocolo"]).set(dados)
                                st.success("🟩 Solicitação marcada como resolvida.")
                                st.rerun()
            
                        st.markdown("----")
