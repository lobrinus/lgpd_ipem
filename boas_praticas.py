import streamlit as st

def render():
    st.markdown("""
<style>
    /* Estilos Gerais */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* --- CORREÇÃO PARA DARK MODE --- */
    /* Define os quadros para usarem as cores do tema do Streamlit */
    .section, .sidebar-section {
        border: 1px solid #4F4F4F; /* Uma cor de borda neutra que funciona bem em ambos os modos */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        /* Usa a cor de fundo secundária do tema, que muda automaticamente entre claro e escuro */
        background-color: var(--secondary-background-color);
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Define o texto dos cabeçalhos dentro dos quadros para usar a cor de texto do tema */
    .section h3, .sidebar-section h3 {
        /* Usa a cor de texto principal do tema, que muda automaticamente entre preto e branco */
        color: var(--text-color);
        font-weight: bold;
    }

    /* O texto dentro das listas (li) herdará a cor do tema automaticamente, 
       desde que não seja forçado para outra cor. */
    .section ul, .sidebar-section ul {
        padding-left: 20px;
    }

    /* Mantém as outras regras que não causam problemas de cor */
    .highlight {
        font-weight: bold;
        color: black; /* O destaque amarelo com texto preto geralmente funciona bem em ambos os modos */
        background-color: #ffeb3b;
    }

    /* Adapta a seção de FAQ para usar as cores do tema */
    .faq-section {
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        /* Também adapta a cor de fundo */
        background-color: var(--secondary-background-color);
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* A cor do título do FAQ (laranja) tem bom contraste em ambos os modos */
    .faq-title {
        color: #FF9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: center;'>✔️ Boas Práticas</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    O IPEM-MG está comprometido em garantir a conformidade com a **LGPD** (Lei Geral de Proteção de Dados). 
    Aqui você encontra informações detalhadas, dicas práticas e conteúdos para promover uma cultura de 
    **privacidade e segurança de dados**:
    """)

    col1, col2, col3 = st.columns([2, 4, 2])

    with col1:
        st.markdown("""
        <div class="sidebar-section">
            <h3>📘 Sobre a LGPD:</h3>
            <ul>
                <li><b>Objetivo:</b> Proteger direitos fundamentais como privacidade e liberdade.</li>
                <li><b>Aplicação:</b> Empresas e órgãos que coletam ou tratam dados pessoais.</li>
                <li><b>Fundamentos:</b> Segurança, transparência e consentimento.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-section">
            <h3>🔑 Dicas para Titulares:</h3>
            <ul>
                <li>Leia sempre as <b>políticas de privacidade</b> antes de fornecer informações.</li>
                <li>Questione o motivo do uso de seus dados.</li>
                <li>Exerça seus direitos, como <b>acesso e retificação</b> de dados.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section">
            <h3>1. Gestão de Dados Pessoais</h3>
            <ul>
                <li><b>Inventário de dados:</b> Mapeamento completo de todos os dados pessoais tratados</li>
                <li><b>Classificação de dados:</b> Identificação de dados sensíveis e críticos</li>
                <li><b>Limitação de acesso:</b> Princípio do menor privilégio</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
            <h3>2. Segurança da Informação</h3>
            <ul>
                <li><b>Criptografia:</b> Para dados em trânsito e em repouso</li>
                <li><b>Controle de acesso:</b> Autenticação forte e logs detalhados</li>
                <li><b>Backup seguro:</b> Com políticas de retenção definidas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
            <h3>3. Capacitação e Conscientização</h3>
            <ul>
                <li><b>Treinamentos regulares:</b> Para todos os colaboradores</li>
                <li><b>Comunicação clara:</b> Orientações sobre tratamento adequado</li>
                <li><b>Cultura de privacidade:</b> Incentivo à proteção de dados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
            <h3>4. Transparência</h3>
            <ul>
                <li><b>Política de privacidade clara:</b> Disponível no site institucional</li>
                <li><b>Canais de comunicação:</b> Para dúvidas e solicitações de titulares</li>
                <li><b>Registro de operações:</b> Documentação dos tratamentos realizados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
            <h3>5. Gerenciamento de Riscos</h3>
            <ul>
                <li><b>Análise de riscos:</b> Avaliar potenciais impactos no tratamento de dados.</li>
                <li><b>Plano de resposta:</b> Criar estratégias para lidar com incidentes.</li>
                <li><b>Continuidade:</b> Garantir que os serviços sejam mantidos em caso de falhas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="sidebar-section">
            <h3>📊 Dados Relevantes:</h3>
            <ul>
                <li><b>80%:</b> Empresas no Brasil estão investindo em LGPD.</li>
                <li><b>25M:</b> Multas aplicadas desde 2020.</li>
                <li><b>60%:</b> Violações são causadas por erro humano.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone: (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
