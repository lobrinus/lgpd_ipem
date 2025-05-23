import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.title("❓ FAQ - Perguntas Frequentes")
    st.markdown("---")

    st.markdown("Abaixo você encontra respostas rápidas para dúvidas frequentes sobre a LGPD no IPEM-MG.")

    # CSS para centralizar imagens
    st.markdown("""
        <style>
            .centered-image {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
            .centered-image img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Centralizando as imagens
    imagens = ["faq_1.png", "faq_2.png", "faq_3.png", "faq_4.png"]
    for imagem in imagens:
        st.markdown(f"""
            <div class="centered-image">
                <img src="{imagem}" alt="FAQ" />
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("**Não encontrou sua dúvida?** Entre em contato com nosso Encarregado de Dados: encarregado.data@ipem.mg.gov.br")

    # Rodapé simples
    st.caption("© 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.")
