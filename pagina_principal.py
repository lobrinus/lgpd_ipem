import streamlit as st
import feedparser # Para ler feeds RSS
from datetime import datetime
import time # Para formatação de data
import re # Para remoção de tags HTML

# Função para buscar e exibir notícias do feed RSS com filtro
def carregar_noticias_lgpd(feed_url, num_noticias=5, termos_filtro=None):
    """
    Busca notícias de um feed RSS, filtra por termos e as exibe no Streamlit.
    """
    if termos_filtro is None:
        # Termos padrão em maiúsculas para facilitar a comparação case-insensitive
        termos_filtro = ["LGPD", "ANPD", "PROTEÇÃO DE DADOS PESSOAIS", "PROTEÇÃO DE DADOS"]

    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo: # Verifica se houve erro ao parsear o feed
            st.error(f"Erro ao carregar o feed de notícias: {feed.bozo_exception}")
            # Adiciona mais detalhes do erro se disponíveis
            if hasattr(feed, 'debug_message'):
                 st.warning(f"Debug Info (Feed): {feed.debug_message}")
            return

        if not feed.entries:
            st.info("Nenhuma notícia encontrada no feed no momento.")
            return

        st.subheader("📰 Notícias Relevantes sobre LGPD e Proteção de Dados (Fonte: Planalto)")
        
        noticias_filtradas_encontradas = []

        for entry in feed.entries:
            titulo = entry.get("title", "").strip()
            link = entry.get("link", "#")
            
            resumo_html = entry.get("summary", entry.get("description", ""))
            
            if resumo_html:
                resumo_texto_limpo = re.sub('<[^<]+?>', '', resumo_html).strip()
            else:
                resumo_texto_limpo = "Sem resumo disponível."

            conteudo_busca = (titulo + " " + resumo_texto_limpo).upper()

            if any(termo.upper() in conteudo_busca for termo in termos_filtro):
                data_publicacao_str = "Data não informada"
                # Tenta obter e formatar a data de publicação
                parsed_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    parsed_date = entry.published_parsed
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed: # Fallback para data de atualização
                    parsed_date = entry.updated_parsed
                
                if parsed_date:
                    try:
                        dt_obj = datetime.fromtimestamp(time.mktime(parsed_date))
                        data_publicacao_str = dt_obj.strftime("%d/%m/%Y às %H:%M")
                    except Exception:
                        # Se houver erro na conversão, usa o valor original se disponível
                        if hasattr(entry, 'published'):
                            data_publicacao_str = entry.get("published", "Data não informada")
                        elif hasattr(entry, 'updated'):
                            data_publicacao_str = entry.get("updated", "Data não informada")
                
                noticias_filtradas_encontradas.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo_limpo": resumo_texto_limpo,
                    "data_publicacao": data_publicacao_str
                })

        if not noticias_filtradas_encontradas:
            st.info(f"Nenhuma notícia encontrada com os termos: {', '.join(termos_filtro)} no feed selecionado.")
            return

        # Exibe o número desejado de notícias filtradas
        for i, noticia in enumerate(noticias_filtradas_encontradas[:num_noticias]):
            with st.container(border=True): # Usando 'border=True' para um visual mais limpo
                st.markdown(f"#### [{noticia['titulo']}]({noticia['link']})")
                st.caption(f"Publicado em: {noticia['data_publicacao']}")
                resumo_preview = (noticia['resumo_limpo'][:350] + '...') if len(noticia['resumo_limpo']) > 350 else noticia['resumo_limpo']
                st.markdown(f"<div style='text-align: justify; font-size: 0.95em;'>{resumo_preview}</div>", unsafe_allow_html=True)
                if noticia['link'] != "#":
                    st.link_button("Ler matéria completa", noticia['link'], use_container_width=True)
            if i < min(num_noticias, len(noticias_filtradas_encontradas)) - 1:
                st.markdown("---") # Adiciona um separador visual

    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar buscar e filtrar as notícias: {e}")
        st.error(f"URL do Feed utilizado: {feed_url}")


