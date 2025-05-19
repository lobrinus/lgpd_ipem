import streamlit as st
from PIL import Image
import feedparser
from login import exibir_login


st.title("🏠 Página Principal")
st.markdown("---")
st.markdown("""
**Bem-vindo ao Portal LGPD do IPEM-MG**

Este portal centraliza todas as informações sobre a implementação da Lei Geral de Proteção de Dados no âmbito do Instituto de Pesos e Medidas de Minas Gerais.
""")

st.markdown("""
<div class="info-box">
    <h4>Destaques:</h4>
    <ul>
        <li><a href="/Política_de_Privacidade" target="_self">📜 Conheça nossa Política de Privacidade</a></li>
        <li><a href="/Solicitar_Acesso_Dados" target="_self">🔓 Saiba como solicitar acesso a seus dados pessoais</a></li>
        <li><a href="/Princípios_Básicos" target="_self">⚖️ Entenda os princípios básicos da LGPD</a></li>
        <li><a href="/Boas_Práticas" target="_self">✅ Veja as boas práticas adotadas pelo IPEM-MG</a></li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("Últimas Atualizações")
st.markdown("""
- **15/03/2025:** Atualização da Política de Privacidade
- **01/04/2025:** Realização de treinamento para colaboradores
- **19/08/2020:** Nomeação do Encarregado de Dados
""")

st.subheader("Contato do Encarregado de Dados")
st.markdown("""
**E-mail:** encarregado.data@ipem.mg.gov.br  
**Telefone:** (31) 3399-7100   
**Horário de atendimento:** 8h às 18h (dias úteis)
""")
st.markdown("---")
st.subheader("🔐 Acesso Administrativo")

if not st.session_state.get("logado"):
    user = st.text_input("Usuário", key="login_user")
    password = st.text_input("Senha", type="password", key="login_pass")
    if st.button("Entrar"):
        usuarios = st.secrets["auth"]
        if user in usuarios and usuarios[user] == password:
            st.session_state["logado"] = True
            st.success("✅ Login realizado com sucesso.")
            st.experimental_rerun()
        else:
            st.error("❌ Usuário ou senha inválidos.")
else:
    st.success("👤 Usuário administrador logado")
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.experimental_rerun()


# Rodapé
st.markdown("""
<hr>
<p style="text-align: center; color: gray;">
    © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
</p>
""", unsafe_allow_html=True)
