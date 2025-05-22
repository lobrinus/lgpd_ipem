import streamlit as st
from PIL import Image
from login_unificado import autenticar_usuario, registrar_usuario
# CSS personalizado

def render()
st.markdown("""
<style>
.policy-container {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.section-title {
    color: #2b5876;
    border-bottom: 2px solid #2b5876;
    padding-bottom: 0.5rem;
    margin-top: 1.5rem;
}
.finalidade-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid #2b5876;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.finalidade-card:hover {
    transform: translateX(5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    background-color: #e9f5ff;
}
.finalidade-title {
    color: #2b5876;
    font-weight: bold;
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.details-content {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 0.8rem;
    border: 1px solid #e1e4e8;
}
.info-box {
    background-color: #f0f9ff;
    border-left: 4px solid #2b5876;
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📜 Política de Privacidade</h1>", unsafe_allow_html=True)
st.markdown("---")

# ABAS
aba1, aba2, aba3 = st.tabs(["📑 Base Legal", "📖 Glossário", "⏳ Linha do Tempo"])

########################
# ABA 1 - BASE LEGAL
########################
with aba1:
    st.subheader("📑 Base Legal Aplicável ")
    
    st.markdown("""
    <style>
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      border: 1px solid #dddddd;
      padding: 8px;
      text-align: center;
    }
    th {
      background-color: #4CAF50;
      color: white;
    }
    td {
      background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

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
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; font-style: italic;'>
    De acordo com o art. 7º, incisos I ao X, e caput do art. 23
    </p>
    """, unsafe_allow_html=True)

########################
# ABA 2 - GLOSSÁRIO
########################
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


########################
# ABA 3 - LINHA DO TEMPO
########################
with aba3:
    st.subheader("⏳ Histórico de Atualizações da Política de Privacidade")

    st.markdown("""
    <style>
    .timeline {
      position: relative;
      max-width: 1000px;
      margin: 0 auto;
    }
    .timeline::after {
      content: '';
      position: absolute;
      width: 6px;
      background-color: #4CAF50;
      top: 0;
      bottom: 0;
      left: 50%;
      margin-left: -3px;
    }
    .container {
      padding: 10px 40px;
      position: relative;
      background-color: inherit;
      width: 50%;
    }
    .container.left {
      left: 0;
    }
    .container.right {
      left: 50%;
    }
    .date {
      padding: 5px;
      background: #4CAF50;
      color: white;
      position: absolute;
      top: 15px;
      width: 100px;
      text-align: center;
      border-radius: 6px;
    }
    .left .date {
      right: -120px;
    }
    .right .date {
      left: -120px;
    }
    .content {
      padding: 20px;
      background-color: #f9f9f9;
      position: relative;
      border-radius: 6px;
    }
    </style>

    <div class="timeline">

      <div class="container left">
        <div class="date">01/2023</div>
        <div class="content">
          <h4>Versão Inicial</h4>
          <p>Publicação da primeira versão da Política de Privacidade.</p>
        </div>
      </div>

      <div class="container right">
        <div class="date">06/2023</div>
        <div class="content">
          <h4>Revisão Geral</h4>
          <p>Ajustes nos tópicos de Direitos dos Titulares e Compartilhamento de Dados.</p>
        </div>
      </div>

      <div class="container left">
        <div class="date">02/2024</div>
        <div class="content">
          <h4>Inclusão de Formulário LGPD</h4>
          <p>Adicionado formulário para solicitação de dados pessoais.</p>
        </div>
      </div>

      <div class="container right">
        <div class="date">05/2025</div>
        <div class="content">
          <h4>Atualização de Transparência</h4>
          <p>Adição da tabela de base legal, glossário LGPD e histórico de atualizações.</p>
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)



