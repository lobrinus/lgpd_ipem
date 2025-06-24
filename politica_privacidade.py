import streamlit as st

def render():
    st.markdown("""
    <style>
    /* CSS Unificado e Adaptativo para Dark Mode */

    /* ----- Contêineres e Cards Principais ----- */
    .policy-container, .finalidade-card, .details-content, .info-box {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .finalidade-card {
        border-left: 4px solid #0d6efd; /* Azul como cor de destaque */
        transition: all 0.3s ease;
    }

    .finalidade-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }

    .info-box {
        border-left: 4px solid #0d6efd; /* Azul como cor de destaque */
        padding: 1em;
        margin: 1em 0;
        border-radius: 0 10px 10px 0;
    }

    /* ----- Títulos ----- */
    h1 {
        color: var(--text-color) !important;
    }
    .section-title {
        color: var(--text-color);
        border-bottom: 2px solid #0d6efd;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }

    .finalidade-title {
        color: var(--text-color);
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ----- Tabela ----- */
    table {
        width: 100%;
        border-collapse: collapse;
        color: var(--text-color);
    }
    th, td {
        border: 1px solid #4F4F4F; /* Borda neutra */
        padding: 8px;
        text-align: center;
    }
    th {
        background-color: #0d6efd; /* Azul para o cabeçalho */
        color: white;
    }
    td {
        background-color: var(--background-color); /* Fundo principal da página */
    }

    /* ----- Timeline ----- */
    .timeline {
        position: relative;
        max-width: 1000px;
        margin: 0 auto;
    }
    .timeline::after {
        content: '';
        position: absolute;
        width: 6px;
        background-color: #0d6efd; /* Azul para a linha da timeline */
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -3px;
    }
    .timeline-container { /* Renomeado de .container para evitar conflitos com Streamlit */
        padding: 10px 40px;
        position: relative;
        background-color: inherit;
        width: 50%;
    }
    .timeline-container.left {
        left: 0;
    }
    .timeline-container.right {
        left: 50%;
    }
    .date {
        padding: 5px;
        background: #0d6efd; /* Azul para a data */
        color: white;
        position: absolute;
        top: 15px;
        width: 100px;
        text-align: center;
        border-radius: 6px;
        z-index: 1;
    }
    .left .date {
        right: -120px;
    }
    .right .date {
        left: -120px;
    }
    .timeline-content { /* Renomeado de .content */
        padding: 20px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        position: relative;
        border-radius: 6px;
        border: 1px solid #4F4F4F;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>📜 Política de Privacidade</h1>", unsafe_allow_html=True)
    st.markdown("---")

    aba1, aba2, aba3 = st.tabs(["📑 Base Legal", "📖 Glossário", "⏳ Linha do Tempo"])

    with aba1:
        st.subheader("📑 Base Legal Aplicável")
        st.markdown("""
        <table>
          <tr>
            <th>Tipo de Dado</th>
            <th>Finalidade</th>
            <th>Base Legal</th>
          </tr>
          <tr>
            <td>Nome Completo, CPF, RG</td>
            <td>Identificação do Cidadão</td>
            <td>Obrigação Legal</td>
          </tr>
          <tr>
            <td>Email, Telefone</td>
            <td>Contato para Suporte e Informações</td>
            <td>Consentimento</td>
          </tr>
          <tr>
            <td>Endereço</td>
            <td>Envio de Documentos Físicos</td>
            <td>Execução de Políticas Públicas</td>
          </tr>
          <tr>
            <td>Dados de Acesso (IP, Logs)</td>
            <td>Garantia da Segurança e Auditoria</td>
            <td>Legítimo Interesse</td>
          </tr>
        </table>
        <p style='text-align: center; font-style: italic; margin-top: 1rem;'>
        De acordo com o art. 7º, incisos I ao X, e caput do art. 23 da LGPD.
        </p>
        """, unsafe_allow_html=True)

    with aba2:
        st.subheader("📖 Glossário LGPD")
        with st.expander("📌 **Dado Pessoal**"):
            st.markdown("Informação relacionada a pessoa natural identificada ou identificável.")
        with st.expander("📌 **Dado Sensível**"):
            st.markdown("Informação sobre origem racial ou étnica, convicção religiosa, opinião política, saúde, vida sexual, dado genético ou biométrico.")
        with st.expander("📌 **Titular dos Dados**"):
            st.markdown("Pessoa natural a quem se referem os dados pessoais que são objeto de tratamento.")
        with st.expander("📌 **Controlador**"):
            st.markdown("Pessoa natural ou jurídica, de direito público ou privado, a quem competem as decisões referentes ao tratamento de dados pessoais.")
        with st.expander("📌 **Operador**"):
            st.markdown("Pessoa natural ou jurídica que realiza o tratamento de dados pessoais em nome do controlador.")
        with st.expander("📌 **Encarregado (DPO)**"):
            st.markdown("Pessoa indicada pelo controlador para atuar como canal de comunicação entre o controlador, os titulares dos dados e a ANPD.")
        with st.expander("📌 **Anonimização**"):
            st.markdown("Utilização de meios técnicos razoáveis para remover elementos que permitam a identificação de um titular dos dados.")
        with st.expander("📌 **Base Legal**"):
            st.markdown("Hipóteses previstas na lei que autorizam o tratamento de dados pessoais.")

    with aba3:
        st.subheader("⏳ Histórico de Atualizações da Política de Privacidade")
        st.markdown("""
        <div class="timeline">
          <div class="timeline-container left">
            <div class="date">01/2020</div>
            <div class="timeline-content">
              <h4>Versão Inicial</h4>
              <p>Publicação da primeira versão da Política de Privacidade.</p>
            </div>
          </div>
          <div class="timeline-container right">
            <div class="date">05/2025</div>
            <div class="timeline-content">
              <h4>Revisão Geral</h4>
              <p>Ajustes nos tópicos de Direitos dos Titulares e Compartilhamento de Dados.</p>
            </div>
          </div>
          <div class="timeline-container left">
            <div class="date">05/2025</div>
            <div class="timeline-content">
              <h4>Inclusão de Formulário LGPD</h4>
              <p>Adicionado formulário para solicitação de dados pessoais.</p>
            </div>
          </div>
          <div class="timeline-container right">
            <div class="date">05/2025</div>
            <div class="timeline-content">
              <h4>Atualização de Transparência</h4>
              <p>Adição da tabela de base legal, glossário LGPD e histórico de atualizações.</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("""
    <div class="policy-container">
        <h2 class="section-title"> Introdução</h2>
        <p>A Lei nº 13.709, de 14 de agosto de 2018, Lei Geral de Proteção de Dados Pessoais (LGPD), objetiva proteger os direitos fundamentais da liberdade, da privacidade e o livre desenvolvimento de qualquer pessoa física que se encontre no território brasileiro.<p>
        <p>Seguindo uma tendência global, a LGPD visa ao correto tratamento de dados pessoais, em meios físicos ou digitais, no âmbito de instituições públicas e privadas.<p>
        <p>Nesse contexto, o Instituto de Metrologia e Qualidade do Estado de Minas Gerais desenvolve o seu Programa de Proteção de Dados Pessoais, e esta página pretende dar transparência à implantação do modelo de governança organizacional para adequação à LGPD.</p>
        <p>O documento aplica-se a todos os processos institucionais que envolvam tratamento de dados pessoais, incluindo sistemas, formulários e procedimentos administrativos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="policy-container">
        <h2 class="section-title"> Finalidades do Tratamento</h2>
        <p>Os dados são tratados exclusivamente para as seguintes finalidades legítimas:</p>
    """, unsafe_allow_html=True)

    finalidades = [
        {"icone": "⚖️", "titulo": "Cumprimento de Obrigações Legais", "descricao": "Tratamento necessário para o cumprimento de obrigações legais e regulatórias pelo IPEM-MG.", "base_legal": "Art. 7º, II da LGPD", "exemplos": ["Fiscalização de produtos e serviços", "Metrologia legal", "Processos administrativos"]},
        {"icone": "🏛️", "titulo": "Execução de Políticas Públicas", "descricao": "Para execução de políticas públicas previstas em leis e regulamentos.", "base_legal": "Art. 7º, IV da LGPD", "exemplos": ["Programas de qualidade", "Ações educativas", "Cadastro de empresas"]},
        {"icone": "📝", "titulo": "Execução de Contratos e Convênios", "descricao": "Para gestão de contratos administrativos e convênios.", "base_legal": "Art. 7º, V da LGPD", "exemplos": ["Cadastro de fornecedores", "Gestão de licitações", "Pagamento a fornecedores"]},
    ]

    for finalidade in finalidades:
        with st.container():
            st.markdown(f"""
            <div class="finalidade-card">
                <div class="finalidade-title">{finalidade['icone']} {finalidade['titulo']}</div>
                <p>{finalidade['descricao']}</p>
                <details>
                    <summary style="cursor: pointer; color: #0d6efd; font-weight: 500;">📌 Ver exemplos e base legal</summary>
                    <div class="details-content">
                        <p><strong>Base Legal:</strong> {finalidade['base_legal']}</p>
                        <strong>Exemplos no IPEM-MG:</strong>
                        <ul>{''.join([f'<li>{exemplo}</li>' for exemplo in finalidade['exemplos']])}</ul>
                    </div>
                </details>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <p>Para exercer seus direitos, entre em contato com nosso Encarregado de Dados:</p>
        <p>📧 <strong>encarregado.data@ipem.mg.gov.br</strong> | 📞 <strong>(31) 3399-7100</strong></p>
        <p>🕒 <strong>Horário de atendimento:</strong> Segunda a sexta, das 8h às 18h</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        <p>Última atualização: 16/04/2025 - Versão 1.0</p><br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7134 / 08000 335 335<br>
        <p>© 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.</p>
    </div>
    """, unsafe_allow_html=True)
