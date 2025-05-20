import streamlit as st

# Deve ser o PRIMEIRO comando Streamlit
st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

from login_unificado import registrar_usuario, autenticar_usuario
# Inicializa estados
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Barra lateral - Login/Registro
with st.sidebar:
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

# Corpo da página inicial
st.title("📘 Sistema LGPD - IPEM-MG")
st.markdown("""
Bem-vindo ao sistema de apoio à adequação à Lei Geral de Proteção de Dados (LGPD) do IPEM-MG.

def image_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
        
    st.title("👋 Página Principal")
    st.markdown("---")
    st.markdown("""
    Visualização dos principais fluxos de dados pessoais no IPEM-MG e as medidas de proteção em cada etapa:
    """)

    st.subheader("1. Coleta de Dados")
    st.markdown("""
    **Fontes:**
    - Formulários físicos e digitais
    - Sistemas internos
    - Parceiros e outras fontes legítimas

    **Medidas:**
    - Informar finalidade e base legal
    - Coletar apenas o necessário
    - Obter consentimento quando aplicável
    """)

    st.subheader("2. Armazenamento")
    st.markdown("""
    **Locais:**
    - Bancos de dados seguros
    - Sistemas com controle de acesso
    - Arquivos físicos em locais restritos

    **Medidas:**
    - Criptografia de dados sensíveis
    - Controle de acesso baseado em função
    - Backup regular e seguro
    """)

    st.subheader("3. Processamento/Uso")
    st.markdown("""
    **Atividades:**
    - Análise para tomada de decisão
    - Prestação de serviços públicos
    - Gestão interna

    **Medidas:**
    - Acesso apenas por pessoal autorizado
    - Registro de operações
    - Monitoramento de atividades
    """)

    st.subheader("4. Compartilhamento")
    st.markdown("""
    **Destinatários:**
    - Outros órgãos públicos
    - Parceiros contratados
    - Autoridades quando exigido por lei

    **Medidas:**
    - Acordos de confidencialidade
    - Anonimização quando possível
    - Canais seguros de transferência
    """)

    st.subheader("5. Descarte")
    st.markdown("""
    **Quando:**
    - Cumprida a finalidade
    - Expirado prazo de retenção
    - Solicitação de exclusão pelo titular

    **Medidas:**
    - Exclusão segura (digital)
    - Destruição física adequada
    - Registro do descarte
    """)

    # Rodapé com imagens base64
    try:
        icone_ipem = image_to_base64("icone_ipem.png")
        lgpd_logo = image_to_base64("lgpd_logo.png")

        st.markdown(f"""
        <style>
            .footer {{
                position: fixed;
                bottom: 10px;
                right: 50px;
                display: flex;
                gap: 10px;
            }}
            .footer img {{
                width: 50px;
                height: auto;
                transition: transform 0.3s ease;
            }}
            .footer img:hover {{
                transform: scale(1.2);
            }}
        </style>

        <div class="footer">
            <img src="data:image/png;base64,{icone_ipem}" alt="Ícone IPEM">
            <img src="data:image/png;base64,{lgpd_logo}" alt="Logo LGPD">
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Erro: Não foi possível carregar uma ou ambas as imagens. Verifique os caminhos e tente novamente.")

    # Rodapé texto
    st.markdown("""
    <hr>
    <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
    </p>
    """, unsafe_allow_html=True)

Use o menu lateral para navegar pelas seções do sistema.
""")
