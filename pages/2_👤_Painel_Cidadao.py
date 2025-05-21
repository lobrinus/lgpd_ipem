import streamlit as st
import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    # Inicialização Firebase (uma única vez)
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.title("🔐 Painel do Cidadão")

    # Inicializa variáveis de sessão
    if "modo_auth" not in st.session_state:
        st.session_state["modo_auth"] = "login"

    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # === SE NÃO ESTIVER LOGADO ===
    if st.session_state["usuario"] is None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login"):
                st.session_state["modo_auth"] = "login"
        with col2:
            if st.button("📝 Registro"):
                st.session_state["modo_auth"] = "registro"

        st.markdown("---")

        if st.session_state["modo_auth"] == "login":
            with st.form("login_form"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar"):
                    sucesso, resultado = autenticar_usuario(email, senha)
                    if sucesso:
                        st.session_state["usuario"] = resultado
                        st.success(f"Logado como: {resultado['email']}")
                        st.rerun()
                    else:
                        st.error(resultado)

        elif st.session_state["modo_auth"] == "registro":
            with st.form("registro_form"):
                nome = st.text_input("Nome completo*")
                telefone = st.text_input("Telefone*")
                email_reg = st.text_input("E-mail*")
                senha_reg = st.text_input("Senha*", type="password")
                senha_conf = st.text_input("Confirme a senha*", type="password")
                registrar_btn = st.form_submit_button("Registrar")

                if registrar_btn:
                    if not all([nome.strip(), telefone.strip(), email_reg.strip(), senha_reg.strip(), senha_conf.strip()]):
                        st.warning("Preencha todos os campos obrigatórios.")
                    elif senha_reg != senha_conf:
                        st.error("As senhas não coincidem.")
                    elif len(senha_reg) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        try:
                            sucesso, msg = registrar_usuario(email_reg, senha_reg, nome, telefone, tipo="cidadao")
                            if sucesso:
                                st.success("✅ Registro realizado com sucesso! Agora você pode fazer login.")
                                st.session_state["modo_auth"] = "login"
                                st.rerun()
                            else:
                                st.error(f"Erro no registro: {msg}")
                        except Exception as e:
                            st.error(f"Erro inesperado: {str(e)}")

        # ⚠️Impede que o resto do app seja carregado antes do login
        st.stop()

 #CONTEÚDO VISÍVEL APÓS LOGIN
    usuario = st.session_state["usuario"]

    # Sidebar com informações rápidas
    with st.sidebar:
        st.subheader("ℹ️ Informações Rápidas")
        st.markdown("""
        **Prazo Máximo de Resposta:**  
        ⏱️ 15 dias úteis  

        **Canais de Atendimento:**  
        📞 (31) 3399-7100  
        📧 lgpd@ipem.mg.gov.br  

        **Horário de Atendimento:**  
        🕒 Seg-Sex: 8h às 18h
        """)

    # Seção de Tipos de Solicitações
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

        - 🔒 **Segurança Nacional e Defesa:**  
          Para proteção do território nacional e atividades estratégicas de Estado

        - 🛡️ **Investigação Criminal:**  
          Em procedimentos de apuração de infrações penais sob tutela judicial

        - 🚨 **Emergências de Saúde Pública:**  
          Para controle de epidemias e proteção coletiva (ex: pandemias)

        - 📊 **Pesquisas Científicas:**  
          Estudos realizados por órgãos de pesquisa com dados anonimizados

        **Base Legal:**  
        *"Nos termos do Artigo 4º, III da LGPD, esses tratamentos são regidos por legislação específica que garante medidas proporcionais e necessárias ao interesse público, com total observância dos direitos fundamentais."*

        **⚠️ Atenção:**  
        A retenção nestes casos segue protocolos rigorosos de segurança e é periodicamente auditada pela Autoridade Nacional de Proteção de Dados (ANPD).
        """)

    # Seção de Processo de Solicitação
    st.markdown("---")
    st.header("📨 Como Fazer uma Solicitação")

    st.subheader("📌 Orientações Importantes")
    st.markdown("""
    1. Preencha todos os campos obrigatórios  
    2. Anexe documentos legíveis  
    3. Verifique seu e-mail regularmente  
    4. Mantenha seu protocolo de atendimento  
    5. Respeite os prazos legais

    ⚠️ Solicitações fraudulentas serão investigadas
    """)

    # --- Minhas Solicitações (compacta, antes do formulário) ---
    st.markdown("### 📬 Minhas Solicitações")
    docs = db.collection("solicitacoes").where("usuario_id", "==", st.session_state.usuario['email']).stream()
    tem_solicitacoes = False

    for doc in docs:
        tem_solicitacoes = True
        data = doc.to_dict()
        status = data.get("status", "Pendente")
        resposta = data.get("resposta")
        protocolo = data.get("protocolo", "")
        tipo = data.get("tipo", "")
        resumo = data.get("descricao", "")[:60] + "..." if len(data.get("descricao", "")) > 60 else data.get("descricao", "")

        # Exibe só o resumo e status
        with st.expander(f"Protocolo: {protocolo} | Tipo: {tipo} | Status: {status}"):
            st.markdown(f"**Resumo:** {resumo}")
            if resposta:
                st.success("📢 Sua solicitação já foi respondida pelo IPEM!")
                st.markdown(f"**Resposta:** {resposta}")

    if not tem_solicitacoes:
        st.info("Você ainda não enviou nenhuma solicitação.", icon="ℹ️")

    # --- Formulário Nova Solicitação ---
    with st.form("nova_solicitacao"):
        st.subheader("Nova Solicitação")

        email_solicitante = st.text_input("E-mail para contato*")
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

        submitted = st.form_submit_button("Enviar Solicitação")

        if submitted:
            # Validação dos campos obrigatórios
            if not all([email_solicitante.strip(), telefone.strip(), tipo.strip(), descricao.strip()]):
                st.error("⚠️ Preencha todos os campos obrigatórios (marcados com *)")
            else:
                # Geração de protocolo único
                protocolo = f"LGPD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                try:
                    # Salva na coleção 'solicitacoes' com o protocolo como ID do documento
                    doc_ref = db.collection("solicitacoes").document(protocolo)
                    doc_ref.set({
                        "protocolo": protocolo,
                        "email_solicitante": email_solicitante,
                        "telefone": telefone,
                        "tipo": tipo,
                        "descricao": descricao,
                        "anexos": [file.name for file in anexos] if anexos else [],
                        "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "status": "Recebido",
                        "responsavel": None,
                        "resposta": None,
                        "usuario_id": st.session_state.usuario['email']
                    })
                    st.success(f"""
                    ✅ Solicitação registrada com sucesso!  
                    **Protocolo:** {protocolo}  
                    **Previsão de resposta:** {(datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%d/%m/%Y')}
                    """)
                except Exception as e:
                    st.error(f"Erro ao enviar solicitação: {str(e)}")
                    

    # Seção de Prazos e Multas
    st.markdown("---")
    st.subheader("⏳ Prazos e Consequências Legais")
    st.markdown("""
    | Situação           | Prazo      | Consequência                   |
    |--------------------|------------|--------------------------------|
    | Resposta inicial   | 15 dias    | -                              |
    | Prorrogação        | +15 dias   | Notificação obrigatória        |
    | Descumprimento     | -          | Multa de até 2% do faturamento |
    """, unsafe_allow_html=True)

    # FAQ
    st.markdown("---")
    st.subheader("❓ Perguntas Frequentes")

    with st.expander("O que fazer se não receber resposta?"):
        st.markdown("""
        1. Verifique sua caixa de spam  
        2. Entre em contato via telefone  
        3. Encaminhe reclamação para ANPD
        """)

    with st.expander("Posso solicitar dados de terceiros?"):
        st.markdown("""
        ❌ Não. Você só pode solicitar informações sobre seus próprios dados pessoais, exceto:
        - Com autorização judicial
        - Em casos de tutela coletiva
        """)

    # Rodapé
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: gray;">
        ℹ️ Atendimento regulamentado pela Lei nº 13.709/2018 (LGPD)<br>
        Última atualização: {datetime.datetime.now().strftime("%d/%m/%Y")}
    </div>
    """, unsafe_allow_html=True)

    # Seção de Solicitações Existentes
    usuario = st.session_state["usuario"]
    if usuario.get("tipo") in ["cidadao", "admin"]:
        st.sidebar.success(f"👤 Logado como: {usuario['email']}")
        st.header("📬 Minhas Solicitações")
        solicitacoes_ref = db.collection("solicitacoes")
        query = solicitacoes_ref.where("email", "==", usuario["email"])
        docs = query.stream()

        tem_solicitacoes = False
        for doc in docs:
            tem_solicitacoes = True
            data = doc.to_dict()
            with st.expander(f"📌 {data.get('mensagem', 'Solicitação')} ({data['data_envio']})"):
                if "resposta" in data and data["resposta"]:
                    st.success("💬 Resposta do IPEM:")
                    st.markdown(data["resposta"])
                    st.caption(f"🕒 Respondido em: {data.get('data_resposta', 'Data não registrada')}")
                else:
                    st.info("⏳ Ainda aguardando resposta do IPEM.")

        if not tem_solicitacoes:
            st.info("Nenhuma solicitação encontrada.")


if __name__ == "__main__":
    render()
