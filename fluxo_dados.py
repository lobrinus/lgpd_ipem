import streamlit as st

def render():
    st.markdown("""
    <h1 style='text-align: center;'>🔄 Fluxo de Dados LGPD</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
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
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
