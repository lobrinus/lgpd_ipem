import streamlit as st
# Importa as funções e variáveis necessárias de login_unificado
try:
    from login_unificado import (
        autenticar_usuario,
        registrar_usuario,
        db # Para verificar se o serviço está disponível, opcional aqui
    )
except ImportError:
    st.error("ERRO CRÍTICO: 'login_unificado.py' não encontrado. A funcionalidade de login está indisponível.")
    st.stop()

def render():
    st.markdown("<h2 style='text-align: center;'>🔐 Acesso ao Portal LGPD</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Verifica se os serviços de autenticação estão disponíveis
    if not autenticar_usuario or not registrar_usuario or not db:
        st.error("❌ Ops! Os serviços de autenticação ou banco de dados não estão disponíveis no momento. Tente novamente mais tarde.")
        st.stop()

    # Se o usuário já está logado, exibe mensagem e opção de sair
    if st.session_state.get("logado", False):
        tipo_logado = st.session_state.get("tipo_usuario", "N/A").capitalize()
        nome_logado = st.session_state.get("nome_usuario", st.session_state.get("email", "Usuário"))

        st.success(f"✅ Você já está logado como {nome_logado} (Perfil: {tipo_logado}).")
        st.markdown("---")
        if tipo_logado.lower() == "admin":
            st.info("➡️ Como Administrador, você pode acessar 'Solicitações Recebidas' no menu principal.")
        else:
            st.info("➡️ Acesse o 'Painel LGPD' no menu principal para gerenciar suas solicitações.")

        if st.button("🚪 Sair / Logout", key="login_page_btn_logout", use_container_width=True):
            keys_to_clear = ["logado", "email", "tipo_usuario", "nome_usuario", "modo_auth_painel"]
            for key_clear_logout in keys_to_clear:
                if key_clear_logout in st.session_state:
                    del st.session_state[key_clear_logout]
            st.success("Logout realizado com sucesso!")
            st.rerun()
        return # Interrompe a renderização do formulário de login/registro

    # Abas para Login e Registro
    if "aba_login_principal" not in st.session_state:
        st.session_state["aba_login_principal"] = "login" # Estado da aba específico para esta página

    tab_login, tab_registro = st.tabs(["🔑 Entrar na Conta", "📝 Criar Nova Conta"])

    with tab_login:
        st.subheader("👤 Identifique-se")
        with st.form("form_login_principal_page"):
            email_login_main = st.text_input("Seu E-mail*", key="main_login_email_page")
            senha_login_main = st.text_input("Sua Senha*", type="password", key="main_login_senha_page")
            submit_login_main = st.form_submit_button("Entrar", use_container_width=True)

            if submit_login_main:
                if not email_login_main or not senha_login_main:
                    st.warning("⚠️ Por favor, preencha seu e-mail e senha.")
                else:
                    sucesso, user_data = autenticar_usuario(email_login_main, senha_login_main)
                    if sucesso:
                        st.session_state["logado"] = True
                        st.session_state["email"] = user_data["email"]
                        st.session_state["tipo_usuario"] = user_data["tipo"]
                        st.session_state["nome_usuario"] = user_data["nome"] # Importante para consistência
                        st.success(f"✅ Bem-vindo(a) de volta, {user_data['nome']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"{user_data}") # Exibe a mensagem de erro de autenticar_usuario
    with tab_registro:
        st.subheader("✍️ Crie sua conta de acesso")
        with st.form("form_registro_principal_page"):
            nome_reg_main = st.text_input("Nome Completo*", key="main_reg_nome_page")
            cpf_reg_main = st.text_input("CPF ou CNPJ*", max_chars=18, key="main_reg_cpf_page")
            telefone_reg_main = st.text_input("Telefone (com DDD)*", key="main_reg_telefone_page")
            email_reg_main = st.text_input("E-mail*", key="main_reg_email_page")
            senha_reg_main = st.text_input("Crie uma Senha (mínimo 6 caracteres)*", type="password", key="main_reg_senha_page")
            senha2_reg_main = st.text_input("Confirme a Senha*", type="password", key="main_reg_senha_conf_page")
            submit_registro_main = st.form_submit_button("Registrar Minha Conta", use_container_width=True)

            if submit_registro_main:
                if not all([nome_reg_main.strip(), cpf_reg_main.strip(), telefone_reg_main.strip(), email_reg_main.strip(), senha_reg_main.strip(), senha2_reg_main.strip()]):
                    st.warning("⚠️ Todos os campos marcados com * são obrigatórios.")
                elif senha_reg_main != senha2_reg_main:
                    st.error("❌ As senhas digitadas não coincidem.")
                elif len(senha_reg_main) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                else:
                    # tipo="cidadao" é o padrão na função registrar_usuario
                    sucesso, msg = registrar_usuario(
                        email=email_reg_main,
                        senha=senha_reg_main,
                        nome=nome_reg_main,
                        telefone=telefone_reg_main,
                        cpf=cpf_reg_main
                    )
                    if sucesso:
                        st.success(msg + " Por favor, acesse a aba 'Entrar na Conta' para fazer login.")
                        # Não faz st.rerun() aqui para o usuário ver a mensagem e mudar de aba manualmente
                        # ou você pode mudar a aba automaticamente se preferir:
                        # st.session_state["aba_login_principal"] = "login"
                        # st.rerun()
                    else:
                        st.error(f"{msg}")
    st.markdown("---")
    st.caption("Ao se registrar ou fazer login, você concorda com nossa Política de Privacidade e Termos de Uso.")

