import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.title("❓ FAQ - Perguntas Frequentes")
    st.markdown("---")

    st.markdown("Abaixo você encontra respostas rápidas para dúvidas frequentes sobre a LGPD no IPEM-MG.")

    # Lista de imagens (certifique-se que estão no mesmo diretório do app)
    imagens = ["faq_1.png", "faq_2.png", "faq_3.png", "faq_4.png"]

    for imagem in imagens:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(imagem, use_container_width=True
    # Rodapé
    st.markdown("---")
    st.info("**Não encontrou sua dúvida?** Entre em contato com nosso Encarregado de Dados: encarregado.data@ipem.mg.gov.br")

    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
