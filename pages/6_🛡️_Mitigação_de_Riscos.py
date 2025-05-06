import streamlit as st

st.set_page_config(
    page_title="Mitigação de Riscos - LGPD IPEM-MG",
    page_icon="🛡️"
)

st.title("🛡️ Mitigação de Riscos")
st.markdown("---")
st.markdown("""
O IPEM-MG adota as seguintes medidas para mitigar riscos relacionados à proteção de dados pessoais:
""")

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

# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)

st.markdown("---")
st.warning("""
**Importante:** Todo incidente envolvendo dados pessoais deve ser imediatamente comunicado ao Encarregado de Dados.
""")
