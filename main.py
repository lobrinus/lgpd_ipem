from streamlit_option_menu import option_menu
import streamlit as st

st.set_page_config(
    page_title="Portal LGPD - IPEM-MG",
    page_icon="📘",
    layout="wide"
)

try:
    st.sidebar.image("icone_ipem.png", use_container_width=True)
except Exception as e:
    st.sidebar.warning(f"Não foi possível carregar a imagem 'icone_ipem.png': {e}")


menu_items_sidebar = [
    "Página Principal",
    "Boas Práticas",
    "Orientação de Dados Pessoais",
    "Quem Lida com os Dados",
    "Política de Privacidade",
    "Mitigação de Riscos",
    "Princípios Básicos",
    "O Que Fazer e Não Fazer",
    "Fluxo de Dados LGPD",
    "FAQ"
]
menu_icons_sidebar = ["house-door-fill", "patch-check-fill", "search-heart-fill",
                      "people-fill", "file-earmark-text-fill", "shield-lock-fill", "bank",
                      "hand-thumbs-up-fill", "arrows-angle-contract", "question-circle-fill"]

with st.sidebar:
    try:
        pagina_selecionada_sidebar = option_menu(
            "Menu Principal",
            options=menu_items_sidebar,
            icons=menu_icons_sidebar,
            menu_icon="list-stars",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px !important", "background-color": "transparent"},
                "icon": {"color": "#0d6efd", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#44475a" # Uma cor de hover que funciona bem em ambos os modos
                },
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            }
        )
    except Exception as e_option_menu:
        st.error(f"Erro ao renderizar o menu de navegação: {e_option_menu}")
        st.stop()

PAGES = {
    "Página Principal": "pagina_principal",
    "Boas Práticas": "boas_praticas",
    "Orientação de Dados Pessoais": "orientacao_dados",
    "Quem Lida com os Dados": "quem_lida",
    "Política de Privacidade": "politica_privacidade",
    "Mitigação de Riscos": "mitigacao_riscos",
    "Princípios Básicos": "principios",
    "O Que Fazer e Não Fazer": "fazer_nao_fazer",
    "Fluxo de Dados LGPD": "fluxo_dados",
    "FAQ": "faq"
}

if pagina_selecionada_sidebar in PAGES:
    module_name = PAGES[pagina_selecionada_sidebar]
    try:
        module = __import__(module_name)
        module.render()
    except ImportError:
        st.error(f"Módulo '{module_name}.py' não encontrado. Verifique o nome do arquivo.")
        st.info(f"Dica: Crie um arquivo chamado '{module_name}.py' na raiz do projeto com uma função 'def render(): st.write(\"Conteúdo de {pagina_selecionada_sidebar}\")'.")
    except AttributeError:
        st.error(f"Módulo '{module_name}.py' não possui uma função chamada 'render()'.")
        st.info(f"Dica: No arquivo '{module_name}.py', defina uma função 'def render():'.")
    except Exception as e_render_geral:
        st.error(f"Erro inesperado ao renderizar a página '{pagina_selecionada_sidebar}': {e_render_geral}")
else:
    st.error(f"Página '{pagina_selecionada_sidebar}' não reconhecida pelo sistema de navegação.")
