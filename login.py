import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.subheader("🔐 Login LGPD")

    if st.session_state.get("logado", False):
        tipo = st.session_state.get("tipo_usuario")
        st.success(f"✅ Você já está logado como {st.session_state['email']} ({tipo})")

        if tipo == "admin":
            st.info("➡️ Acesse o painel de administração no menu 'Solicitações Recebidas'.")
        else:
            st.info("➡️ Acesse o painel do cidadão no menu 'Painel LGPD'.")

        if st.button("🚪 Sair"):
            for key in ["logado", "email", "tipo_usuario", "admin_email"]:
                st.session_state.pop(key, None)
            st.rerun()

        return

    if "aba_login" not in st.session_state:
        st.session_state["aba_login"] = "login"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state["aba_login"] = "login"
    with col2:
        if st.button("Registro"):
            st.session_state["aba_login"] = "registro"

    st.write("---")

    # 🔑 Login
    if st.session_state["aba_login"] == "login":
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            sucesso, dados = autenticar_usuario(email, senha)
            if sucesso:
                st.session_state["logado"] = True
                st.session_state["email"] = dados["email"]
                st.session_state["tipo_usuario"] = dados["tipo"]
                if dados["tipo"] == "admin":
                    st.session_state["admin_email"] = dados["email"]

                # 🔥 Redirecionamento inteligente
                if dados["tipo"] == "admin":
                    st.success("✅ Bem-vindo, administrador!")
                    st.info("➡️ Acesse o painel de administração no menu 'Solicitações Recebidas'.")
                else:
                    st.success("✅ Bem-vindo, cidadão!")
                    st.info("➡️ Acesse o painel do cidadão no menu 'Painel LGPD'.")

                st.experimental_rerun()

            else:
                st.error(dados)

    # 📝 Registro
    else:
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        senha = st.text_input("Senha", type="password")
        senha2 = st.text_input("Confirme a senha", type="password")

        if st.button("Registrar"):
            if not all([nome.strip(), cpf.strip(), email.strip(), telefone.strip(), senha.strip(), senha2.strip()]):
                st.error("❌ Todos os campos são obrigatórios.")
            elif senha != senha2:
                st.error("❌ As senhas não coincidem.")
            elif len(senha) < 6:
                st.error("❌ A senha deve ter pelo menos 6 caracteres.")
            else:
                sucesso, msg = registrar_usuario(email, senha, nome, telefone, cpf)
                if sucesso:
                    st.success(msg)
                    st.session_state["aba_login"] = "login"
                    st.rerun()
                else:
                    st.error(msg)
