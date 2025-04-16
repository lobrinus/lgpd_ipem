import streamlit as st

st.set_page_config(
    page_title="Boas Práticas - LGPD IPEM-MG",
    page_icon="✅"
)

st.title("✅ Boas Práticas no IPEM-MG")
st.markdown("---")
st.markdown("""
O IPEM-MG adota as seguintes boas práticas para garantir a conformidade com a LGPD:
""")

st.subheader("1. Gestão de Dados Pessoais")
st.markdown("""
- **Inventário de dados:** Mapeamento completo de todos os dados pessoais tratados
- **Classificação de dados:** Identificação de dados sensíveis e críticos
- **Limitação de acesso:** Princípio do menor privilégio
""")

st.subheader("2. Segurança da Informação")
st.markdown("""
- **Criptografia:** Para dados em trânsito e em repouso
- **Controle de acesso:** Autenticação forte e logs detalhados
- **Backup seguro:** Com políticas de retenção definidas
""")

st.subheader("3. Capacitação e Conscientização")
st.markdown("""
- **Treinamentos regulares:** Para todos os colaboradores
- **Comunicação clara:** Orientações sobre tratamento adequado
- **Cultura de privacidade:** Incentivo à proteção de dados
""")

st.subheader("4. Transparência")
st.markdown("""
- **Política de privacidade clara:** Disponível no site institucional
- **Canais de comunicação:** Para dúvidas e solicitações de titulares
- **Registro de operações:** Documentação dos tratamentos realizados
""")

st.markdown("---")
st.subheader("Checklist de Boas Práticas")
st.checkbox("Realizar apenas o tratamento necessário para a finalidade declarada")
st.checkbox("Manter os dados atualizados e precisos")
st.checkbox("Armazenar os dados apenas pelo tempo necessário")
st.checkbox("Garantir a segurança dos dados contra acessos não autorizados")
st.checkbox("Documentar todas as operações de tratamento de dados")