#  Introdução
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Introdução</h2>
    <p>A Lei nº 13.709, de 14 de agosto de 2018, Lei Geral de Proteção de Dados Pessoais (LGPD), objetiva proteger os direitos fundamentais da liberdade, da privacidade e o livre desenvolvimento de qualquer pessoa física que se encontre no território brasileiro.<p>
    <p>Seguindo uma tendência global, a LGPD visa ao correto tratamento de dados pessoais, em meios físicos ou digitais, no âmbito de instituições públicas e privadas.<p>
    <p>Nesse contexto, o Instituto de Metrologia e Qualidade do Estado de Minas Gerais desenvolve o seu Programa de Proteção de Dados Pessoais, e esta página pretende dar transparência à implantação do modelo de governança organizacional para adequação à LGPD.</p>
    <p>O documento aplica-se a todos os processos institucionais que envolvam tratamento de dados pessoais, incluindo sistemas, formulários e procedimentos administrativos.</p>
</div>
""", unsafe_allow_html=True)


# Alterações na Política
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Alterações na Política</h2>
    <p>Esta política poderá ser atualizada para refletir mudanças normativas ou operacionais. As alterações serão comunicadas:</p>
    <ul>
        <li>Através do nosso site institucional</li>
        <li>Na seção <strong style="color: #2b5876;">Últimas Atualizações</strong> da Página Principal</li>
    </ul>
</div>
""", unsafe_allow_html=True)


#  Definições
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Definições</h2>
    <ul>
        <li><strong>Titular</strong>: Pessoa natural a quem se referem os dados</li>
        <li><strong>Controlador</strong>: IPEM-MG, que decide sobre o tratamento</li>
        <li><strong>Operador</strong>: Terceiros que processam dados em nosso nome</li>
        <li><strong>Encarregado (DPO)</strong>: Responsável pela proteção de dados</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# CSS para estilização de quadros
st.markdown("""
<style>
    .container-section {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .finalidade-card {
        border: 2px solid black; /* Borda Preta */
        border-radius: 10px; /* Bordas arredondadas */
        padding: 20px; /* Espaço interno */
        background-color: #f9f9f9; /* Fundo claro */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra */
        margin-bottom: 20px; /* Espaçamento entre os quadros */
        flex: 1; /* Permite ajustar o tamanho */
    }
    .finalidade-title {
        color: black;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px; /* Espaçamento abaixo do título */
    }
    .data-container {
        display: flex; /* Layout horizontal */
        gap: 20px; /* Espaçamento entre os quadros */
        justify-content: space-between; /* Ajusta alinhamento horizontal */
        flex-wrap: wrap; /* Ajusta automaticamente em telas menores */
    }
    .data-container ul {
        list-style-type: none; /* Remove marcadores padrão */
        padding-left: 0;
    }
    .data-container ul li {
        margin-bottom: 10px; /* Espaçamento entre os itens */
    }
</style>
""", unsafe_allow_html=True)

# CSS básico para estilização
st.markdown("""
    <style>
        .finalidade-card {
            border: 2px solid black; /* Borda Preta */
            border-radius: 10px; /* Bordas arredondadas */
            padding: 20px; /* Espaço interno */
            background-color: #f9f9f9; /* Fundo claro */
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra */
            margin-bottom: 20px; /* Espaçamento inferior */
        }
        .finalidade-title {
            color: balck; /* Cor do título */
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 10px; /* Espaçamento abaixo do título */
        }
        ul {
            list-style-type: none; /* Remove marcadores padrão */
            padding-left: 0; /* Remove espaçamento à esquerda */
        }
        ul li {
            margin-bottom: 10px; /* Espaçamento entre itens */
        }
    </style>
""", unsafe_allow_html=True)

# Seção: Dados Coletados
st.header("Dados Coletados")
st.markdown("O IPEM-MG coleta os seguintes dados, organizados de acordo com sua natureza:")

# Layout com colunas nativas para quadros
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="finalidade-card">
        <div class="finalidade-title">📄 Dados Pessoais</div>
        <ul>
            <li><b>Nome</b></li>
            <li><b>CPF</b></li>
            <li><b>RG</b></li>
            <li><b>Data de Nascimento</b></li>
            <li><b>Gênero</b></li>
            <li><b>Endereço</b></li>
            <li><b>Telefone</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="finalidade-card">
        <div class="finalidade-title">📄 Dados Pessoais Sensíveis</div>
        <ul>
            <li><b>Origem racial ou étnica</b></li>
            <li><b>Convicção religiosa</b></li>
            <li><b>Opinião política</b></li>
            <li><b>Dados referentes à saúde ou à vida sexual</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

