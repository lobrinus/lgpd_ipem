import streamlit as st
from login import exibir_login

st.set_page_config(
    page_title="O Que Fazer e Não Fazer - LGPD IPEM-MG",
    page_icon="✅❌"
)
exibir_login()
st.title("✅❌ O Que Fazer e Não Fazer")
st.markdown("---")
st.markdown("""
Guia rápido de condutas adequadas e inadequadas no tratamento de dados pessoais no IPEM-MG:
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ O Que Fazer")
    st.markdown("""
    - Coletar apenas dados necessários para a finalidade declarada
    - Manter os dados atualizados e precisos
    - Armazenar em ambiente seguro com acesso controlado
    - Excluir dados quando não forem mais necessários
    - Registrar todas as operações de tratamento
    - Comunicar incidentes ao Encarregado imediatamente
    - Usar canais seguros para compartilhar dados
    - Solicitar orientação em caso de dúvidas
    """)

with col2:
    st.subheader("❌ O Que Não Fazer")
    st.markdown("""
    - Coletar dados sem base legal ou consentimento
    - Manter dados além do tempo necessário
    - Armazenar em locais não autorizados (ex: pendrives)
    - Compartilhar dados sem verificar a necessidade
    - Enviar dados por e-mail não criptografado
    - Ignorar solicitações de titulares
    - Deixar sistemas desprotegidos ou sem senha
    - Tentar esconder violações ou incidentes
    """)

st.markdown("---")
st.subheader("Situações Comuns")
st.markdown("""
**Recebimento de solicitação de titular:**
✅ Encaminhar imediatamente ao Encarregado  
❌ Tentar resolver por conta própria ou ignorar

**Identificação de dado desatualizado:**
✅ Atualizar ou marcar para correção  
❌ Manter o dado incorreto no sistema

**Necessidade de compartilhar dados com terceiro:**
✅ Verificar contrato/cláusula de proteção  
❌ Enviar sem medidas de segurança adequadas

**Descoberta de violação:**
✅ Comunicar imediatamente ao DPO  
❌ Tentar resolver sem registro ou tentar esconder
""")

# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
