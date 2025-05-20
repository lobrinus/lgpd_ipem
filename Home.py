import streamlit as st
from login_unificado import registrar_usuario, autenticar_usuario

# Configuração da página
st.set_page_config(
    page_title="LGPD - IPEM-MG",
    page_icon="🏠",
    layout="wide"
)

# Inicializa estados de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Barra lateral - Login/Registro
with st.sidebar:
    st.page_link("pages/1_pagina_principal.py", label="🏠 Página Principal")
    st.markdown("## 🔐 Acesso")

    if st.session_state["usuario"] is None:
        aba = st.radio("Escolha uma opção:", ["Entrar", "Registrar"], horizontal=True, key="aba_login")

        if aba == "Entrar":
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                sucesso, resultado = autenticar_usuario(email, senha)
                if sucesso:
                    st.session_state["usuario"] = resultado
                    st.session_state["logado"] = True
                    st.session_state["tipo_usuario"] = resultado["tipo"]
                    st.session_state["email"] = resultado["email"]
                    if resultado["tipo"] == "admin":
                        st.session_state["admin_email"] = resultado["email"]
                    st.rerun()
                else:
                    st.error(resultado)
        elif aba == "Registrar":
            email_r = st.text_input("Novo E-mail")
            senha_r = st.text_input("Senha", type="password")
            senha2_r = st.text_input("Confirmar Senha", type="password")
            if st.button("Registrar"):
                if senha_r != senha2_r:
                    st.error("❌ As senhas não coincidem.")
                else:
                    sucesso, msg = registrar_usuario(email_r, senha_r)
                    if sucesso:
                        st.success(msg)
                        st.info("Agora você pode fazer login.")
                        st.session_state["aba_login"] = "Entrar"
                        st.rerun()
                    else:
                        st.error(msg)
    else:
        user = st.session_state.get("usuario", None)
        if isinstance(user, dict) and "email" in user and "tipo" in user:
            st.success(f"🔓 Logado como: {user['email']} ({user['tipo']})")
            if st.button("Sair"):
                for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                    st.session_state.pop(key, None)
                st.rerun()
        else:
            st.warning("⚠️ Sessão iniciada, mas os dados do usuário estão incompletos. Tente sair e entrar novamente.")
            if st.button("Forçar logout"):
                for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                    st.session_state.pop(key, None)
                st.rerun()

# Corpo principal da página inicial
if st.session_state.get("logado"):
    st.title("🏠 Portal LGPD - IPEM-MG")
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
            st.subheader("🚨 Canal de Denúncias")
            st.markdown("""
            **Para reportar incidentes ou irregularidades:**  
            - 📧 [ouvidoria@ipem.mg.gov.br](mailto:ouvidoria@ipem.mg.gov.br)  
            - 📞 0800 335 335  
            - 🌐 [Formulário Online](https://www.ipem.mg.gov.br/fale-conosco)
            """)
    
    st.markdown("---")
    
    # Seção de Acesso Rápido
    st.subheader("⚡ Acesso Rápido")
    cols = st.columns(4)
    with cols[0]:
        st.markdown("📜 [Política de Privacidade](https://www.ipem.mg.gov.br/politica-de-privacidade-e-protecao-de-dados-pessoais)")
    with cols[1]:
        st.markdown("📋 [Formulário de Solicitação de Dados](https://www.ipem.mg.gov.br/fale-conosco)")
    with cols[2]:
        st.markdown("⚖️ [Guia LGPD para Cidadãos](https://www.gov.br/governodigital/pt-br/lgpd-pagina-do-cidadao)")
    with cols[3]:
        st.markdown("🔒 [Painel do Cidadão](#)")
    
    st.markdown("---")
    
    # Últimas Atualizações
    st.subheader("📢 Últimas Notícias")
    with st.expander("🔔 Novidades do Sistema (Atualizado em 20/05/2025)"):
        st.markdown("""
        - Nova funcionalidade de acompanhamento de solicitações
        - Atualização da Política de Privacidade (versão 2.1)
        - Treinamento LGPD para servidores em 25/05
        """)
    
    # Seção Informativa
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
        R: Através do Painel do Cidadão ou formulário específico[21]

        Q: Quanto tempo demora uma resposta?  
        R: Prazo máximo de 15 dias úteis[14]

        Q: Posso acessar dados de terceiros?  
        R: Somente com autorização judicial expressa[19]
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

else:
    st.title("📘 Bem-vindo ao Sistema LGPD do IPEM-MG")
    st.markdown("---")
    st.markdown("""
    **O Instituto de Pesos e Medidas de Minas Gerais está comprometido com a proteção de dados pessoais em conformidade com a Lei Geral de Proteção de Dados (LGPD).**

    🔐 Faça login ou registre-se na barra lateral para:
    - Acompanhar solicitações de dados
    - Acessar documentos institucionais
    - Realizar denúncias e reclamações
    - Consultar políticas de privacidade

    *"Promovendo a transparência e segurança no tratamento de dados pessoais desde 2020"*
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


