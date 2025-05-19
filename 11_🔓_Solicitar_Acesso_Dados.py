import streamlit as st
from PIL import Image
from login import exibir_login

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

# Formas de Solicitação
st.markdown("""
- **E-mail:** [ecarregado.data@ipem.mg.gov.br](mailto:ecarregado.data@ipem.mg.gov.br)
- **Formulário Online:** [🔗 Clique aqui para preencher o formulário](#)
- **Presencialmente:** Na sede do IPEM-MG
""")

# Se o estado for ativado por clique no link simulado
if st.session_state.get("go_to_formulario", False):
    st.session_state["pagina_escolhida"] = "📧 Formulário LGPD"
    st.session_state["go_to_formulario"] = False
    st.rerun()

# Script para simular clique em link interno
st.markdown("""
<script>
const link = window.parent.document.querySelector('iframe')?.contentWindow.document.querySelector('a[href="#"]');
if (link) {
    link.addEventListener("click", function(e) {
        e.preventDefault();
        window.parent.postMessage({ type: "streamlit:setSessionState", key: "go_to_formulario", value: true }, "*");
    });
}
</script>
""", unsafe_allow_html=True)


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
