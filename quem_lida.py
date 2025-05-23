import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.markdown("""
    <h1 style='text-align: center;'>❓ FAQ - Perguntas Frequentes</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    A LGPD define diferentes papéis e responsabilidades no tratamento de dados pessoais. No IPEM-MG, essas funções estão assim distribuídas:
    """)
    
    st.subheader("Controlador de Dados")
    st.markdown("""
    **Definição:** Pessoa natural ou jurídica que toma as decisões sobre o tratamento de dados pessoais.
    
    **No IPEM-MG:** O próprio Instituto, representado por sua alta administração, é o controlador dos dados tratados em suas atividades.
    
    **Responsabilidades:**
    - Definir as finalidades do tratamento
    - Garantir a conformidade com a LGPD
    - Responder por eventuais violações
    - Indicar o Encarregado de Dados
    """)
    
    st.subheader("Operador de Dados")
    st.markdown("""
    **Definição:** Pessoa que realiza o tratamento em nome do controlador.
    
    **No IPEM-MG:** São os colaboradores, setores e sistemas que processam dados sob as diretrizes do Instituto.
    
    **Responsabilidades:**
    - Seguir as instruções do controlador
    - Manter a segurança dos dados
    - Comunicar incidentes
    - Auxiliar na conformidade
    """)
    
    st.subheader("Encarregado de Dados (DPO)")
    st.markdown("""
    **Definição:** Intermediador entre controlador, titulares e ANPD.
    
    **No IPEM-MG:** [Nome do Encarregado], designado por portaria.
    
    **Atribuições:**
    - Aceitar reclamações de titulares
    - Prestar esclarecimentos
    - Orientar colaboradores
    - Comunicar-se com a ANPD
    """)
    
    st.subheader("Titular de Dados")
    st.markdown("""
    **Definição:** Pessoa natural a quem se referem os dados pessoais.
    
    **No IPEM-MG:** Podem ser:
    - Servidores e colaboradores
    - Usuários de serviços
    - Fornecedores e parceiros
    - Cidadãos em geral que interagem com o Instituto
    
    **Direitos:**
    - Acesso, correção e eliminação de dados
    - Portabilidade
    - Revogação de consentimento
    - Oposição a tratamentos
    """)
    
    st.markdown("---")
    st.info("""
    **Contato do Encarregado: encarregado.data@ipem.mg.gov.br | (31) 3399-7100
    Horário de atendimento: 08:00 às 17:00 (exceto feriados)**""")
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335<br>
        <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.
    </p>
    </div>
    """, unsafe_allow_html=True)
