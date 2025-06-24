import streamlit as st

def render():
    st.markdown("""
    <h1 style='text-align: center;'>❓ FAQ - Perguntas Frequentes</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <p style='text-align: center; font-size: 18px;'>
        Abaixo você encontra respostas rápidas para dúvidas frequentes sobre a LGPD no IPEM-MG.
    </p>
    """, unsafe_allow_html=True)

    # Lista de imagens
    imagens = ["faq_1.png", "faq_2.png", "faq_3.png", "faq_4.png"]

    for imagem in imagens:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(imagem, use_container_width=True)

    # Rodapé
    st.markdown("---")
    st.info("**Não encontrou sua dúvida?** Entre em contato com nosso Encarregado de Dados: encarregado.data@ipem.mg.gov.br")

    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