#  Finalidades do Tratamento
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Finalidades do Tratamento</h2>
    <p>Os dados são tratados exclusivamente para as seguintes finalidades legítimas:</p>
""", unsafe_allow_html=True)

finalidades = [
    {
        "icone": "⚖️",
        "titulo": "Cumprimento de Obrigações Legais",
        "descricao": "Tratamento necessário para o cumprimento de obrigações legais e regulatórias pelo IPEM-MG.",
        "base_legal": "Art. 7º, II da LGPD",
        "exemplos": [
            "Fiscalização de produtos e serviços conforme Lei nº 9.933/1999",
            "Metrologia legal conforme Decreto nº 2.182/1997",
            "Registro de instrumentos de medição",
            "Processos administrativos de infração",
            "Comunicações ao Ministério Público e órgãos de controle"
        ]
    },
    {
        "icone": "🏛️",
        "titulo": "Execução de Políticas Públicas",
        "descricao": "Para execução de políticas públicas previstas em leis e regulamentos.",
        "base_legal": "Art. 7º, IV da LGPD",
        "exemplos": [
            "Programas de qualidade e metrologia",
            "Ações educativas para consumidores",
            "Cadastro de empresas regulamentadas",
            "Publicação de resultados de fiscalização",
            "Certificação de produtos"
        ]
    },
    {
        "icone": "📝",
        "titulo": "Execução de Contratos e Convênios",
        "descricao": "Para gestão de contratos administrativos e convênios.",
        "base_legal": "Art. 7º, V da LGPD",
        "exemplos": [
            "Cadastro de fornecedores e contratados",
            "Gestão de processos licitatórios",
            "Pagamento a fornecedores",
            "Fiscalização de contratos",
            "Comunicação com outros órgãos públicos"
        ]
    },
    {
        "icone": "👥",
        "titulo": "Proteção à Vida e Incolumidade Física",
        "descricao": "Para proteção da vida ou da incolumidade física do titular ou de terceiro.",
        "base_legal": "Art. 7º, VIII da LGPD",
        "exemplos": [
            "Registro de acidentes com produtos fiscalizados",
            "Emergências em laboratórios de metrologia",
            "Comunicação de produtos perigosos à vigilância sanitária",
            "Cadastro de EPIs para fiscais",
            "Relatórios de segurança do trabalho"
        ]
    },
    {
        "icone": "🔍",
        "titulo": "Prevenção à Fraude e Segurança",
        "descricao": "Para prevenção à fraude e garantia da segurança do titular.",
        "base_legal": "Art. 7º, IX da LGPD",
        "exemplos": [
            "Sistemas de identificação de fiscais",
            "Registro de denúncias anônimas",
            "Controle de acesso às dependências do órgão",
            "Monitoramento de sistemas",
            "Investigação de irregularidades"
        ]
    },
    {
        "icone": "📊",
        "titulo": "Estudos por Órgão de Pesquisa",
        "descricao": "Para realização de estudos por órgão de pesquisa, garantida a anonimização.",
        "base_legal": "Art. 7º, IV c/c Art. 11 da LGPD",
        "exemplos": [
            "Pesquisas estatísticas sobre consumo",
            "Estudos metrológicos",
            "Relatórios anuais de fiscalização",
            "Indicadores de qualidade",
            "Dados anonimizados para pesquisas acadêmicas"
        ]
    },
    {
        "icone": "💼",
        "titulo": "Processamento Interno Administrativo",
        "descricao": "Para atendimento das necessidades administrativas internas do IPEM-MG.",
        "base_legal": "Art. 7º, V da LGPD",
        "exemplos": [
            "Gestão de recursos humanos",
            "Controle de ponto eletrônico",
            "Registro de treinamentos",
            "Comunicações internas",
            "Gestão documental"
        ]
    }
]

for finalidade in finalidades:
    with st.container():
        st.markdown(f"""
        <div class="finalidade-card">
            <div class="finalidade-title">
                {finalidade['icone']} {finalidade['titulo']}
            </div>
            <p>{finalidade['descricao']}</p>
            <details>
                <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">
                    📌 Ver exemplos e base legal
                </summary>
                <div class="details-content">
                    <p><strong>Base Legal:</strong> {finalidade['base_legal']}</p>
                    <strong>Exemplos no IPEM-MG:</strong>
                    <ul>
                        {''.join([f'<li>{exemplo}</li>' for exemplo in finalidade['exemplos']])}
                    </ul>
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Fecha o container