def render():
    st.markdown("""
    <h1 style='text-align: center;'>🏠 Bem Vindo ao Portal LGPD - IPEM-MG</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    

    # Seção de Acesso Rápido
    st.subheader("⚡ Acesso Rápido")
    cols = st.columns([1, 1, 1], gap="small")
    with cols[0]:
        st.link_button(
            label="📜 Política de Privacidade",
            url="https://www.ipem.mg.gov.br/politica-de-privacidade-e-protecao-de-dados-pessoais",
            use_container_width=True
        )
    with cols[1]:
        st.link_button(
            label="📋 Solicitação de Dados",
            url="https://www.ipem.mg.gov.br/fale-conosco",
            use_container_width=True
        )
    with cols[2]:
        st.link_button(
            label="⚖️ Guia LGPD",
            url="https://www.gov.br/governodigital/pt-br/lgpd-pagina-do-cidadao",
            use_container_width=True
        )
    st.markdown("---")

    # Inclusão da seção de notícias LGPD
    feed_planalto_url = "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias/ultimas-noticias/RSS"
    # Termos para filtrar as notícias, mais específicos
    termos_para_filtrar = ["LGPD", "ANPD", "Proteção de Dados Pessoais", "Proteção de Dados"] 
    carregar_noticias_lgpd(feed_planalto_url, num_noticias=3, termos_filtro=termos_para_filtrar) # Exibindo 3 notícias

    st.markdown("---")

    # Seção de Contato
    with st.container():
        col1, col2 = st.columns([2, 3])
        with col1:
            st.subheader("📞 Contato do Encarregado de Dados")
            st.markdown("""
            **Encarregado (DPO):** Leonardo Silva Marafeli
            **E-mail:** [encarregado.data@ipem.mg.gov.br](mailto:encarregado.data@ipem.mg.gov.br)
            **Telefone:** (31) 3399-7100
            **Horário:** 8h às 18h (dias úteis)
            **Endereço:**
            Rua Cristiano França Teixeira Guimarães, 80
            Bairro Cinco - Contagem/MG
            CEP: 32010-130
            """)
        with col2:
            st.subheader("🚨 Canal de Denúncias LGPD")
            st.markdown("""
            **Para reportar incidentes ou irregularidades relacionados a LGPD:**
            - 📧 [encarregado.data@ipem.mg.gov.br](mailto:encarregado.data@ipem.mg.gov.br)
            - 📞 (31) 3399-7100 / 0800 335 335
            - 🌐 Formulário Online via Painel LGPD
            """)
    st.markdown("---")

    # Últimas Notícias (do sistema)
    st.subheader("📢 Novidades do Portal") # Alterei o título para diferenciar do feed de notícias externas
    with st.expander("🔔 Atualizações do Sistema (Status: 20/05/2025)"):
        st.markdown("""
        - Nova funcionalidade de acompanhamento de solicitações.
        - Atualização da Política de Privacidade (versão 2.1).
        - Integração com notícias sobre a LGPD diretamente de fontes governamentais.
        - Treinamento LGPD para servidores (em andamento).
        """)
    st.markdown("---")

    # Recursos Importantes
    st.subheader("📚 Recursos Importantes")
    tab1, tab2, tab3 = st.tabs(["Legislação", "Boas Práticas", "FAQ"])
    with tab1:
        st.markdown("""
        **Legislação Relevante:**
        - [Lei nº 13.709/2018 (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
        - [Decreto nº 10.474/2020](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10474.htm)
        - [Resoluções da ANPD](https://www.gov.br/anpd/pt-br)
        """)
    with tab2:
        st.markdown("""
        **Principais Boas Práticas:**
        1. Coleta mínima necessária de dados.
        2. Criptografia de dados sensíveis em trânsito e repouso.
        3. Atualização regular de sistemas e softwares.
        4. Treinamento anual de colaboradores sobre LGPD.
        5. Auditorias periódicas de segurança e conformidade.
        """)
    with tab3:
        st.markdown("""
        **Perguntas Frequentes:**
        P: Como solicitar exclusão de dados?
        R: Através do Painel LGPD ou formulário específico de contato com o DPO.

        P: Quanto tempo demora uma resposta à minha solicitação?
        R: O prazo padrão é de até 15 dias, podendo ser prorrogado mediante justificativa, dependendo da complexidade.

        P: Posso acessar dados de terceiros através do portal?
        R: Não. O acesso é restrito aos dados do próprio titular, salvo representação legal ou autorização judicial.
        """)
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px; font-size:0.9em;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)

