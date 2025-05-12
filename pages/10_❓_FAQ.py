import streamlit as st

st.set_page_config(
    page_title="FAQ - LGPD IPEM-MG",
    page_icon="❓"
)

st.title("❓ Perguntas Frequentes")
st.markdown("---")

st.subheader("1. O que é a LGPD?")
st.markdown("""
A Lei Geral de Proteção de Dados (LGPD) é a legislação brasileira que regula as atividades de tratamento de dados pessoais. Ela estabelece direitos para os titulares de dados e obrigações para as organizações que coletam e processam esses dados.
""")

st.subheader("2. O IPEM-MG está em conformidade com a LGPD?")
st.markdown("""
Sim, o IPEM-MG adotou uma série de medidas para garantir a conformidade com a LGPD, incluindo a nomeação de um Encarregado de Dados, a elaboração de políticas internas, a realização de treinamentos e a implementação de medidas técnicas de segurança.
""")

st.subheader("3. Como posso solicitar acesso aos meus dados pessoais?")
st.markdown("""
Você pode enviar uma solicitação para o Encarregado de Dados do IPEM-MG pelo e-mail dpo@ipem.mg.gov.br, informando seu nome completo, CPF e detalhes sobre os dados que deseja acessar.
""")

st.subheader("4. Quanto tempo o IPEM-MG tem para responder a uma solicitação?")
st.markdown("""
O prazo legal é de 15 dias, prorrogável por mais 15 dias mediante justificativa. O IPEM-MG se esforça para responder todas as solicitações no menor prazo possível.
""")

st.subheader("5. O que fazer em caso de vazamento de dados?")
st.markdown("""
Caso identifique ou suspeite de um vazamento de dados pessoais tratados pelo IPEM-MG, entre em contato imediatamente com o Encarregado de Dados pelo e-mail encarregado.data@ipem.mg.gov.br ou pelo telefone (31) 3399-7100
""")

st.subheader("6. Posso solicitar a exclusão dos meus dados?")
st.markdown("""
Sim, em alguns casos. A LGPD permite a exclusão de dados tratados com base no consentimento. Para dados tratados com outras bases legais (como cumprimento de obrigação legal), a exclusão pode não ser possível, mas você será informado sobre as razões.
""")

st.subheader("7. Como o IPEM-MG protege meus dados?")
st.markdown("""
Adotamos diversas medidas de segurança, incluindo:
- Controle rigoroso de acesso
- Criptografia de dados sensíveis
- Monitoramento contínuo de sistemas
- Treinamento de colaboradores
- Políticas e procedimentos claros
""")

st.markdown("---")
st.info("""
**Não encontrou sua dúvida?** Entre em contato com nosso Encarregado de Dados: encarregado.data@ipem.mg.gov.br
""")
# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
