import streamlit as st
from PIL import Image
from login_unificado import autenticar_usuario, registrar_usuario

# CSS global
st.markdown("""
<style>
.policy-container {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.section-title {
    color: #2b5876;
    border-bottom: 2px solid #2b5876;
    padding-bottom: 0.5rem;
    margin-top: 1.5rem;
}
.finalidade-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid #2b5876;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.finalidade-card:hover {
    transform: translateX(5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    background-color: #e9f5ff;
}
.finalidade-title {
    color: #2b5876;
    font-weight: bold;
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.details-content {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 0.8rem;
    border: 1px solid #e1e4e8;
}
.info-box {
    background-color: #f0f9ff;
    border-left: 4px solid #2b5876;
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# Marca d'água e botão de login
st.markdown("""
    <div style="position: absolute; top: 20px; right: 30px; z-index: 9999;">
        <a href="/login" style="padding: 8px 16px; background-color: #0e1117; color: white; border: 1px solid #4a4a4a; border-radius: 5px; text-decoration: none; font-weight: bold;">Login</a>
    </div>
    <div style="position: fixed; bottom: 10px; right: 10px; opacity: 0.2; z-index: -1;">
        <img src="ipem_mg.png" width="200">
    </div>
""", unsafe_allow_html=True)

# Logo e título
logo_ipem = Image.open('ipem_mg.png')
st.image(logo_ipem, width=150)
st.title("🔓 Solicitar Acesso a Dados Pessoais")
st.markdown("---")

# Introdução
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Como solicitar acesso aos seus dados pessoais </h2>
    <p> No IPEM-MG, você pode exercer seus direitos como titular de dados pessoais através das opções a seguir: </p>
</div>
""", unsafe_allow_html=True)

# Direitos do Titular
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📑 Direitos do Titular</div>
    <p>De acordo com a LGPD, você tem direito a:</p>
    <details>
        <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">📌 Ver detalhes</summary>
        <div class="details-content">
            <ul>
                <li>Confirmar a existência de tratamento</li>
                <li>Acessar seus dados</li>
                <li>Corrigir dados incompletos ou inexatos</li>
                <li>Solicitar anonimização, bloqueio ou eliminação de dados quando aplicável</li>
                <li>Revogar consentimento quando aplicável</li>
                <li>Obter informações sobre compartilhamento</li>
            </ul>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)

# E-mail
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📧 Solicitação por E-mail</div>
    <p>Você pode enviar sua solicitação diretamente por e-mail:</p>
    <p><strong>encarregado.data@ipem.mg.gov.br</strong></p>
    <details>
        <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">📌 Como fazer</summary>
        <div class="details-content">
            <p>Envie um e-mail com as seguintes informações:</p>
            <ul>
                <li>Nome completo</li>
                <li>CPF ou CNPJ</li>
                <li>Telefone de contato</li>
                <li>Descrição clara do direito que deseja exercer</li>
                <li>Período ou contexto dos dados solicitados</li>
            </ul>
            <p>Você receberá uma resposta dentro do prazo legal.</p>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)

# Formulário Online
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🌐 Solicitação pelo Formulário Online</div>
    <p>Você também pode utilizar o Painel do Cidadão.</p>
    <details>
        <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">📌 Como fazer</summary>
        <div class="details-content">
            <ol>
                <li>Acesse o site e clique na aba <strong>Painel do Cidadão</strong></li>
                <li>Crie sua conta e faça o login</li>
                <li>Após o login, clique na aba <strong>Formulário LGPD</strong></li>
                <li>Preencha os dados solicitados e envie</li>
            </ol>
            <p>A resposta será enviada dentro do prazo legal e poderá ser visualizada diretamente no Painel do Cidadão.</p>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)

# Presencial
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🏢 Solicitação Presencial</div>
    <p>Você pode comparecer pessoalmente à sede do IPEM-MG.</p>
    <details>
        <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">📌 Como fazer</summary>
        <div class="details-content">
            <p>Leve um documento oficial com foto e informe sua solicitação diretamente ao atendente responsável.</p>
            <p>O atendimento será registrado e processado conforme a LGPD.</p>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)

# Prazo
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">⏱️ Prazo de Resposta</div>
    <p>O IPEM-MG responderá sua solicitação em até <strong>15 dias</strong>, prorrogáveis por mais 15 dias mediante justificativa, conforme determina a LGPD.</p>
</div>
""", unsafe_allow_html=True)

# Contato
st.markdown("""
<div class="info-box">
    <p><strong>Dúvidas?</strong> Entre em contato com nosso Encarregado de Dados:</p>
    <p>📧 <strong>encarregado.data@ipem.mg.gov.br</strong> | 📞 <strong>(31) 3399-7100</strong></p>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("""
<hr>
<div style="text-align: center; color: gray;">
    <p>© 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.</p>
</div>
""", unsafe_allow_html=True)
