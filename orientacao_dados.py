import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.markdown("""
    <h1 style='text-align: center;'>🔍 Orientação sobre Dados Pessoais</h1>
    """, unsafe_allow_html=True)
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
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
