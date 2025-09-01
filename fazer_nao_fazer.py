import streamlit as st

def render():
    st.markdown("""
    <h1 style='text-align: center;'>✅ O Que Fazer e Não Fazer ❌</h1>
    """, unsafe_allow_html=True)
    st.markdown("---") 
    
    # Seção Principal de Do's and Don'ts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ O Que Fazer")
        st.markdown("""
        - **Bloqueie o computador** sempre que se ausentar da sua mesa.
        - **Use senhas fortes**, com letras, números e símbolos.
        - **Guarde documentos físicos** em gavetas ou armários trancados.
        - **Retire impressões** da impressora imediatamente.
        - **Use apenas o e-mail institucional** para trabalho.
        - **Contate o setor de TI** em caso de e-mail suspeito (phishing).
        - **Use canais seguros** para compartilhar dados.
        - **Compartilhe dados apenas com autorização** e real necessidade.
        """)
    
    with col2:
        st.subheader("❌ O Que Não Fazer")
        st.markdown("""
        - **Coletar dados** sem base legal ou finalidade clara.
        - **Manter dados** além do tempo necessário para a finalidade.
        - **Armazenar em locais não autorizados** (Ex: pendrives pessoais).
        - **Compartilhar dados** sem verificar a real necessidade.
        - **Enviar dados sensíveis** por meios não seguros.
        - **Ignorar solicitações** de titulares de dados.
        - **Deixar sistemas desprotegidos** ou sem senha.
        - **Tentar esconder** violações ou incidentes de segurança.
        """)
    
    st.markdown("---")
    st.subheader("Situações Comuns do Dia a Dia")

    # Nova seção de Situações Comuns com duas colunas
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        #### ✅ Ações Corretas
        
        **Ao receber uma solicitação de titular:**
        - Encaminhar imediatamente ao Encarregado (DPO).

        **Ao identificar um dado desatualizado:**
        - Atualizar ou solicitar a correção no sistema.

        **Ao precisar compartilhar dados com terceiro:**
        - Verificar se o contrato possui cláusula de proteção de dados.

        **Ao descobrir uma violação de dados:**
        - Comunicar imediatamente ao Encarregado (DPO).
        """)

    with col4:
        st.markdown("""
        #### ❌ Ações Incorretas
        
        **Ao receber uma solicitação de titular:**
        - Tentar resolver por conta própria ou ignorar.

        **Ao identificar um dado desatualizado:**
        - Manter o dado incorreto no sistema.

        **Ao precisar compartilhar dados com terceiro:**
        - Enviar sem medidas de segurança adequadas.

        **Ao descobrir uma violação de dados:**
        - Tentar resolver sem registro ou esconder o fato.
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
