from streamlit_option_menu import option_menu
import streamlit as st

st.set_page_config(
    page_title="Portal LGPD - IPEM-MG",
    page_icon="📘",
    layout="wide"
)

# CSS para ocultar os ícones do menu (se ainda quiser)
st.markdown("""
    <style>
    .icon {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("ipem_mg.png", use_container_width=True)
with st.sidebar:
    if st.session_state.get("logado", False):
        email = st.session_state.get("email", "")
        tipo = st.session_state.get("tipo_usuario", "cidadao").lower()

        if tipo == "admin":
            texto_tipo = "Administrador"
        else:
            texto_tipo = "Cidadão"

        st.markdown(
            f"""
            <div style="
                background-color: #4CAF50;
                padding: 10px;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                margin-bottom: 15px;
                word-break: break-word;
            ">
                Usuário: {email}<br>
                Logado como {texto_tipo}
            </div>
            """,
            unsafe_allow_html=True
        )
    pagina = option_menu(
        "Menu Principal",
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
        ],
        # NÃO passar o parâmetro icons para evitar sobrescrever seus ícones
        menu_icon="cast",
        default_index=1,
        orientation="vertical"
    )

# --- Renderização de cada página ---
if pagina == "🔐 Login":
    import login
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
