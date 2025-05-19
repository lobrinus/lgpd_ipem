import streamlit as st
from PIL import Image
from login import exibir_login
import streamlit.components.v1 as components

# CSS global e botão de login customizado
st.markdown("""
    <style>
    /* Marca d'água */
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.2;
        z-index: -1;
    }

    /* Botão de login no canto superior direito */
    .login-button-container {
        position: absolute;
        top: 20px;
        right: 30px;
        z-index: 9999;
    }

    .login-button {
        padding: 8px 16px;
        background-color: #0e1117;
        color: white;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .login-button:hover {
        background-color: #4a4a4a;
    }

    .login-button:active {
        background-color: #6a6a6a;
    }

    /* Botão estilo link */
    .link-button {
        background: none;
        color: #0066cc;
        border: none;
        padding: 0;
        font-size: 1em;
        text-decoration: underline;
        cursor: pointer;
    }

    .link-button:hover {
        color: #004080;
    }
    </style>

    <!-- Botão de login -->
    <div class="login-button-container">
        <a href="/login" class="login-button">Login</a>
    </div>

    <!-- Marca d'água -->
    <div class="watermark">
        <img src="ipem_mg.png" width="200">
    </div>
""", unsafe_allow_html=True)

# Logo e título
logo_ipem = Image.open('ipem_mg.png')
st.image(logo_ipem, width=150)
st.title("🔓 Solicitar Acesso a Dados Pessoais")
st.markdown("---")

# Seção 1 — Direitos
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
""")

st.markdown("### 2. Formas de Solicitação")
st.markdown("- **E-mail:** [ecarregado.data@ipem.mg.gov.br](mailto:ecarregado.data@ipem.mg.gov.br)")

# Botão estilo link
st.write("- **Formulário Online:**", end=" ")
if st.button("🔗 Clique aqui para preencher o formulário", key="formulario_link", help="Abrir formulário"):
    st.session_state["pagina_escolhida"] = "📧 Formulário LGPD"
    st.rerun()

st.markdown("- **Presencialmente:** Na sede do IPEM-MG")

# Seção 3 — Informações necessárias
st.markdown("""
### 3. Informações Necessárias
Para agilizar seu atendimento, inclua na solicitação:
- Seu nome completo
- CPF
- Descrição clara do direito que deseja exercer
- Período ou contexto dos dados solicitados
""")

# Prazo
st.markdown("---")
st.subheader("Prazo de Resposta")
st.markdown("""
O IPEM-MG responderá sua solicitação em até **15 dias**, prorrogáveis por mais 15 dias mediante justificativa, conforme determina a LGPD.
""")

# Contato
st.markdown("---")
st.info("""
**Dúvidas?** Entre em contato com nosso Encarregado de Dados:  
📧 encarregado.data@ipem.mg.gov.br | 📞 (31) 3399-7100
""")

# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
