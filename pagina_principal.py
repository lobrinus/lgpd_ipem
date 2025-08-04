import streamlit as st
from datetime import datetime
import time
import re

def render():
    st.markdown("""
    <h1 style='text-align: center;'>🏠 Bem Vindo ao Portal LGPD - IPEM-MG</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("⚡ Acesso Rápido")
    cols = st.columns([1, 1, 1], gap="small")
    with cols[0]:
        st.link_button(
            label="📜 Política de Privacidade",
            url="https://www.ipem.mg.gov.br/politica-de-privacidade-e-protecao-de-dados-pessoais",
            use_container_width=True
        )
    with cols[1]:
        st.link_button(
            label="📋 Solicitação de Dados",
            url="https://www.ipem.mg.gov.br/fale-conosco",
            use_container_width=True
        )
    with cols[2]:
        st.link_button(
            label="⚖️ Guia LGPD",
            url="https://www.gov.br/governodigital/pt-br/lgpd-pagina-do-cidadao",
            use_container_width=True
        )

    with st.container():
        col1, col2 = st.columns([2, 3])
        with col1:
            st.subheader("📞 Contato do Encarregado de Dados")
            st.markdown("""
            **Encarregado (DPO):** Leonardo Silva Marafeli
            **E-mail:** [encarregado.data@ipem.mg.gov.br](mailto:encarregado.data@ipem.mg.gov.br)
            **Telefone:** (31) 3399-7100
            **Horário:** 8h às 18h (dias úteis)
            **Endereço:**
            Rua Cristiano França Teixeira Guimarães, 80
            Bairro Cinco - Contagem/MG
            CEP: 32010-130
            """)
        with col2:
            st.subheader("🚨 Canal de Denúncias LGPD")
            st.markdown("""
            **Para reportar incidentes ou irregularidades relacionados a LGPD:**
            - 📧 [encarregado.data@ipem.mg.gov.br](mailto:encarregado.data@ipem.mg.gov.br)
            - 📞 (31) 3399-7100 / 0800 335 335
            - 🌐 Formulário Online via Painel LGPD
            """)
    st.markdown("---")

   
    st.subheader("📢 Novidades do Portal") 
    with st.expander("🔔 Atualizações do Sistema (Status: 20/05/2025)"):
        st.markdown("""
        - Novo Painel de Login
        - Nova funcionalidade de acompanhamento de solicitações.
        - Atualização da Política de Privacidade.
        - Integração com notícias sobre a LGPD diretamente de fontes governamentais.
        - Treinamento LGPD para servidores (em andamento).
        """)
    st.markdown("---")
    st.subheader("📚 Recursos Importantes")
    tab1, tab2, tab3 = st.tabs(["Legislação", "Boas Práticas", "FAQ"])
    with tab1:
        st.markdown("""
        **Legislação Relevante:**
        - [Lei nº 13.709/2018 (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
        - [Decreto nº 10.474/2020](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10474.htm)
        - [Resoluções da ANPD](https://www.gov.br/anpd/pt-br)
        """)
    with tab2:
        st.markdown("""
        **Principais Boas Práticas:**
        1. Coleta mínima necessária de dados.
        2. Criptografia de dados sensíveis em trânsito e repouso.
        3. Atualização regular de sistemas e softwares.
        4. Treinamento anual de colaboradores sobre LGPD.
        5. Auditorias periódicas de segurança e conformidade.
        """)
    with tab3:
        st.markdown("""
        **Perguntas Frequentes:**
        
        P: Como solicitar exclusão de dados?  
        R: Através do Painel LGPD ou formulário específico de contato com o DPO.
        
        P: Quanto tempo demora uma resposta à minha solicitação?  
        R: O prazo padrão é de até 15 dias, podendo ser prorrogado mediante justificativa, dependendo da complexidade.
        
        P: Posso acessar dados de terceiros através do portal?  
        R: Não. O acesso é restrito aos dados do próprio titular, salvo representação legal ou autorização judicial.
        """)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px; font-size:0.9em;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7100 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)






