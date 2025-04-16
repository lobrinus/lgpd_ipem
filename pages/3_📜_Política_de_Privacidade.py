import streamlit as st
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Política de Privacidade - IPEM-MG",
    page_icon="📜",
    layout="wide"
)

# CSS personalizado
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

# Cabeçalho
logo = Image.open('ipem_mg.png')
st.image(logo, width=200)
st.title("📜 Política de Privacidade do IPEM-MG")
st.markdown("---")

#  Introdução
st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Introdução</h2>
    <p>Esta Política de Privacidade estabelece as diretrizes para tratamento de dados pessoais no âmbito do Instituto de Pesos e Medidas do Estado de Minas Gerais (IPEM-MG), em conformidade com a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).</p>
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
        <li>Na seção de <a href="/Página_Principal#ultimas-atualizacoes" target="_self" style="color: #2b5876; font-weight: bold; text-decoration: underline;">
           Últimas Atualizações
           </a> da Página Principal
        </li>
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

#  Dados Coletados
dados_coletados = [
    {
        "icone": "📋",
        "titulo": "Dados de Identificação",
        "itens": "Nome completo, CPF, RG, data de nascimento, filiação, local de nascimento, gênero, nacionalidade, estado civil"
    },
    {
        "icone": "📞",
        "titulo": "Dados de Contato",
        "itens": "Endereço residencial, e-mail, telefone fixo e celular, "
    },
    {
        "icone": "🏢",
        "titulo": "Dados Profissionais",
        "itens": "Registro profissional, formação acadêmica, histórico funcional"
    },
    {
        "icone": "🗂️",
        "titulo": "Dados Sensíveis",
        "itens": "Informações sobre saúde, deficiência, origem racial ou étnica, convicções religiosas, opiniões políticas, vida sexual"
    }
]

st.markdown("""
<div class="policy-container">
    <h2 class="section-title"> Dados Coletados</h2>
    <p>O IPEM-MG trata os seguintes tipos de dados pessoais:</p>
""", unsafe_allow_html=True)

for dado in dados_coletados:
    st.markdown(f"""
    <div class="finalidade-card">
        <div class="finalidade-title">{dado['icone']} {dado['titulo']}</div>
        <p>{dado['itens']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

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

# Box de contato do DPO
st.markdown("""
<div class="info-box">
    <p>Para exercer seus direitos, entre em contato com nosso Encarregado de Dados:</p>
    <p>📧 <strong>ouvidoria@ipem.mg.gov.br</strong> | 📞 <strong>(31) 3399-7100</strong></p>
    <p>🕒 <strong>Horário de atendimento:</strong> Segunda a sexta, das 8h às 18h</p>
</div>

</div>  <!-- Fecha o policy-container -->
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



# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Última atualização: 15/03/2023 - Versão 1.0</p>
    <p>Instituto de Pesos e Medidas do Estado de Minas Gerais</p>
</div>
""", unsafe_allow_html=True)