#  Compartilhamento de Dados
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Compartilhamento de Dados</h2>
    <p>O IPEM-MG poderá compartilhar dados pessoais com:</p>
""", unsafe_allow_html=True)

# Dados em formato estruturado para fácil manutenção
compartilhamento = [
    {
        "icone": "🏛️",
        "titulo": "Órgãos Públicos",
        "descricao": "Para cumprimento de obrigações legais ou execução de políticas públicas",
        "detalhes": [
            "Ministério Público",
            "Órgãos de fiscalização",
            "Secretarias estaduais",
            "Agências reguladoras"
        ]
    },
    {
        "icone": "🤝",
        "titulo": "Terceiros Contratados",
        "descricao": "Parceiros que prestam serviços ao Instituto, mediante contrato com cláusulas de proteção de dados",
        "detalhes": [
            "Empresas de tecnologia",
            "Consultorias especializadas",
            "Laboratórios de metrologia",
            "Serviços de auditoria"
        ]
    }
]

for item in compartilhamento:
    st.markdown(f"""
    <div class="finalidade-card">
        <div class="finalidade-title">{item['icone']} {item['titulo']}</div>
        <p>{item['descricao']}</p>
        <details>
            <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">
                📌 Ver exemplos
            </summary>
            <div class="details-content">
                <strong>Exemplos de compartilhamento:</strong>
                <ul>
                    {''.join([f'<li>{exemplo}</li>' for exemplo in item['detalhes']])}
                </ul>
            </div>
        </details>
    </div>
    """, unsafe_allow_html=True)

# Fechamento do container
st.markdown("</div>", unsafe_allow_html=True)

#  Direitos dos Titulares
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Direitos dos Titulares</h2>
    <p>De acordo com o Art. 18 da LGPD, você tem direito a:</p>
""", unsafe_allow_html=True)

# Dados estruturados para os direitos
direitos = [
    {
        "icone": "🔍",
        "titulo": "Acesso",
        "descricao": "Solicitar cópia dos dados pessoais em tratamento",
        "detalhes": [
            "Relatório completo dos dados armazenados",
            "Informação sobre as finalidades do tratamento",
            "Lista de compartilhamentos realizados"
        ]
    },
    {
        "icone": "✏️",
        "titulo": "Correção",
        "descricao": "Atualizar dados incompletos, inexatos ou desatualizados",
        "detalhes": [
            "Retificação de informações cadastrais",
            "Atualização de endereço ou contato",
            "Correção de registros funcionais"
        ]
    },
    {
        "icone": "🚫",
        "titulo": "Anonimização",
        "descricao": "Solicitar a eliminação da identificação quando possível",
        "detalhes": [
            "Eliminação de dados não obrigatórios",
            "Conversão para dados anônimos",
            "Generalização",
            "Criptografia",
            "Tarjamento",
            "Bloqueio de dados desnecessários"
        ]
    }
]

# Exibição dos direitos
for direito in direitos:
    st.markdown(f"""
    <div class="finalidade-card">
        <div class="finalidade-title">{direito['icone']} {direito['titulo']}</div>
        <p>{direito['descricao']}</p>
        <details>
            <summary style="cursor: pointer; color: #2b5876; font-weight: 500;">
                📌 Ver detalhes
            </summary>
            <div class="details-content">
                <strong>Exemplos de aplicação:</strong>
                <ul>
                    {''.join([f'<li>{detalhe}</li>' for detalhe in direito['detalhes']])}
                </ul>
            </div>
        </details>
    </div>
    """, unsafe_allow_html=True)

