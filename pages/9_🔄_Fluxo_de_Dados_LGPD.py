import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.title("🔄 Fluxo de Dados LGPD")
    st.markdown("---")
    st.markdown("""
    Visualização dos principais fluxos de dados pessoais no IPEM-MG e as medidas de proteção em cada etapa:
    """)

    st.subheader("1. Coleta de Dados")
    st.markdown("""
    **Fontes:**
    - Formulários físicos e digitais
    - Sistemas internos
    - Parceiros e outras fontes legítimas

    **Medidas:**
    - Informar finalidade e base legal
    - Coletar apenas o necessário
    - Obter consentimento quando aplicável
    """)

    st.subheader("2. Armazenamento")
    st.markdown("""
    **Locais:**
    - Bancos de dados seguros
    - Sistemas com controle de acesso
    - Arquivos físicos em locais restritos

    **Medidas:**
    - Criptografia de dados sensíveis
    - Controle de acesso baseado em função
    - Backup regular e seguro
    """)

    st.subheader("3. Processamento/Uso")
    st.markdown("""
    **Atividades:**
    - Análise para tomada de decisão
    - Prestação de serviços públicos
    - Gestão interna

    **Medidas:**
    - Acesso apenas por pessoal autorizado
    - Registro de operações
    - Monitoramento de atividades
    """)

    st.subheader("4. Compartilhamento")
    st.markdown("""
    **Destinatários:**
    - Outros órgãos públicos
    - Parceiros contratados
    - Autoridades quando exigido por lei

    **Medidas:**
    - Acordos de confidencialidade
    - Anonimização quando possível
    - Canais seguros de transferência
    """)

    st.subheader("5. Descarte")
    st.markdown("""
    **Quando:**
    - Cumprida a finalidade
    - Expirado prazo de retenção
    - Solicitação de exclusão pelo titular

    **Medidas:**
    - Exclusão segura (digital)
    - Destruição física adequada
    - Registro do descarte
    """)

    # Rodapé
    st.markdown("""
    <hr>
    <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
    </p>
    """, unsafe_allow_html=True)
