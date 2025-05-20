import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

st.title("⚖️ Princípios Básicos da LGPD")
st.markdown("---")
st.markdown("""
A LGPD estabelece 10 princípios que devem orientar todo tratamento de dados pessoais no IPEM-MG:
""")

st.subheader("1. Finalidade")
st.markdown("""
Realização do tratamento para propósitos legítimos, específicos, explícitos e informados ao titular.
""")

st.subheader("2. Adequação")
st.markdown("""
Compatibilidade do tratamento com as finalidades informadas ao titular.
""")

st.subheader("3. Necessidade")
st.markdown("""
Limitação do tratamento ao mínimo necessário para a realização de suas finalidades.
""")

st.subheader("4. Livre Acesso")
st.markdown("""
Garantia aos titulares de consulta facilitada e gratuita sobre a forma e a duração do tratamento.
""")

st.subheader("5. Qualidade dos Dados")
st.markdown("""
Garantia de exatidão, clareza, relevância e atualização dos dados.
""")

st.subheader("6. Transparência")
st.markdown("""
Garantia aos titulares de informações claras, precisas e facilmente acessíveis sobre o tratamento.
""")

st.subheader("7. Segurança")
st.markdown("""
Utilização de medidas técnicas e administrativas aptas a proteger os dados pessoais.
""")

st.subheader("8. Prevenção")
st.markdown("""
Adoção de medidas para prevenir a ocorrência de danos em virtude do tratamento de dados.
""")

st.subheader("9. Não Discriminação")
st.markdown("""
Impossibilidade de realização do tratamento para fins discriminatórios ilícitos ou abusivos.
""")

st.subheader("10. Responsabilização e Prestação de Contas")
st.markdown("""
Demonstração pelo agente da adoção de medidas eficazes capazes de comprovar o cumprimento das normas de proteção de dados.
""")

st.markdown("---")
st.info("""
Todos os processos do IPEM-MG que envolvem tratamento de dados pessoais devem observar estes princípios em todas as etapas.
""")
# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
