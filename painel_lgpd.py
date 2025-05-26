import streamlit as st
import datetime
import os
import pytz
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

timezone_brasilia = pytz.timezone('America/Sao_Paulo')


def render():
    # === Inicialização do Firebase (executa apenas uma vez) ===
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.markdown("""
    <h1 style='text-align: center;'>🔐 Painel LGPD</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # === Estado de sessão ===
    if "modo_auth" not in st.session_state:
        st.session_state["modo_auth"] = "login"
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # === AUTENTICAÇÃO ===
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
                            st.rerun()
                        else:
                            st.error(f"Erro ao fazer login: {resultado}")

        elif st.session_state["modo_auth"] == "registro":
            with st.form("form_registro"):
                st.subheader("📝 Registro")
                nome = st.text_input("Nome completo*")
                cpf = st.text_input("CPF*", max_chars=14, help="Digite o CPF no formato 000.000.000-00")
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

    usuario = st.session_state["usuario"]
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👤 Logado como: {usuario['email']} ({usuario['tipo']})")
    with col2:
        if st.button("🚪 Sair"):
            st.session_state["usuario"] = None
            st.session_state["modo_auth"] = "login"
            st.rerun()
    # =============================
    # 📜 Seção de Tipos de Solicitações
    # =============================
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
        - Qualquer informação relacionada à Lei de Proteção de Dados
        deverá ser solicitada pelo formulário abaixo.
        """)
    with st.expander("🗑️ Exclusão de Dados (Artigo 18-VI)"):
        st.markdown("""
        **Condições para exclusão:**
        - Dados coletados com consentimento
        - Finalidade original cumprida
        - Sem obrigação legal de armazenamento

        **Exceções Legais:** (Artigo 4º da LGPD)
        - Segurança Nacional
        - Investigação Criminal
        - Emergências de Saúde Pública
        - Pesquisas Científicas
        """)

    st.markdown("---")
    st.header("📨 Minhas Solicitações")

    docs = db.collection("solicitacoes").where("usuario_id", "==", usuario['email']).stream()
    tem_solicitacoes = False

    for doc in docs:
        tem_solicitacoes = True
        data = doc.to_dict()

        status = data.get("status", "Pendente")
        protocolo = data.get("protocolo", "")
        tipo = data.get("tipo", "")
        descricao = data.get("descricao", "")
        resumo = descricao[:60] + "..." if len(descricao) > 60 else descricao

        historico = data.get("historico", [])

        with st.expander(f"Protocolo: {protocolo} | Tipo: {tipo} | Status: {status}"):
            st.markdown(f"**Resumo da solicitação:** {resumo}")
            st.markdown(f"**Descrição completa:** {descricao}")

            st.subheader("📬 Histórico de Mensagens")
            if historico:
                for item in historico:
                    remetente = "Você" if item.get("remetente") == "cidadao" else "Admin"
                    mensagem = item.get("mensagem", "")
                    data_msg = item.get("data", "").replace("T", " ").split(".")[0]
                    if remetente == "Admin":
                        st.markdown(f"**{remetente} em `{data_msg}`:**")
                        st.success(mensagem)
                    else:
                        st.markdown(f"**{remetente} em `{data_msg}`:**")
                        st.info(mensagem)
            else:
                st.warning("⏳ Ainda não há mensagens nesta solicitação.")

            st.markdown("---")

            # 🔁 Campo para responder enquanto não estiver resolvido
            if status in ["pendente", "respondido"]:
                with st.form(f"continuar_{protocolo}"):
                    nova_msg = st.text_area("💬 Enviar nova mensagem nesta solicitação", height=100)
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
                            historico.append(nova_entrada)
                            db.collection("solicitacoes").document(protocolo).update({
                                "historico": historico,
                                "status": "pendente"
                            })
                            st.success("✅ Mensagem enviada com sucesso!")
                            st.rerun()

            elif status == "resolvido":
                st.info("✔️ Esta solicitação foi marcada como **Resolvida** e não aceita mais mensagens.")

    if not tem_solicitacoes:
        st.info("ℹ️ Você ainda não enviou nenhuma solicitação.")

    st.markdown("---")

    # =============================
    # 📤 Formulário Nova Solicitação
    # =============================
    st.subheader("Nova Solicitação")

    with st.form("nova_solicitacao"):
        nome_solicitante = st.text_input("Nome do Titular*")
        telefone = st.text_input("Telefone para contato*")
        tipo = st.selectbox("Tipo de Solicitação*", [
            "Acesso aos Dados",
            "Correção de Dados",
            "Exclusão de Dados",
            "Portabilidade",
            "Outros"
        ])
        descricao = st.text_area("Descreva sua solicitação em detalhes*")
        anexos = st.file_uploader("Anexar documentos comprobatórios", accept_multiple_files=True)

        submitted = st.form_submit_button("🚀 Enviar Solicitação")

        if submitted:
            if not all([nome_solicitante.strip(), telefone.strip(), tipo.strip(), descricao.strip()]):
                st.error("⚠️ Preencha todos os campos obrigatórios (marcados com *)")
            else:
                protocolo = f"LGPD-{datetime.datetime.now(timezone_brasilia).strftime('%Y%m%d%H%M%S%f')}"
                agora = datetime.datetime.now(timezone_brasilia)

                usuario_doc = db.collection("usuarios").document(usuario['email']).get()
                usuario_data = usuario_doc.to_dict() if usuario_doc.exists else {}
                cpf = usuario_data.get('cpf', '---')

                doc_ref = db.collection("solicitacoes").document(protocolo)
                doc_ref.set({
                    "protocolo": protocolo,
                    "email": usuario['email'],
                    "nome": nome_solicitante,
                    "cpf": cpf,
                    "telefone": telefone,
                    "tipo": tipo,
                    "descricao": descricao,
                    "anexos": [file.name for file in anexos] if anexos else [],
                    "data_envio": agora.isoformat(),
                    "status": "Recebido",
                    "responsavel": None,
                    "resposta": None,
                    "usuario_id": usuario['email'],
                    "historico": [
                        {
                            "remetente": "cidadao",
                            "mensagem": descricao,
                            "data": agora.isoformat()
                        }
                    ]
                })

                st.success(f"""
                ✅ Solicitação registrada com sucesso!  
                **Protocolo:** {protocolo}  
                **Previsão de resposta:** {(agora + datetime.timedelta(days=15)).strftime('%d/%m/%Y')}
                """)
                st.rerun()
    # =============================
    # ⏳ Seção de Prazos e Multas
    # =============================
    st.markdown("---")
    st.subheader("⏳ Prazos e Consequências Legais")
    st.markdown("""
    | Situação           | Prazo      | Consequência                   |
    |--------------------|------------|--------------------------------|
    | Resposta inicial   | 15 dias    | -                              |
    | Prorrogação        | +15 dias   | Notificação obrigatória        |
    | Descumprimento     | -          | Multa de até 2% do faturamento |
    """, unsafe_allow_html=True)

    # =============================
    # ❓ FAQ - Perguntas Frequentes
    # =============================
    st.markdown("---")
    st.subheader("❓ Perguntas Frequentes")

    with st.expander("O que fazer se não receber resposta?"):
        st.markdown("""
        1. Entre em contato via telefone
        2. Encaminhe reclamação para ANPD [**Clicando Aqui**](https://falabr.cgu.gov.br/web/home)
        3. Verifique sua caixa de E-mail (inclusive SPAM). Em alguns casos, o IPEM-MG pode responder por E-mail.
        """)

    with st.expander("Posso solicitar dados de terceiros?"):
        st.markdown("""
        ❌ Não. Você só pode solicitar informações sobre seus próprios dados pessoais.
        **Exceções:**
        - Com autorização judicial
        - Em casos de tutela coletiva devidamente comprovada
        """)

    with st.expander("Quanto tempo leva para obter uma resposta?"):
        st.markdown("""
        ⏳ O prazo legal é de até **15 dias úteis** a partir da data de solicitação.  
        ⚠️ Em alguns casos pode haver prorrogação, desde que devidamente justificada.
        """)

    with st.expander("Quais documentos preciso enviar?"):
        st.markdown("""
        🆔 Documento oficial de identificação (RG, CNH, etc.)  
        📄 Documentos específicos, dependendo do tipo de solicitação (ex.: comprovante para correção de dados).
        """)

    with st.expander("Meus dados são compartilhados?"):
        st.markdown("""
        🔐 O IPEM-MG só compartilha dados nas situações autorizadas pela **Lei nº 13.709/2018 (LGPD)**, tais como:
        - Cumprimento de obrigação legal
        - Execução de políticas públicas
        - Proteção da vida
        - Exercício regular de direitos
        - Segurança pública, defesa nacional ou atividades de investigação
        """)

    # =============================
    # 🔚 Rodapé e Fechamento
    # =============================
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: gray;">
        ℹ️ Atendimento regulamentado pela Lei nº 13.709/2018 (LGPD)<br>
        Última atualização: {datetime.datetime.now().strftime("%d/%m/%Y")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
