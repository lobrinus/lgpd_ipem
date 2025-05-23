import streamlit as s
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.markdown("""
    <h1 style='text-align: center;'>🛡️ Mitigação de Riscos</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
        
    st.subheader("1. Avaliação de Riscos")
    st.markdown("""
    - **Identificação de ativos:** Sistemas, bancos de dados e processos que tratam dados pessoais
    - **Classificação de dados:** Por nível de sensibilidade e criticidade
    - **Análise de vulnerabilidades:** Pontos fracos que podem ser explorados
    - **Avaliação de impacto:** Consequências potenciais de violações
    """)
    
    st.subheader("2. Medidas de Proteção")
    st.markdown("""
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
    
    st.subheader("3. Monitoramento e Melhoria")
    st.markdown("""
    - Auditorias regulares de conformidade
    - Análise contínua de logs e acessos
    - Atualização periódica de medidas de segurança
    - Revisão de políticas conforme mudanças legais
    """)
    
    st.subheader("4. Plano de Resposta a Incidentes")
    st.markdown("""
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
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
