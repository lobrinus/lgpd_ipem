import streamlit as st
from PIL import Image
from login import exibir_login

st.title("🏠 Página Principal")
st.markdown("---")

st.markdown("""
**Bem-vindo ao Portal LGPD do IPEM-MG**

Este portal centraliza todas as informações sobre a aplicação da Lei Geral de Proteção de Dados no Instituto de Metrologia e Qualidade do Estado de Minas Gerais (IPEM-MG).
""")

# Acesso rápido (sem links)
st.markdown("""
<div class="info-box">
    <h4>📌 Acesso Rápido:</h4>
    <ul>
        <li>📜 Política de Privacidade — disponível no menu lateral</li>
        <li>🔓 Solicitar Acesso a Dados — disponível no menu lateral</li>
        <li>⚖️ Princípios da LGPD — disponível no menu lateral</li>
        <li>✅ Boas Práticas no IPEM-MG — disponível no menu lateral</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# O que é LGPD
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📖 O que é a LGPD?</div>
    <p>A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) estabelece regras sobre coleta, uso, armazenamento e compartilhamento de dados pessoais no Brasil, promovendo transparência, segurança e respeito à privacidade dos cidadãos.</p>
</div>
""", unsafe_allow_html=True)

# Objetivo do Portal
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🎯 Objetivo do Portal</div>
    <p>O Portal LGPD foi criado para garantir transparência e facilitar o exercício dos direitos dos titulares de dados no âmbito do IPEM-MG. Aqui, você encontrará informações, orientações e ferramentas para interagir com segurança e clareza com a administração pública.</p>
</div>
""", unsafe_allow_html=True)

# Sobre o IPEM-MG
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🏛️ Sobre o IPEM-MG</div>
    <p>O Instituto de Metrologia e Qualidade do Estado de Minas Gerais (IPEM-MG) é responsável pela execução das atividades de metrologia legal, fiscalização de produtos regulamentados e certificações no Estado, sempre com foco na proteção do consumidor e da livre concorrência.</p>
</div>
""", unsafe_allow_html=True)

# Responsabilidades LGPD
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📂 Responsabilidades na Proteção de Dados</div>
    <p>O IPEM-MG realiza o tratamento de dados pessoais apenas quando necessário para o cumprimento de suas funções legais. Todas as operações seguem os princípios da LGPD, com especial atenção à segurança, finalidade e necessidade dos dados tratados.</p>
</div>
""", unsafe_allow_html=True)

# Painel do Cidadão
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">👥 Painel do Cidadão</div>
    <p>Por meio do <strong>Painel do Cidadão</strong>, você pode:</p>
    <ul>
        <li>Enviar solicitações sobre seus dados pessoais</li>
        <li>Acompanhar o andamento da resposta</li>
        <li>Visualizar respostas já recebidas</li>
    </ul>
    <p>Acesse a aba no menu lateral, crie sua conta e exerça seus direitos garantidos pela LGPD.</p>
</div>
""", unsafe_allow_html=True)

# Transparência Ativa
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📢 Transparência Ativa</div>
    <p>Documentos e informações públicas sobre a LGPD no IPEM-MG:</p>
    <ul>
        <li>📄 Política de Privacidade</li>
        <li>📋 Relatório de Impacto à Proteção de Dados (quando disponível)</li>
        <li>📚 Registros de atividades de tratamento</li>
        <li>🧑‍🏫 Treinamentos internos sobre LGPD</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Canal de Reclamações
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🚨 Canal para Reclamações</div>
    <p>Se você acredita que seus dados foram utilizados indevidamente, entre em contato:</p>
    <ul>
        <li>📧 <strong>E-mail:</strong> encarregado.data@ipem.mg.gov.br</li>
        <li>📞 <strong>Telefone:</strong> (31) 3399-7100</li>
        <li>🧾 Também disponível no Painel do Cidadão</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Últimas atualizações
st.subheader("🕓 Últimas Atualizações")
st.markdown("""
- **15/03/2025:** Atualização da Política de Privacidade  
- **01/04/2025:** Realização de treinamento para colaboradores  
- **19/08/2020:** Nomeação do Encarregado de Dados  
""")

# Contato
st.subheader("📞 Contato do Encarregado de Dados")
st.markdown("""
**E-mail:** encarregado.data@ipem.mg.gov.br  
**Telefone:** (31) 3399-7100  
**Horário de atendimento:** 8h às 18h (dias úteis)
""")

# Rodapé
st.markdown("""
<hr>
<div style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</div>
""", unsafe_allow_html=True)
