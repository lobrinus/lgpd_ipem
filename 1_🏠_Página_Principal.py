import streamlit as st
from PIL import Image
from login import exibir_login

# Título e introdução
st.title("🏠 Página Principal")
st.markdown("---")
st.markdown("""
**Bem-vindo ao Portal LGPD do IPEM-MG**

Este portal centraliza todas as informações sobre a aplicação da Lei Geral de Proteção de Dados no Instituto de Pesos e Medidas do Estado de Minas Gerais.
""")

# Bloco com destaques
st.markdown("""
<div class="info-box">
    <h4>📌 Acesso Rápido:</h4>
    <ul>
        <li><a href="/Política_de_Privacidade" target="_self">📜 Política de Privacidade</a></li>
        <li><a href="/Solicitar_Acesso_Dados" target="_self">🔓 Solicitar Acesso a Dados</a></li>
        <li><a href="/Princípios_Básicos" target="_self">⚖️ Princípios da LGPD</a></li>
        <li><a href="/Boas_Práticas" target="_self">✅ Boas Práticas no IPEM-MG</a></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Bloco: O que é a LGPD
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">📖 O que é a LGPD?</div>
    <p>A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) estabelece regras sobre coleta, uso, armazenamento e compartilhamento de dados pessoais no Brasil, promovendo transparência, segurança e respeito à privacidade dos cidadãos.</p>
</div>
""", unsafe_allow_html=True)

# Bloco: Compromisso do IPEM-MG
st.markdown("""
<div class="finalidade-card">
    <div class="finalidade-title">🔐 Compromisso com a Privacidade</div>
    <p>O IPEM-MG está comprometido com a proteção dos dados pessoais tratados em suas atividades. Implementamos medidas administrativas, técnicas e organizacionais para garantir segurança, transparência e respeito à legislação.</p>
</div>
""", unsafe_allow_html=True)

# Bloco: Painel do Cidadão
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

# Bloco: Últimas Atualizações
st.subheader("🕓 Últimas Atualizações")
st.markdown("""
- **15/03/2025:** Atualização da Política de Privacidade  
- **01/04/2025:** Realização de treinamento para colaboradores  
- **19/08/2020:** Nomeação do Encarregado de Dados  
""")

# Bloco: Contato do Encarregado
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
