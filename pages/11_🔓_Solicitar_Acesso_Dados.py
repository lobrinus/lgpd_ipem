import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Solicitar Acesso a Dados - LGPD IPEM-MG",
    page_icon="🔓"
)

# CSS e marca d'água
st.markdown("""
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.2;
        z-index: -1;
    }
    </style>
    <div class="watermark"><img src="ipem_mg.png" width="200"></div>
""", unsafe_allow_html=True)

# Logo e título
logo_ipem = Image.open('ipem_mg.png')
st.image(logo_ipem, width=150)
st.title("🔓 Solicitar Acesso a Dados Pessoais")
st.markdown("---")

# Conteúdo
st.markdown("""
## Como solicitar acesso aos seus dados pessoais

No IPEM-MG, você pode exercer seus direitos como titular de dados pessoais da seguinte forma:

### 1. Direitos do Titular
De acordo com a LGPD, você tem direito a:
- Confirmar a existência de tratamento
- Acessar seus dados
- Corrigir dados incompletos ou inexatos
- Solicitar anonimização, bloqueio ou eliminação de dados desde que não sejam necessários para o tratamento
- Revogar o consentimento desde que não haja outra base legal para o tratamento
- Solicitar informações sobre o compartilhamento de seus dados com terceiros

### 2. Formas de Solicitação
Você pode fazer sua solicitação através de:
- **E-mail:** ouvidoria@ipem.mg.gov.br
- **Formulário Online:** [Acesse aqui]()
- **Presencialmente:** Na sede do IPEM-MG

### 3. Informações Necessárias
Para agilizar seu atendimento, inclua na solicitação:
- Seu nome completo
- CPF
- Descrição clara do direito que deseja exercer
- Período ou contexto dos dados solicitados
""")

st.markdown("---")
st.subheader("Prazo de Resposta")
st.markdown("""
O IPEM-MG responderá sua solicitação em até **15 dias**, prorrogáveis por mais 15 dias mediante justificativa, conforme determina a LGPD.
""")

st.markdown("---")
st.info("""
**Dúvidas?** Entre em contato com nosso Encarregado de Dados:  
📧 ouvidoria@ipem.mg.gov.br | 📞 (31) 3399-7100
""")