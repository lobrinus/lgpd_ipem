import streamlit as st

# Configuração inicial do app
st.set_page_config(
    page_title="Portal LGPD - IPEM-MG",
    page_icon="📘",
    layout="wide"
)

# --- Menu Lateral ---
st.sidebar.image("logo_ipem.png", use_column_width=True)
st.sidebar.title("Menu de Navegação")

pagina = st.sidebar.selectbox(
    "Selecione uma página:",
    [
        "🔐 Login",
        "🏠 Página Principal",
        "👤 Painel Cidadão",
        "✅ Boas Práticas",
        "🔍 Orientação de Dados Pessoais",
        "👥 Quem Lida com os Dados",
        "📜 Política de Privacidade",
        "🛡️ Mitigação de Riscos",
        "⚖️ Princípios Básicos",
        "✅❌ O Que Fazer e Não Fazer",
        "🔄 Fluxo de Dados LGPD",
        "🔓 Solicitar Acesso aos Dados",
        "📧 Formulário LGPD",
        "📁 Solicitações Recebidas",
        "❓ FAQ"
    ]
)

# --- Renderização de cada página ---
if pagina == "🔐 Login":
    import home
    login.render()

elif pagina == "🏠 Página Principal":
    import pagina_principal
    pagina_principal.render()

elif pagina == "👤 Painel Cidadão":
    import painel_cidadao
    painel_cidadao.render()

elif pagina == "✅ Boas Práticas":
    import boas_praticas
    boas_praticas.render()

elif pagina == "🔍 Orientação de Dados Pessoais":
    import orientacao_dados
    orientacao_dados.render()

elif pagina == "👥 Quem Lida com os Dados":
    import quem_lida
    quem_lida.render()

elif pagina == "📜 Política de Privacidade":
    import politica_privacidade
    politica_privacidade.render()

elif pagina == "🛡️ Mitigação de Riscos":
    import mitigacao_riscos
    mitigacao_riscos.render()

elif pagina == "⚖️ Princípios Básicos":
    import principios
    principios.render()

elif pagina == "✅❌ O Que Fazer e Não Fazer":
    import fazer_nao_fazer
    fazer_nao_fazer.render()

elif pagina == "🔄 Fluxo de Dados LGPD":
    import fluxo_dados
    fluxo_dados.render()

elif pagina == "🔓 Solicitar Acesso aos Dados":
    import solicitar_acesso
    solicitar_acesso.render()

elif pagina == "📧 Formulário LGPD":
    import formulario_lgpd
    formulario_lgpd.render()

elif pagina == "📁 Solicitações Recebidas":
    import solicitacoes_recebidas
    solicitacoes_recebidas.render()

elif pagina == "❓ FAQ":
    import faq
    faq.render()
