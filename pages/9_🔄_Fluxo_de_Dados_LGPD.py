import streamlit as st

st.set_page_config(
    page_title="Fluxo de Dados - LGPD IPEM-MG",
    page_icon="🔄"
)

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

st.markdown("---")
st.image("https://miro.medium.com/v2/resize:fit:1400/1*_NVB4dmR1Q0aJv2B1H_o3Q.png", caption="Exemplo de Fluxo de Dados Pessoais", width=600)