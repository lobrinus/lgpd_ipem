import streamlit as st
from login import exibir_login


st.title("🔍 Orientação sobre Dados Pessoais")
st.markdown("---")
st.markdown("""
Esta seção fornece orientações sobre como identificar, classificar e tratar dados pessoais no âmbito do IPEM-MG.
""")

st.subheader("O que são Dados Pessoais?")
st.markdown("""
De acordo com a LGPD, **dado pessoal** é qualquer informação relacionada a pessoa natural identificada ou identificável.

**Exemplos no IPEM-MG:**
- Nome completo
- CPF
- Endereço residencial
- E-mail institucional
- Histórico funcional
- Registros de acesso a sistemas
""")

st.subheader("Dados Pessoais Sensíveis")
st.markdown("""
São dados sobre:
- Origem racial ou étnica
- Convicção religiosa
- Opinião política
- Filiação a sindicato ou organização religiosa, filosófica ou política
- Dado referente à saúde ou à vida sexual
- Dado genético ou biométrico

**Tratamento especial:** Exigem medidas de proteção reforçadas e só podem ser tratados em situações específicas previstas em lei.
""")

st.subheader("Dados Anonimizados")
st.markdown("""
Dados que não podem ser associados a um indivíduo, considerando o uso de meios técnicos razoáveis e disponíveis.

**Importante:** A anonimização deve ser irreversível para que os dados deixem de ser considerados pessoais.
""")

st.subheader("Como Identificar Dados Pessoais")
st.markdown("""
1. Verifique se a informação se refere a uma pessoa natural
2. Avalie se é possível identificar a pessoa direta ou indiretamente
3. Considere o contexto e a combinação com outros dados
4. Em caso de dúvida, trate como dado pessoal
""")

st.markdown("---")
st.warning("""
**Atenção:** Todo tratamento de dados pessoais no IPEM-MG deve ser registrado no Inventário de Dados Pessoais e ter base legal adequada.
""")

# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
