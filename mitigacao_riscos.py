import streamlit as st

def render_header():
    st.markdown(
        "<h1 style='text-align: center;'>🛡️ Mitigação de Riscos</h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")

def render_section(title, content):
    st.subheader(title)
    st.markdown(content)

def render_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; margin-top: 40px;">
            © 2025 IPEM-MG. Todos os direitos reservados.<br>
            R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
            CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
        </div>
        """,
        unsafe_allow_html=True
    )

def render():
    render_header()
    render_section("1. Avaliação de Riscos", """
    - **Identificação de ativos:** Sistemas, bancos de dados e processos que tratam dados pessoais
    - **Classificação de dados:** Por nível de sensibilidade e criticidade
    - **Análise de vulnerabilidades:** Pontos fracos que podem ser explorados
    - **Avaliação de impacto:** Consequências potenciais de violações
    """)
    render_section("2. Medidas de Proteção", """
    **Técnicas:**
    - Criptografia de dados sensíveis
    - Controle de acesso baseado em função (RBAC)
    - Monitoramento contínuo de sistemas
    - Backup seguro e teste de recuperação

    **Administrativas:**
    - Políticas e procedimentos claros
    - Treinamento regular de colaboradores
    - Contratos com terceiros com cláusulas de proteção
    - Plano de resposta a incidentes
    """)
    render_section("3. Monitoramento e Melhoria", """
    - Auditorias regulares de conformidade
    - Análise contínua de logs e acessos
    - Atualização periódica de medidas de segurança
    - Revisão de políticas conforme mudanças legais
    """)
    render_section("4. Plano de Resposta a Incidentes", """
    **Etapas:**
    1. **Identificação:** Detecção do incidente
    2. **Contenção:** Limitação do dano
    3. **Análise:** Determinação de causa e extensão
    4. **Eradicação:** Eliminação da causa
    5. **Recuperação:** Retorno à normalidade
    6. **Lições aprendidas:** Melhorias para evitar recorrência

    **Comunicação:** Notificação à ANPD e titulares quando necessário
    """)
    st.markdown("---")
    st.warning("""
    **Importante:** Todo incidente envolvendo dados pessoais deve ser imediatamente comunicado ao Encarregado de Dados.
    """)
    render_footer()
