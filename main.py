from streamlit_option_menu import option_menu
import streamlit as st

# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Portal LGPD - IPEM-MG",
    page_icon="📘",  # Ou o caminho para um ícone .png/.ico, ex: "img_lgpd/icone.png"
    layout="wide"
)

# --- Barra Lateral (Sidebar) ---
# Certifique-se que 'icone_ipem.png' está na pasta raiz ou forneça o caminho correto.
# Exemplo se estiver em uma subpasta: "img_lgpd/icone_ipem.png"
try:
    st.sidebar.image("icone_ipem.png", use_container_width=True)
except Exception as e:
    st.sidebar.warning(f"Não foi possível carregar a imagem 'icone_ipem.png': {e}")

        st.markdown(
            f"""
            <div style="
                border: 1px solid #ddd; /* Borda cinza clara */
                background-color: #90EE90; /* Fundo levemente verde claro */
                padding: 12px;
                border-radius: 8px;
                color: #333; /* Cor do texto escura */
                font-weight: bold;
                margin-bottom: 20px;
                word-break: break-word;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08); /* Sombra suave */
            ">
                <span style="font-size: 0.9em; color: #555;">Usuário:</span> {display_name_sidebar}<br>
                <span style="font-size: 0.9em; color: #555;">Perfil:</span> {tipo_usuario_sidebar}
            </div>
            """,
            unsafe_allow_html=True
        )


    # --- Definição do Menu de Navegação ---
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
    menu_icons_sidebar = ["house-door-fill", "person-badge-fill", "patch-check-fill", "search-heart-fill",
                          "people-fill", "file-earmark-text-fill", "shield-lock-fill", "bank",
                          "hand-thumbs-up-fill", "arrows-angle-contract", "question-circle-fill"] # Ícone "arrows- μέσω-fill" não é padrão, trocado.

    if st.session_state.get("logado", False) and st.session_state.get("tipo_usuario") == "admin":
        admin_menu_item = "Painel Administrador"
        admin_menu_icon = "folder2-open" # Ícone para o painel admin
        if admin_menu_item not in menu_items_sidebar:
            menu_items_sidebar.insert(2, admin_menu_item) # Posição 2 (terceiro item)
            menu_icons_sidebar.insert(2, admin_menu_icon)

    try:
        pagina_selecionada_sidebar = option_menu(
            "Menu Principal",
            options=menu_items_sidebar,
            icons=menu_icons_sidebar,
            menu_icon="list-stars", # Ícone do menu
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px !important", "background-color": "#f0f2f6"}, # Cor de fundo suave
                "icon": {"color": "#0d6efd", "font-size": "20px"}, # Azul para ícones
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#dde"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"}, # Azul para selecionado
            }
        )
    except Exception as e_option_menu:
        st.error(f"Erro ao renderizar o menu de navegação: {e_option_menu}")
        st.stop() # Impede a continuação se o menu falhar

# --- Lógica de Renderização de Páginas ---
# Cada 'nome_do_arquivo.py' deve ter uma função render()
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

# Verifica se a página selecionada existe no mapeamento
if pagina_selecionada_sidebar in PAGES:
    module_name = PAGES[pagina_selecionada_sidebar]

    else:
        # Para todas as outras páginas
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