#  Medidas de Segurança
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Medidas de Segurança</h2>
    <p>O IPEM-MG adota as seguintes medidas técnicas e administrativas:</p>
    <ul>
        <li>Criptografia de dados sensíveis</li>
        <li>Controle de acesso com credenciais individuais</li>
        <li>Monitoramento contínuo dos sistemas</li>
        <li>Treinamento dos colaboradores</li>
        <li>Backup protegido</li>
        <li>Atualizações dos sistemas de segurança</li>
        <li>Conscientização</li>
        <li>Prevenção de Ameaças</li>
    </ul>
</div>
""", unsafe_allow_html=True)

#  Retenção e Eliminação
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Retenção e Eliminação</h2>
    <p>Os dados pessoais são mantidos pelo período necessário para:</p>
    <ul>
        <li>Cumprimento de obrigações legais (ex: 5 anos para processos administrativos)</li>
        <li>Exercício regular de direitos</li>
        <li>Preservação de interesses públicos</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# Legislação Aplicável
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Legislação Aplicável</h2>
    <p>Esta política está fundamentada nos seguintes dispositivos da <strong>Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018)</strong>:</p>
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem;">
        <!-- Quadro 1 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">📜 Disposições Gerais</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 1º-6º</strong>: Princípios e fundamentos</li>
                <li><strong>Art. 6º</strong>: Princípios do tratamento</li>
            </ul>
        </div>
        <!-- Quadro 2 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">⚖️ Bases Legais</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 7º, II</strong>: Cumprimento de obrigação legal</li>
                <li><strong>Art. 7º, IV</strong>: Políticas públicas</li>
                <li><strong>Art. 7º, V</strong>: Execução de contratos</li>
            </ul>
        </div>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem;">
        <!-- Quadro 3 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">🛡️ Segurança</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 46</strong>: Medidas de segurança</li>
                <li><strong>Art. 47</strong>: Relatório de impacto</li>
            </ul>
        </div>
        <!-- Quadro 4 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">🏛️ Órgãos Públicos</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 23</strong>: Tratamento governamental</li>
                <li><strong>Art. 24</strong>: Compartilhamento público</li>
            </ul>
        </div>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem;">
        <!-- Quadro 5 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">👤 Direitos</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 18</strong>: Direitos dos titulares</li>
                <li><strong>Art. 19</strong>: Prazos de resposta</li>
            </ul>
        </div>
        <!-- Quadro 6 -->
        <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #2b5876; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 1rem; color: #2b5876;">🚨 Proteção</h4>
            <p><strong>Artigos:</strong></p>
            <ul style="padding-left: 1.5rem; line-height: 1.6;">
                <li><strong>Art. 7º, VIII</strong>: Proteção à vida</li>
                <li><strong>Art. 7º, IX</strong>: Prevenção à fraude</li>
            </ul>
        </div>
    </div>
    <div class="info-box" style="margin-top: 2rem;">
        <p>Para consulta integral da legislação:</p>
        <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm" 
           target="_blank" style="color: #2b5876; font-weight: bold; text-decoration: none; transition: all 0.3s ease;">
           📚 Acesse o texto completo da LGPD
        </a>
        <p style="margin-top: 0.5rem; font-size: 0.9em;">Link oficial do Planalto</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Box de contato do DPO
st.markdown("""
<div class="info-box">
    <p>Para exercer seus direitos, entre em contato com nosso Encarregado de Dados:</p>
    <p>📧 <strong>encarregado.data@ipem.mg.gov.br</strong> | 📞 <strong>(31) 3399-7100</strong></p>
    <p>🕒 <strong>Horário de atendimento:</strong> Segunda a sexta, das 8h às 18h</p>
</div>

</div>  <!-- Fecha o policy-container -->
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Última atualização: 16/04/2025 - Versão 1.0</p>
    <p>Instituto de Pesos e Medidas do Estado de Minas Gerais</p>
    <p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.
</p>
</div>
""", unsafe_allow_html=True)

render()

