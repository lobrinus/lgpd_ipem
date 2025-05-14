import streamlit as st
import smtplib
from email.message import EmailMessage


    # Exibindo a imagem centralizada com HTML e CSS
st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
    <img src="data:image/png;base64,{encoded_image}" alt="Logo IPEM-MG" style="height: 100px;">
</div>
""", unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Erro: Arquivo de imagem 'ipem_reduzido.png' não encontrado. Verifique o caminho.")
st.set_page_config(page_title="Formulário LGPD", page_icon="📨", layout="wide")

# Oculta esta página do menu lateral
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] a[href$="formulario_lgpd"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)


# CSS de tema consistente
st.markdown("""
<style>
.form-container {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    border: 2px solid black;
}
.form-title {
    color: #2b5876;
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("📨 Formulário de Solicitação - LGPD")

# Formulário
with st.form("formulario_lgpd"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Preencha as informações abaixo:</div>', unsafe_allow_html=True)

    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone de contato")
    email_contato = st.text_input("E-mail de contato")
    cpf = st.text_input("CPF")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("📩 Enviar Solicitação")
    st.markdown('</div>', unsafe_allow_html=True)

    if enviado:
        if nome and telefone and email_contato and cpf and mensagem:
            try:
                # Ajuste conforme o Necessario
                remetente = "seu_email@ipem.mg.gov.br"
                senha = "sua_senha_de_aplicativo"
                destinatario = "encarregado.data@ipem.mg.gov.br"

                msg = EmailMessage()
                msg['Subject'] = "Nova Solicitação LGPD - IPEM-MG"
                msg['From'] = remetente
                msg['To'] = destinatario

                conteudo = f"""
                Nova solicitação recebida via portal LGPD:

                Nome: {nome}
                Telefone: {telefone}
                E-mail: {email_contato}
                CPF: {cpf}
                Mensagem:
                {mensagem}
                """

                msg.set_content(conteudo)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(remetente, senha)
                    smtp.send_message(msg)

                st.success("✅ Solicitação enviada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao enviar o e-mail: {e}")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos.")
