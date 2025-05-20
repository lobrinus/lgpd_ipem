import streamlit as st
from PIL import Image


def render()
from login_unificado import autenticar_usuario, registrar_usuario

    # Título principal
    st.title("🏠 Página Principal")
    st.markdown("---")
    
    # Seção: Introdução
    st.header("🔎 Sobre o Portal LGPD")
    st.markdown("""
    O Portal LGPD do Instituto de Metrologia e Qualidade do Estado de Minas Gerais (IPEM-MG) tem como objetivo garantir transparência, segurança e respeito aos direitos dos cidadãos no tratamento de dados pessoais.
    """)
    
    # Seção: Acesso Rápido
    st.header("🚀 Acesso Rápido")
    st.markdown("""
    Acesse os principais conteúdos do portal através do menu lateral:
    
    - 📜 Política de Privacidade  
    - 🔓 Solicitação de Acesso a Dados  
    - ⚖️ Princípios da LGPD  
    - ✅ Boas Práticas do IPEM-MG  
    - 👥 Painel do Cidadão  
    """)
    
    # Seção: O que é a LGPD
    st.header("📖 O que é a LGPD?")
    st.markdown("""
    A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) estabelece regras sobre coleta, uso, armazenamento e compartilhamento de dados pessoais, promovendo transparência e segurança.
    """)
    
    # Seção: Compromisso do IPEM-MG
    st.header("🔐 Compromisso do IPEM-MG")
    st.markdown("""
    O IPEM-MG trata dados pessoais apenas quando necessário para o cumprimento de obrigações legais e institucionais. Todas as operações seguem os princípios da LGPD.
    """)
    
    # Seção: Objetivos do Portal
    st.header("🎯 Objetivos do Portal")
    st.markdown("""
    - Facilitar o exercício dos direitos dos titulares de dados  
    - Centralizar informações institucionais sobre proteção de dados  
    - Divulgar documentos e boas práticas de conformidade  
    """)
    
    # Seção: Transparência Ativa
    st.header("📢 Transparência Ativa")
    st.markdown("""
    - 📄 Política de Privacidade disponível online  
    - 📋 Relatório de Impacto à Proteção de Dados (quando aplicável)  
    - 📚 Registros de tratamento e treinamentos internos  
    """)
    
    # Seção: Painel do Cidadão
    st.header("👥 Painel do Cidadão")
    st.markdown("""
    O Painel do Cidadão é a ferramenta digital que permite ao titular:
    
    - Registrar solicitações de acesso a dados  
    - Acompanhar o andamento de pedidos  
    - Visualizar respostas recebidas  
    """)
    
    # Seção: Canal para Reclamações
    st.header("🚨 Canal para Reclamações")
    st.markdown("""
    Caso você identifique uso indevido de seus dados pessoais, entre em contato:
    
    - 📧 E-mail: encarregado.data@ipem.mg.gov.br  
    - 📞 Telefone: (31) 3399-7100  
    - 🧾 Também disponível no Painel do Cidadão  
    """)
    
    # Seção: Últimas Atualizações
    st.header("🕓 Últimas Atualizações")
    st.markdown("""
    - 15/03/2025: Atualização da Política de Privacidade  
    - 01/04/2025: Treinamento para colaboradores  
    - 19/08/2020: Nomeação do Encarregado de Dados  
    """)
    
    # Seção: Contato
    st.header("📞 Contato do Encarregado de Dados")
    st.markdown("""
    - E-mail: encarregado.data@ipem.mg.gov.br  
    - Telefone: (31) 3399-7100  
    - Horário de atendimento: 8h às 18h (dias úteis)  
    """)
    
    # Rodapé
    st.markdown("""
    <hr>
    <div style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
    </div>
    """, unsafe_allow_html=True)
