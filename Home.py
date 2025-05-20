import streamlit as st
import importlib
from login_unificado import registrar_usuario, autenticar_usuario

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# Estado inicial do login
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Login unificado na barra lateral
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
                    st.experimental_rerun()
                else:
                    st.error(resultado)

        elif aba == "Registrar":
            email_r = st.text_input("Novo E-mail", key="email_registrar")
            senha_r = st.text_input("Senha", type="password", key="senha_registrar")
            senha2_r = st.text_input("Confirmar Senha", type="password", key="senha2_registrar")

            if st.button("Registrar"):
                if senha_r != senha2_r:
                    st.error("❌ As senhas não coincidem.")
                else:
                    sucesso, msg = registrar_usuario(email_r, senha_r)
                    if sucesso:
                        st.success(msg)
                        st.info("Agora você pode fazer login.")
                        st.session_state["aba_login"] = "Entrar"
                        st.experimental_rerun()
                    else:
                        st.error(msg)

    else:
        user = st.session_state["usuario"]
        st.success(f"🔓 Logado como: {user['email']} ({user['tipo']})")
        if st.button("Sair"):
            for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()

# Define as páginas públicas (chaves: nome mostrado, valores: nome do módulo sem .py)
paginas = {
    "👤 Painel do Cidadão": "14_👤_Painel_Cidadao",
    "👋 Bem-vindo": "0_👋_Pagina_Inicio",
    "🏠 Página Principal": "1_🏠_Página_Principal",
    "📨 Formulário LGPD": "12_📧_Formulario_LGPD",
    "✅ Boas Práticas": "2_✅_Boas_Práticas",
    "📜 Política de Privacidade": "3_📜_Política_de_Privacidade",
    "🔍 Orientação de Dados Pessoais": "4_🔍_Orientação_de_Dados_Pessoais",
    "👥 Quem Lida com os Dados": "5_👥_Quem_Lida_com_os_Dados",
    "🛡️ Mitigação de Riscos": "6_🛡️_Mitigação_de_Riscos",
    "⚖️ Princípios Básicos": "7_⚖️_Princípios_Básicos",
    "✅❌ O Que Fazer e Não_Fazer": "8_✅❌_O_Que_Fazer_e_Não_Fazer",
    "🔄 Fluxo de Dados LGPD": "9_🔄_Fluxo_de_Dados_LGPD",
    "❓ FAQ": "10_❓_FAQ",
    "🔓 Solicitar Acesso Dados": "11_🔓_Solicitar_Acesso_Dados"
}

# Se logado como admin, adiciona página privada
if st.session_state.get("usuario") and st.session_state["usuario"].get("tipo") == "admin":
    paginas["📁 Solicitações Recebidas"] = "13_📁_Solicitações_Recebidas"

# Menu lateral para navegação
pagina_padrao = "👋 Bem-vindo"
pagina_ativa = st.session_state.get("pagina_escolhida", pagina_padrao)
if pagina_ativa not in paginas:
    pagina_ativa = pagina_padrao

pagina_escolhida = st.sidebar.radio(
    "📄 Navegação",
    list(paginas.keys()),
    index=list(paginas.keys()).index(pagina_ativa),
    key="pagina_escolhida"
)
st.session_state["pagina_escolhida"] = pagina_escolhida

# Importa e executa a função render da página escolhida
nome_modulo = paginas[pagina_escolhida]
try:
    modulo = importlib.import_module(f"pages.{nome_modulo}")
    modulo.render()
except Exception as e:
    import traceback
    st.error(f"Erro ao carregar a página '{pagina_escolhida}': {e}")
    st.text(traceback.format_exc())
