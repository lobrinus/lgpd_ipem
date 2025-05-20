import streamlit as st
import base64
import os
import feedparser
from datetime import datetime
from PIL import Image



def image_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render():
    st.title("👋 Bem Vindo")

    # Verificação SE as imagens existem
    if not os.path.exists("ipem_mg.png"):
        st.error("Erro: ipem_mg.png não encontrado!")
    if not os.path.exists("img_lgpd/privacy.jpg"):
        st.error("Erro: privacy.jpg não encontrado na pasta img_lgpd!")
    
    # CSS personalizado
    st.markdown("""
        <style>
        .header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .news-container {
            background-color: #f9f5e9;
            padding: 2rem;
            border: 1px solid #d4d4d4;
            margin: 2rem 0;
            font-family: 'Georgia', serif;
        }
        .news-header {
            color: #8b0000;
            border-bottom: 2px solid #8b0000;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }
        .news-card {
            background-color: #fffdf6;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid #8b0000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .news-title {
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: #222;
        }
        .news-meta {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            font-style: italic;
        }
        .news-pagination {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        .news-pagination button {
            background-color: #8b0000 !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
        }
        .news-pagination button:disabled {
            background-color: #cccccc !important;
            cursor: not-allowed;
        }
        button {
            background-color: #8b0000 !important;
            color: white !important;
        }
        .highlight-box {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        .highlight-box:hover {
            background-color: #2b5876;
            color: white !important;
            transform: scale(1.02);
        }
        .highlight-box:hover a {
            color: white !important;
        }
        .watermark {
            position: fixed;
            bottom: 10px;
            right: 10px;
            opacity: 0.2;
            z-index: -1;
        }    
        .info-box {
            background-color: #f0f9ff;
            border-left: 4px solid #2b5876;
            padding: 1em;
            margin: 1em 0;
            border-radius: 0 8px 8px 0;
        }
        .info-box ul {
            padding-left: 20px;
        }
        .info-box a {
            color: #2b5876;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .info-box a:hover {
            color: #1e3a8a;
            text-decoration: underline;
        }
        
        .transparent-img {
            opacity: 0.3;  /* 0.0 (totalmente transparente) a 1.0 (totalmente opaco) */
        }
            </style>
        """, unsafe_allow_html=True)
    
    
        # Testando a imagem centralizada
        try:
            # Carregando a imagem
            logo = Image.open('ipem_reduzido.png')
        
            # Convertendo a imagem para base64 para uso em HTML
            with open('ipem_reduzido.png', "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
        
            # Exibindo a imagem centralizada com HTML e CSS
            st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
                <img src="data:image/png;base64,{encoded_image}" alt="Logo IPEM-MG" style="height: 100px;">
            </div>
            """, unsafe_allow_html=True)
        
        except FileNotFoundError:
            st.error("Erro: Arquivo de imagem 'ipem_reduzido.png' não encontrado. Verifique o caminho.")
        
        # Conteúdo principal com título centralizado
        st.markdown("""
        <div style="text-align: center;">
            <h1>Bem-vindo ao Portal LGPD do IPEM-MG</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        
        # Destaques com hiperlinks
        st.subheader("Destaques:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="highlight-box">
                <a href="https://www.gov.br/anpd/pt-br" target="_blan_self">
                🏛️ Site oficial da ANPD
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="highlight-box">
                <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm" target="_blan_self">
                📜 Acesse o texto da Lei nº 13.709/2018 (LGPD)
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # SEÇÃO DE ÚLTIMAS NOTÍCIAS SOBRE LGPD
        @st.cache_data(ttl=3600)
        def fetch_news():
            try:
                feed = feedparser.parse("https://news.google.com/rss/search?q=LGPD+OR+'Lei+Geral+de+Proteção+de+Dados'&hl=pt-BR&gl=BR&ceid=BR:pt-419")
                return [{
                    'title': entry.title.replace(" - ", " — "),
                    'source': getattr(entry, 'source', {}).get('title', 'Fonte desconhecida'),
                    'date': datetime(*entry.published_parsed[:6]).strftime('%d/%m/%Y às %H:%M') if hasattr(entry, 'published_parsed') else 'Data desconhecida',
                    'link': entry.link,
                    'summary': entry.get('summary', 'Clique para ler a matéria completa...')
                } for entry in feed.entries]
            except Exception as e:
                st.error(f"Erro ao carregar notícias: {e}")
                return []
        
        # Controle de paginação
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        news_data = fetch_news()
        per_page = 5
        total_pages = (len(news_data) + per_page - 1) // per_page
        
        # Container principal
        with st.container():
            st.markdown("""
            <div class="news-container">
                <div class="news-header">📰 Ultimas Notícias da LGPD</div>
            """, unsafe_allow_html=True)
        
            # Notícias da página atual
            start_idx = st.session_state.current_page * per_page
            for news in news_data[start_idx:start_idx + per_page]:
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">{news['title']}</div>
                    <div class="news-meta">{news['source']} | {news['date']}</div>
                    <p>{news['summary']}</p>
                    <a href="{news['link']}" target="_blank">🔗 Ler matéria completa</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Controles de paginação
        st.markdown("""
        <div class="news-pagination">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])  # Definição das colunas com proporções
        
        # Botão "Notícias anteriores" na esquerda
        with col1:
            if st.button("◀ Notícias anteriores", 
                         disabled=st.session_state.current_page == 0,
                         key="prev_btn"):
                st.session_state.current_page -= 1
                st.rerun()
        
        # Espaço no meio (coluna central - opcional para estética)
        with col2:
            st.markdown("")  # Vazio, mas pode ser usado para mensagens ou instruções
        
        # Botão "Próximas notícias" na direita
        with col3:
            if st.button("Próximas notícias ▶", 
                         disabled=st.session_state.current_page >= total_pages - 1,
                         key="next_btn"):
                st.session_state.current_page += 1
                st.rerun()
        
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem; color: #666;">
                Página {st.session_state.current_page + 1} de {total_pages}
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Informações básicas
        st.markdown("---")
        st.subheader("Informações Básicas sobre a LGPD")
        st.markdown("""
        A **Lei Geral de Proteção de Dados (LGPD)**, Lei nº 13.709/2018, estabelece normas sobre o tratamento de dados pessoais. 
        A Lei Geral de Proteção de Dados Pessoais (LGPD), em vigor desde 2020, estabelece diretrizes para o tratamento de dados pessoais no Brasil, visando garantir a privacidade e a segurança das informações dos cidadãos.
        Para os cidadãos, a LGPD representa um avanço na garantia de seus direitos à privacidade e ao controle sobre suas informações pessoais. Para os servidores públicos, especialmente aqueles envolvidos no tratamento de dados, é essencial compreender e aplicar as diretrizes da LGPD para assegurar a conformidade legal e proteger os dados sob sua responsabilidade.
        """)
        
        # Convertendo imagens para base64
        try:
            icone_ipem = image_to_base64("icone_ipem.png")
            lgpd_logo = image_to_base64("lgpd_logo.png")
        
        # CSS para o rodapé    
            st.markdown(f"""
            <style>
                .footer {{
                    position: fixed;
                    bottom: 10px; /* Posiciona no rodapé */
                    right: 50px; /* Encosta à direita */
                    display: flex; /* Organiza os ícones lado a lado */
                    gap: 10px; /* Espaço entre os ícones */
                }}
                .footer img {{
                    width: 50px; /* Define o tamanho dos ícones */
                    height: auto; /* Mantém proporções */
                    transition: transform 0.3s ease; /* Suavidade ao passar o mouse */
                }}
                .footer img:hover {{
                    transform: scale(1.2); /* Efeito de zoom no hover */
                }}
            </style>
        
            <div class="footer">
                <img src="data:image/png;base64,{icone_ipem}" alt="Ícone IPEM">
                <img src="data:image/png;base64,{lgpd_logo}" alt="Logo LGPD">
            </div>
            """, unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.error("Erro: Não foi possível carregar uma ou ambas as imagens. Verifique os caminhos e tente novamente.")

