import streamlit as st
import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    # Inicialização do Firebase (executa uma única vez)
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.markdown("<h1 style='text-align: center;'>🔐 Painel LGPD</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Estado da sessão
    if "modo_auth" not in st.session_state:
        st.session_state["modo_auth"] = "login"  # "login" ou "registro"
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # AUTENTICAÇÃO
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
                            st.experimental_rerun()
                        else:
                            st.error(f"Erro ao fazer login: {resultado}")

        elif st.session_state["modo_auth"] == "registro":
            with st.form("form_registro"):
                st.subheader("📝 Registro")
                nome = st.text_input("Nome completo*")
                telefone = st.text_input("Telefone*")
                email_reg = st.text_input("E-mail*")
                senha_reg = st.text_input("Senha*", type="password")
                senha_conf = st.text_input("Confirme a senha*", type="password")
                registro_submit = st.form_submit_button("Registrar")

                if registro_submit:
                    if not all([nome.strip(), telefone.strip(), email_reg.strip(), senha_reg.strip(), senha_conf.strip()]):
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
                                tipo="cidadao"
                            )
                            if sucesso:
                                st.success("✅ Registro concluído! Agora você pode fazer login.")
                                st.session_state["modo_auth"] = "login"
                                st.experimental_rerun()
                            else:
                                st.error(f"Erro no registro: {msg}")
                        except Exception as e:
                            st.error(f"Erro inesperado: {str(e)}")

        st.stop()  # Não prossegue sem login

    # Usuário logado
    usuario = st.session_state["usuario"]
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👤 Logado como: {usuario['email']} ({usuario['tipo']})")
    with col2:
        if st.button("🚪 Sair"):
            st.session_state["usuario"] = None
            st.session_state["modo_auth"] = "login"
            st.experimental_rerun()

    # Tipos de solicitações
    st.header("📋 Tipos de Solicitações")
    with st.expander("🔍 Confirmar Existência de Dados (Artigo 18-I)"):
        st.markdown("""
        **O que você pode solicitar:**
        - Verificação se o IPEM-MG possui seus dados cadastrais

        **Documentação necessária:**
        - Cópia do documento de identificação

        **Prazo máximo:** 24 horas (resposta simplificada)
        """)
    with st.expander("📂 Acesso aos Dados (Artigo 18-II)"):
        st.markdown("""
        **O que você pode solicitar:**
        - Cópia completa de todos seus dados armazenados
        - Histórico de uso dos dados
        - Informação sobre o compartilhamento dos dados

        **Prazo máximo:** 15 dias úteis
        """)
    with st.expander("✏️ Correção de Dados (Artigo 18-III)"):
        st.markdown("""
        **Quando solicitar:**
        - Dados desatualizados
        - Informações incorretas
        - Registros incompletos

        **Anexos obrigatórios:**
        - Documento comprobatório da correção
        - Identificação válida
        """)
    with st.expander("ℹ️ Informativa"):
        st.markdown("""
        - **Qualquer** informação relacionada à **Lei de Proteção de Dados**
        deverá ser solicitada pelo formulário abaixo.
        """)
    with st.expander("🗑️ Exclusão de Dados (Artigo 18-VI)"):
        st.markdown("""
        **Condições para exclusão:**
        - Dados coletados com consentimento
        - Finalidade original cumprida
        - Sem obrigação legal de armazenamento

        **Exceções Legais (Artigo 4º da LGPD):**  
        O IPEM-MG poderá reter dados pessoais mesmo após o cumprimento da finalidade original nos seguintes casos:
        - 🔒 **Segurança Nacional e Defesa:** Para proteção do território nacional e atividades estratégicas de Estado
        - 🛡️ **Investigação Criminal:** Em procedimentos de apuração de infrações penais sob tutela judicial
        - 🚨 **Emergências de Saúde Pública:** Para controle de epidemias e proteção coletiva (ex: pandemias)
        - 📊 **Pesquisas Científicas:** Estudos realizados por órgãos de pesquisa com dados anonimizados

        **Base Legal:**  
        *"Nos termos do Artigo 4º, III da LGPD, esses tratamentos são regidos por legislação específica que garante medidas proporcionais e necessárias ao interesse público, com total observância dos direitos fundamentais."*

        **⚠️ Atenção:**  
        A retenção nestes casos segue protocolos rigorosos de segurança e é periodicamente auditada pela Autoridade Nacional de Proteção de Dados (ANPD).
        """)

    st.markdown("---")
    st.header("📨 Minhas Solicitações")

    # Filtro (exemplo: filtro por protocolo, tipo, status, etc)
    filtro_protocolo = st.text_input("Filtrar por protocolo (ex: LGPD-2023...)")
    filtro_tipo = st.selectbox("Filtrar por tipo", options=["Todos", "Acesso aos Dados", "Correção de Dados", "Exclusão de Dados", "Portabilidade", "Outros"])
    filtro_status = st.selectbox("Filtrar por status", options=["Todos", "Recebido", "Pendente", "Respondido", "Concluído"])

    solicitacoes = []
    query = db.collection("solicitacoes").where("usuario_id", "==", usuario['email'])

    if filtro_protocolo:
        query = query.where("protocolo", "==", filtro_protocolo.strip())
    if filtro_tipo != "Todos":
        query = query.where("tipo", "==", filtro_tipo)
    if filtro_status != "Todos":
        query = query.where("status", "==", filtro_status)

    docs = query.stream()
    for doc in docs:
        solicitacoes.append((doc.id, doc.to_dict()))

    if not solicitacoes:
        st.info("Nenhuma solicitação encontrada com esses filtros.", icon="ℹ️")

    # Mostrar as solicitações
    for doc_id, data in sorted(solicitacoes, key=lambda x: x[1].get("data_envio", ""), reverse=True):
        protocolo = data.get("protocolo", "")
        tipo = data.get("tipo", "")
        status = data.get("status", "Pendente")
        descricao = data.get("descricao", "") or ""
        resposta = data.get("resposta", None)

        with st.expander(f"Protocolo: {protocolo} | Tipo: {tipo} | Status: {status}"):
            st.markdown("### Descrição da solicitação:")
            st.text_area("Solicitação do cidadão", value=descricao, disabled=True, height=150)

            if resposta:
                st.success("📢 Sua solicitação foi respondida:")
                st.markdown(f"**Resposta:** {resposta}")

            # Se for admin, pode responder e excluir
            if usuario["tipo"] == "admin":
                with st.form(f"form_resposta_{doc_id}"):
                    resposta_admin = st.text_area("Responder solicitação", value=resposta or "")
                    enviar_resposta = st.form_submit_button("Enviar resposta")
                    if enviar_resposta:
                        try:
                            doc_ref = db.collection("solicitacoes").document(doc_id)
                            doc_ref.update({
                                "resposta": resposta_admin,
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

    st.markdown("---")
    st.header("📨 Nova Solicitação")
    with st.form("nova_solicitacao"):
        email_solicitante = st.text_input("Seu e-mail*", value=usuario["email"], disabled=True)
        tipo_solicitacao = st.selectbox("Tipo da solicitação", ["Acesso aos Dados", "Correção de Dados", "Exclusão de Dados", "Portabilidade", "Outros"])
        descricao_solicitacao = st.text_area("Descreva sua solicitação*", height=150)
        enviar = st.form_submit_button("Enviar Solicitação")

        if enviar:
            if not descricao_solicitacao.strip():
                st.warning("A descrição da solicitação é obrigatória.")
            else:
                protocolo_novo = f"LGPD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                try:
                    db.collection("solicitacoes").add({
                        "usuario_id": usuario["email"],
                        "protocolo": protocolo_novo,
                        "tipo": tipo_solicitacao,
                        "descricao": descricao_solicitacao,
                        "status": "Recebido",
                        "data_envio": datetime.datetime.now().isoformat(),
                        "resposta": None
                    })
                    st.success(f"Solicitação enviada com sucesso! Protocolo: {protocolo_novo}")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao enviar solicitação: {str(e)}")
