import streamlit as st
import base64
import os
import feedparser
from datetime import datetime
from PIL import Image

def image_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
        
from login_unificado import registrar_usuario, autenticar_usuario

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

    # Rodapé com imagens base64
    try:
        icone_ipem = image_to_base64("icone_ipem.png")
        lgpd_logo = image_to_base64("lgpd_logo.png")

        st.markdown(f"""
        <style>
            .footer {{
                position: fixed;
                bottom: 10px;
                right: 50px;
                display: flex;
                gap: 10px;
            }}
            .footer img {{
                width: 50px;
                height: auto;
                transition: transform 0.3s ease;
            }}
            .footer img:hover {{
                transform: scale(1.2);
            }}
        </style>

        <div class="footer">
            <img src="data:image/png;base64,{icone_ipem}" alt="Ícone IPEM">
            <img src="data:image/png;base64,{lgpd_logo}" alt="Logo LGPD">
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Erro: Não foi possível carregar uma ou ambas as imagens. Verifique os caminhos e tente novamente.")

    # Rodapé texto
    st.markdown("""
    <hr>
    <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
    </p>
    """, unsafe_allow_html=True)
