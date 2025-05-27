import streamlit as st
import feedparser # Para ler feeds RSS
from datetime import datetime
import time # Para formatação de data

# Função para buscar e exibir notícias do feed RSS
def carregar_noticias_lgpd(feed_url, num_noticias=5):
    """
    Busca notícias de um feed RSS e as exibe no Streamlit.
    """
    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo: # Verifica se houve erro ao parsear o feed
            st.error(f"Erro ao carregar o feed de notícias: {feed.bozo_exception}")
            return

        if not feed.entries:
            st.info("Nenhuma notícia encontrada no feed no momento.")
            return

        st.subheader("📰 Últimas Notícias sobre LGPD (ANPD)")
        for i, entry in enumerate(feed.entries[:num_noticias]):
            titulo = entry.get("title", "Sem título")
            link = entry.get("link", "#")
            resumo = entry.get("summary", "Sem resumo disponível.")

            # Tenta formatar a data de publicação
            data_publicacao_str = "Data não informada"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    # entry.published_parsed é uma tupla time.struct_time
                    # Converte para objeto datetime e depois formata
                    dt_obj = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    data_publicacao_str = dt_obj.strftime("%d/%m/%Y às %H:%M")
                except Exception:
                    # Se houver erro na conversão, usa o valor original se disponível
                    data_publicacao_str = entry.get("published", "Data não informada")
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed: # Fallback para data de atualização
                 try:
                    dt_obj = datetime.fromtimestamp(time.mktime(entry.updated_parsed))
                    data_publicacao_str = dt_obj.strftime("%d/%m/%Y às %H:%M")
                 except Exception:
                    data_publicacao_str = entry.get("updated", "Data não informada")


            with st.container(border=True):
                st.markdown(f"#### [{titulo}]({link})")
                st.caption(f"Publicado em: {data_publicacao_str}")
                st.markdown(f"<div style='text-align: justify;'>{resumo}</div>", unsafe_allow_html=True)
                st.link_button("Ler mais", link, use_container_width=True)
            if i < num_noticias - 1: # Adiciona um separador, exceto após a última notícia
                st.markdown("---")

    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar buscar as notícias: {e}")


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
        st.markdown("---") # Separador

        # Chamada para a função de notícias
        feed_anpd_url = "https://www.gov.br/anpd/pt-br/assuntos/noticias/RSS"
        carregar_noticias_lgpd(feed_anpd_url) # Você pode ajustar o número de notícias aqui
    
        st.markdown("---") # Separador
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

    # Últimas Notícias
    st.subheader("📢 Últimas Notícias")
    with st.expander("🔔 Novidades do Sistema (Atualizado em 20/05/2025)"):
        st.markdown("""
        - Nova funcionalidade de acompanhamento de solicitações
        - Atualização da Política de Privacidade (versão 2.1)
        - Integração com notícias sobre a LGPD diretamente dos sites oficiais
        - Treinamento LGPD para servidores em 
        """)
    # Recursos
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
        1. Coleta mínima necessária
        2. Criptografia de dados sensíveis
        3. Atualização regular de sistemas
        4. Treinamento anual de colaboradores
        5. Auditorias trimestrais de segurança
        """)
    with tab3:
        st.markdown("""
        **Perguntas Frequentes:**
        Q: Como solicitar exclusão de dados?  
        R: Através do Painel LGPD ou formulário específico

        Q: Quanto tempo demora uma resposta?  
        R: Prazo máximo de 15 dias úteis. Com a probabilidade de prorrogação dependendo da complexidade da solicitação

        Q: Posso acessar dados de terceiros?  
        R: Somente com autorização judicial expressa
        """)
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
