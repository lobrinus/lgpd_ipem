import streamlit as st
from login import exibir_login

st.set_page_config(
    page_title="Boas Práticas - LGPD IPEM-MG",
    page_icon="✅",
    layout="wide"  # Layout amplo para melhor aproveitamento da tela
)
exibir_login()
# CSS Geral e Reformulação de Estilo
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .section, .sidebar-section {
        border: 2px solid black; /* Cor da borda */
        border-radius: 10px; /* Bordas arredondadas */
        padding: 20px; /* Espaço interno */
        margin-bottom: 20px; /* Espaço entre seções */
        background-color: #f9f9f9; /* Cor do fundo */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra */
    }
    .sidebar-section {
        background-color: #e8f5e9; /* Fundo verde-claro */
    }
    .section h3, .sidebar-section h3 {
        color: black; /* Cor do título */
        font-weight: bold;
    }
    .section ul, .sidebar-section ul {
        padding-left: 20px; /* Recuo para listas */
    }
    .highlight {
        font-weight: bold;
        color: black; /* Cor do texto destacado */
        background-color: #ffeb3b; /* Fundo amarelo para destaque */
    }
    .faq-section {
        border: 2px solid #FF9800; /* Laranja para destacar FAQs */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #FFF3E0; /* Fundo laranja claro */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .faq-title {
        color: #FF9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título Principal e Introdução
st.title("✅ Boas Práticas no IPEM-MG")
st.markdown("---")
st.markdown("""
O IPEM-MG está comprometido em garantir a conformidade com a **LGPD** (Lei Geral de Proteção de Dados). Aqui você encontra informações detalhadas, dicas práticas e conteúdos para promover uma cultura de **privacidade e segurança de dados**:
""")

# Layout dividido em colunas para aproveitar o espaço
col1, col2, col3 = st.columns([1.2, 3, 1.2])

# Lateral esquerda
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

# Conteúdo principal
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


# Lateral direita
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


# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
