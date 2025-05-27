import streamlit as st
import datetime
import os # Para manipulação de caminhos e extensões de arquivo
import pytz # Para fusos horários
# import json # Não usado diretamente se os segredos são dicts
import uuid # Para nomes de arquivo únicos
from firebase_admin import firestore # Apenas firestore se db já importado
# Importa as funções e variáveis necessárias de login_unificado
try:
    from login_unificado import (
        autenticar_usuario,
        registrar_usuario,
        upload_file_to_storage,
        db, # Instância do Firestore client
        timezone_brasilia, # Objeto de fuso horário
        gerar_protocolo_unico # Função para gerar protocolo
    )
except ImportError:
    st.error("ERRO CRÍTICO: 'login_unificado.py' não encontrado. Funcionalidades essenciais do Painel LGPD estão indisponíveis.")
    st.stop()

def exibir_rodape():
    # Função para exibir o rodapé padronizado
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px; font-size: 0.9em;">
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335<br>
        <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render():
    st.markdown("<h1 style='text-align: center;'>👤 Painel LGPD</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if not db or not autenticar_usuario or not registrar_usuario or not upload_file_to_storage or not gerar_protocolo_unico:
        st.error("❌ Ops! Um ou mais serviços essenciais não estão disponíveis. Verifique 'login_unificado.py' e a configuração do Firebase.")
        st.stop()

    if "modo_auth_painel" not in st.session_state:
        st.session_state["modo_auth_painel"] = "login"

    if not st.session_state.get("logado", False):
        st.subheader("Acesse ou crie sua conta para continuar")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Entrar no Painel", key="painel_btn_login_tab_render", use_container_width=True):
                st.session_state["modo_auth_painel"] = "login"
        with col2:
            if st.button("📝 Criar Conta", key="painel_btn_registro_tab_render", use_container_width=True):
                st.session_state["modo_auth_painel"] = "registro"
        st.markdown("---")

        if st.session_state["modo_auth_painel"] == "login":
            with st.form("form_login_painel_lgpd_page"):
                st.subheader("🔑 Login")
                email_login = st.text_input("E-mail*", key="login_email_painel_lgpd_key")
                senha_login = st.text_input("Senha*", type="password", key="login_senha_painel_lgpd_key")
                login_submit = st.form_submit_button("Entrar")

                if login_submit:
                    if not email_login or not senha_login:
                        st.warning("Por favor, preencha todos os campos.")
                    else:
                        sucesso, user_data = autenticar_usuario(email_login, senha_login)
                        if sucesso:
                            st.session_state["logado"] = True
                            st.session_state["email"] = user_data["email"]
                            st.session_state["tipo_usuario"] = user_data["tipo"]
                            st.session_state["nome_usuario"] = user_data["nome"]
                            st.success("✅ Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"{user_data}")
        else: # modo_auth_painel == "registro"
            with st.form("form_registro_painel_lgpd_page"):
                st.subheader("📝 Registro de Novo Usuário")
                nome_reg = st.text_input("Nome completo*", key="reg_nome_painel_key")
                cpf_reg = st.text_input("CPF ou CNPJ*", max_chars=18, key="reg_cpf_painel_key")
                telefone_reg = st.text_input("Telefone*", key="reg_telefone_painel_key")
                email_reg = st.text_input("E-mail*", key="reg_email_painel_lgpd_key")
                senha_reg = st.text_input("Senha (mínimo 6 caracteres)*", type="password", key="reg_senha_painel_key")
                senha_conf_reg = st.text_input("Confirme a senha*", type="password", key="reg_senha_conf_painel_key")
                registro_submit = st.form_submit_button("Registrar")

                if registro_submit:
                    if not all([nome_reg.strip(), cpf_reg.strip(), telefone_reg.strip(), email_reg.strip(), senha_reg.strip(), senha_conf_reg.strip()]):
                        st.warning("Por favor, preencha todos os campos obrigatórios.")
                    elif senha_reg != senha_conf_reg:
                        st.error("❌ As senhas não coincidem.")
                    elif len(senha_reg) < 6:
                        st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                    else:
                        sucesso, msg = registrar_usuario(
                            email=email_reg, senha=senha_reg, nome=nome_reg,
                            telefone=telefone_reg, cpf=cpf_reg, tipo="cidadao"
                        )
                        if sucesso:
                            st.success(msg)
                            st.session_state["modo_auth_painel"] = "login"
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg)
        exibir_rodape() # Adiciona o rodapé aqui também para páginas de login/registro
        return

    # --- Usuário Logado ---
    if not st.session_state.get("logado", False):
        st.warning("⚠️ Sessão de usuário inválida. Por favor, faça login novamente.")
        keys_to_clear_critical = ["logado", "email", "tipo_usuario", "nome_usuario", "modo_auth_painel"]
        for key_critical in keys_to_clear_critical:
            if key_critical in st.session_state:
                del st.session_state[key_critical]
        st.rerun()
        st.stop()

    usuario_logado_email = st.session_state.get("email")
    usuario_logado_nome = st.session_state.get("nome_usuario")

    if not usuario_logado_email:
        st.error("❌ Erro crítico: E-mail do usuário não encontrado na sessão após o login. Por favor, refaça o login ou contate o suporte.")
        st.stop()

    st.info(f"Bem-vindo(a) ao seu painel, {usuario_logado_nome}!")

    tab_nova, tab_minhas = st.tabs(["📨 Nova Solicitação", "📜 Minhas Solicitações"])

    with tab_nova:
        st.markdown("<h2 style='text-align: center;'>📥 Enviar Nova Solicitação LGPD</h2>", unsafe_allow_html=True)
        with st.form("form_nova_solicitacao_lgpd_tab", clear_on_submit=True):
            st.markdown("### 📋 Detalhes da Solicitação")

            user_doc_fs = db.collection("usuarios").document(usuario_logado_email).get()
            user_data_fs = user_doc_fs.to_dict() if user_doc_fs.exists else {}

            st.text_input("Nome Completo*", value=user_data_fs.get("nome", usuario_logado_nome), disabled=True, key="form_nova_sol_nome")
            st.text_input("E-mail*", value=user_data_fs.get("email", usuario_logado_email), disabled=True, key="form_nova_sol_email")
            st.text_input("CPF/CNPJ*", value=user_data_fs.get("cpf", "Não informado"), disabled=True, key="form_nova_sol_cpf")
            telefone_form = st.text_input("Telefone*", value=user_data_fs.get("telefone", "Não informado"), key="form_nova_sol_telefone")

            tipo_solicitacao = st.selectbox(
                "**Tipo de Solicitação***",
                options=["Acesso aos Dados", "Retificação de Dados", "Exclusão de Dados", "Outros"],
                index=0,
                key="form_nova_sol_tipo"
            )
            descricao_inicial = st.text_area(
                "**Descrição Detalhada da Solicitação***",
                height=200,
                placeholder="Descreva sua solicitação aqui...",
                key="form_nova_sol_descricao"
            )
            uploaded_files_nova = st.file_uploader(
                "📎 Anexar documentos (Opcional - JPG, PNG, PDF)",
                type=["jpg", "jpeg", "png", "pdf"],
                accept_multiple_files=True,
                key="form_nova_sol_anexos"
            )

            enviar_solicitacao_btn = st.form_submit_button("📤 Enviar Solicitação")

            if enviar_solicitacao_btn:
                if not descricao_inicial.strip():
                    st.error("❌ A descrição detalhada é obrigatória!")
                else:
                    try:
                        protocolo = gerar_protocolo_unico()
                        data_envio_obj = datetime.datetime.now(timezone_brasilia)
                        data_envio_iso = data_envio_obj.isoformat()
                        anexos_finais_nova = []
                        if uploaded_files_nova:
                            for uploaded_file in uploaded_files_nova:
                                file_extension = os.path.splitext(uploaded_file.name)[1]
                                unique_filename = f"{uuid.uuid4()}{file_extension}"
                                destination_path = f"anexos_solicitacoes/{protocolo}/{unique_filename}"
                                url = upload_file_to_storage(uploaded_file, destination_path)
                                if url:
                                    anexos_finais_nova.append({"nome_arquivo": uploaded_file.name, "url": url})
                                else:
                                    st.warning(f"⚠️ Falha ao enviar o arquivo: {uploaded_file.name}.")

                        nova_solicitacao_data = {
                            "protocolo": protocolo,
                            "nome_solicitante": user_data_fs.get("nome", usuario_logado_nome),
                            "email_solicitante": user_data_fs.get("email", usuario_logado_email),
                            "cpf_solicitante": user_data_fs.get("cpf", ""),
                            "telefone_solicitante": telefone_form,
                            "tipo_solicitacao": tipo_solicitacao,
                            "data_envio_inicial": data_envio_iso,
                            "status": "pendente",
                            "anexos_urls": anexos_finais_nova,
                            "historico": [{
                                "data": data_envio_iso,
                                "mensagem": descricao_inicial,
                                "remetente": "cidadao",
                                "autor_email": usuario_logado_email,
                                "autor_nome": usuario_logado_nome,
                                "anexos_mensagem_urls": anexos_finais_nova
                            }],
                            "ultima_atualizacao": firestore.SERVER_TIMESTAMP
                        }
                        db.collection("solicitacoes").document(protocolo).set(nova_solicitacao_data)
                        st.success(f"✅ Solicitação registrada com sucesso! Protocolo: **{protocolo}**")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Erro crítico ao enviar solicitação: {str(e)}")

    with tab_minhas:
        st.markdown("<h2 style='text-align: center;'>📜 Minhas Solicitações Enviadas</h2>", unsafe_allow_html=True)

        if not usuario_logado_email:
            st.error("❌ E-mail do usuário não identificado para buscar solicitações. Faça login novamente.")
            st.stop() # Adicionado st.stop() para maior segurança

        solicitacoes_query = db.collection("solicitacoes").where("email_solicitante", "==", usuario_logado_email).order_by("data_envio_inicial", direction=firestore.Query.DESCENDING)
        minhas_solicitacoes_docs = solicitacoes_query.stream()
        lista_minhas_solicitacoes = [doc.to_dict() for doc in minhas_solicitacoes_docs]

        if not lista_minhas_solicitacoes:
            st.info("ℹ️ Você ainda não enviou nenhuma solicitação.")
        else:
            status_opcoes_display = {
                "pendente": "🕒 Aguardando Resposta",
                "respondido": "🗣️ Respondido pelo IPEM",
                "resolvido": "✔️ Resolvido"
            }
            status_cores = {"pendente": "orange", "respondido": "blue", "resolvido": "green"}

            for s_data in lista_minhas_solicitacoes:
                protocolo_s = s_data.get("protocolo", f"proto_err_{uuid.uuid4().hex[:6]}")
                status_atual_s = s_data.get("status", "desconhecido")
                display_status_s = status_opcoes_display.get(status_atual_s, "🔘 Status Desconhecido")
                cor_status_s = status_cores.get(status_atual_s, "grey")
                data_para_exibir_str = s_data.get("ultima_atualizacao", s_data.get("data_envio_inicial"))

                try:
                    if isinstance(data_para_exibir_str, datetime.datetime): # Se for Timestamp do Firestore
                        # Garante que é timezone-aware (Firestore server timestamps são UTC)
                        data_obj_s = data_para_exibir_str.astimezone(timezone_brasilia) if data_para_exibir_str.tzinfo else timezone_brasilia.localize(data_para_exibir_str)
                    elif isinstance(data_para_exibir_str, str): # Se for string ISO
                        data_obj_s = datetime.datetime.fromisoformat(data_para_exibir_str).astimezone(timezone_brasilia)
                    else: # Fallback se o tipo não for esperado
                        data_obj_s = datetime.datetime.now(timezone_brasilia) # Ou outra data padrão
                        st.caption(f"Alerta: Formato de data inesperado para {protocolo_s}: {type(data_para_exibir_str)}")
                    data_formatada_s = data_obj_s.strftime('%d/%m/%Y às %H:%M')
                except Exception as e_date:
                    data_formatada_s = "Data Indisponível"
                    st.caption(f"Erro ao formatar data para {protocolo_s}: {e_date}")


                expander_title = f"**Protocolo:** {protocolo_s} | **Última Interação:** {data_formatada_s} | **Status:** <span style='color:{cor_status_s};font-weight:bold;'>{display_status_s}</span>"

                with st.expander(expander_title, expanded=False):
                    st.markdown(f"#### Detalhes da Solicitação: {protocolo_s}")
                    st.markdown(f"**Tipo:** {s_data.get('tipo_solicitacao', 'N/A')}")
                    historico_conversa_s = s_data.get("historico", [])
                    if not historico_conversa_s:
                        st.write("_Nenhuma mensagem no histórico._")
                    else:
                        st.markdown("**Histórico da Conversa:**")
                        for msg_idx, msg in enumerate(historico_conversa_s):
                            remetente_display = "👤 **Você**" if msg.get("remetente") == "cidadao" else f"🏢 **IPEM-MG ({msg.get('autor_nome', 'Admin')})**"
                            try:
                                data_msg_obj = datetime.datetime.fromisoformat(msg.get("data")).astimezone(timezone_brasilia)
                                data_msg_formatada_hist = data_msg_obj.strftime('%d/%m/%Y às %H:%M')
                            except:
                                data_msg_formatada_hist = "Data Inválida"
                            st.markdown(f"--- \n _{remetente_display} em {data_msg_formatada_hist}_:")
                            st.markdown(f"> {msg.get('mensagem', '_Mensagem vazia_')}")
                            anexos_msg_hist = msg.get("anexos_mensagem_urls", [])
                            if anexos_msg_hist:
                                with st.container(): # Usar container para melhor agrupamento visual
                                    st.markdown("_Anexos da mensagem:_")
                                    for anexo_idx, anexo_item in enumerate(anexos_msg_hist):
                                        st.markdown(f"- [{anexo_item.get('nome_arquivo', 'Ver Anexo')}]({anexo_item.get('url')})", unsafe_allow_html=True, key=f"anexo_link_{protocolo_s}_{msg_idx}_{anexo_idx}")
                        st.markdown("---")

                    if status_atual_s != "resolvido":
                        with st.form(key=f"form_continuar_solicitacao_cidadao_{protocolo_s}"): # Chave do formulário mais específica
                            nova_mensagem_cidadao = st.text_area(
                                "📝 Enviar nova mensagem ou responder:",
                                height=100,
                                key=f"form_cont_nova_msg_cidadao_input_{protocolo_s}" # Chave do widget
                            )
                            uploaded_files_continua = st.file_uploader(
                                "📎 Anexar novos arquivos (Opcional)",
                                type=["jpg", "jpeg", "png", "pdf"],
                                accept_multiple_files=True,
                                key=f"form_cont_anexos_cidadao_uploader_{protocolo_s}" # Chave do widget
                            )
                            enviar_nova_msg_btn = st.form_submit_button("📩 Enviar Mensagem")

                            if enviar_nova_msg_btn:
                                if not nova_mensagem_cidadao.strip():
                                    st.warning("⚠️ Digite sua mensagem antes de enviar.")
                                else:
                                    anexos_finais_continua = []
                                    if uploaded_files_continua:
                                        for uploaded_file_c in uploaded_files_continua:
                                            file_extension_c = os.path.splitext(uploaded_file_c.name)[1]
                                            unique_filename_c = f"{uuid.uuid4()}{file_extension_c}"
                                            destination_path_c = f"anexos_solicitacoes/{protocolo_s}/historico/{unique_filename_c}"
                                            url_c = upload_file_to_storage(uploaded_file_c, destination_path_c)
                                            if url_c:
                                                anexos_finais_continua.append({"nome_arquivo": uploaded_file_c.name, "url": url_c})
                                    nova_entrada_historico = {
                                        "data": datetime.datetime.now(timezone_brasilia).isoformat(),
                                        "mensagem": nova_mensagem_cidadao,
                                        "remetente": "cidadao",
                                        "autor_email": usuario_logado_email,
                                        "autor_nome": usuario_logado_nome,
                                        "anexos_mensagem_urls": anexos_finais_continua
                                    }
                                    db.collection("solicitacoes").document(protocolo_s).update({
                                        "historico": firestore.ArrayUnion([nova_entrada_historico]),
                                        "status": "pendente",
                                        "ultima_atualizacao": firestore.SERVER_TIMESTAMP
                                    })
                                    st.success("✅ Mensagem enviada! O IPEM foi notificado.")
                                    st.rerun()
                    else:
                        st.success("✔️ Esta solicitação foi marcada como resolvida.")
                        st.markdown("💬 _Não é possível enviar novas mensagens para solicitações resolvidas._")
                    st.markdown("---") # Separador visual para cada solicitação


def exibir_rodape():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px; font-size: 0.9em;">
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br>
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335<br>
        <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os direitos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)
