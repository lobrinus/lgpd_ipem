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

    # Controla o estado de login na sessão
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # Se não estiver logado, exibe formulário de login
    if st.session_state["usuario"] is None:
        st.title("🔐 Login - Painel do Cidadão")
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
        st.info("Por favor, faça login para acessar o painel.")
        return  # Encerra aqui se não estiver logado
    
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
    st.header("📋 Tipos de Solicitações ")
    
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
    
    with st.expander("ℹ️ Informativa "):
        st.markdown("""
        - **Qualquer** informação relacionado a **Lei de Proteção de Dados**
        deverá ser solicitada pelo Formulario abaixo
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
    
    col1, col2 = st.columns([3,2])
    with col1:
        with st.form("nova_solicitacao"):
            st.subheader("Nova Solicitação")
            tipo = st.selectbox("Tipo de Solicitação", [
                "Acesso aos Dados",
                "Correção de Dados",
                "Exclusão de Dados",
                "Portabilidade",
                "Outros"
            ])
