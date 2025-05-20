import streamlit as st
import os
from login_unificado import registrar_usuario, autenticar_usuario

st.set_page_config(page_title="LGPD - IPEM-MG", layout="wide")

# ✅ Garante que o estado 'logado' exista
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Login unificado direto na barra lateral
with st.sidebar:
    st.markdown("## 🔐 Acesso")

    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

if st.session_state["usuario"] is None:
    aba = st.radio("Escolha uma opção:", ["Entrar", "Registrar"], horizontal=True)

    if aba == "Entrar":
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            from login_unificado import autenticar_usuario
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
                    from login_unificado import registrar_usuario
                    sucesso, msg = registrar_usuario(email_r, senha_r)
                    if sucesso:
                        st.success(msg)
                        st.info("Agora você pode fazer login.")
                        st.session_state["usuario"] = {
                            "email": email_r.lower(),
                            "tipo": "cidadao"
                        }
                        st.session_state["logado"] = True
                        st.session_state["tipo_usuario"] = "cidadao"
                        st.session_state["email"] = email_r.lower()
                        st.rerun()
                    else:
                        st.error(msg)

else:
    user = st.session_state.get("usuario", None)

    if isinstance(user, dict) and "email" in user and "tipo" in user:
        st.success(f"🔓 Logado como: {user['email']} ({user['tipo']})")
        if st.button("Sair"):
            # Limpa todas as variáveis relacionadas ao login
            for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                st.session_state.pop(key, None)
            st.rerun()
    else:
        st.warning("⚠️ Sessão iniciada, mas os dados do usuário estão incompletos. Tente sair e entrar novamente.")
        if st.button("Forçar logout"):
            for key in ["usuario", "logado", "tipo_usuario", "email", "admin_email"]:
                st.session_state.pop(key, None)
            st.rerun()



# Define as páginas públicas
paginas = {
    "👤 Painel do Cidadão": "14_👤_Painel_Cidadao.py",
    "👋 Bem-vindo": "0_👋_Pagina_Inicio.py",
    "🏠 Página Principal": "1_🏠_Página_Principal.py",
    "📨 Formulário LGPD": "12_📧_Formulario_LGPD.py",
    "✅ Boas Práticas": "2_✅_Boas_Práticas.py",
    "📜 Política de Privacidade": "3_📜_Política_de_Privacidade.py",
    "🔍 Orientação de Dados Pessoais": "4_🔍_Orientação_de_Dados_Pessoais.py",
    "👥 Quem Lida com os Dados": "5_👥_Quem_Lida_com_os_Dados.py",
    "🛡️ Mitigação de Riscos": "6_🛡️_Mitigação_de_Riscos.py",
    "⚖️ Princípios Básicos": "7_⚖️_Princípios_Básicos.py",
    "✅❌ O Que Fazer e Não_Fazer": "8_✅❌_O_Que_Fazer_e_Não_Fazer.py",
    "🔄 Fluxo de Dados LGPD": "9_🔄_Fluxo_de_Dados_LGPD.py",
    "❓ FAQ": "10_❓_FAQ.py",
    "🔓 Solicitar Acesso Dados": "11_🔓_Solicitar_Acesso_Dados.py"
}

# Se logado como admin, mostra página privada
if "usuario" in st.session_state and st.session_state["usuario"]:
    tipo = st.session_state["usuario"]["tipo"]
    if tipo == "admin":
        paginas["📁 Solicitações Recebidas"] = "13_📁_Solicitações_Recebidas.py"


# Menu lateral
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

# Executa a página escolhida
arquivo = paginas[pagina_escolhida]
if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        try:
            exec(f.read(), globals())
        except Exception as e:
            import traceback
            st.error(f"Erro no exec: {e}")
            st.text(traceback.format_exc())
else:
    st.error(f"❌ Arquivo '{arquivo}' não encontrado. Verifique se ele está no diretório correto.")
