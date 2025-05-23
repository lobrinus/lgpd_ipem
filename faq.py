import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.title("❓ FAQ - Perguntas Frequentes")
    st.markdown("---")

    st.markdown("Abaixo você encontra respostas rápidas para dúvidas frequentes sobre a LGPD no IPEM-MG.")

    # Exibe imagens das FAQs
    # Substitua os nomes abaixo por suas imagens reais
    st.image("faq_1.png", use_column_width=True, caption="O que é a LGPD?")
    st.image("faq_2.png", use_column_width=True, caption="Como o IPEM-MG protege meus dados?")
    st.image("faq_3.png", use_column_width=True, caption="Como posso solicitar acesso aos meus dados pessoais?")
    st.image("faq_4.png", use_column_width=True, caption="Quais são meus direitos?")
    # Adicione ou remova imagens conforme necessário

    st.markdown("---")
    st.info("**Não encontrou sua dúvida?** Entre em contato com nosso Encarregado de Dados: encarregado.data@ipem.mg.gov.br")

    # Rodapé simples
    st.caption("© 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.")

