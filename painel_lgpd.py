import streamlit as st
import datetime
import os # Para manipulação de caminhos e extensões de arquivo
import pytz # Para fusos horários
import json # Embora não usado diretamente aqui se os segredos são dicts
import uuid # Para nomes de arquivo únicos
from firebase_admin import firestore # Apenas firestore se db já importado
# Importa as funções e variáveis necessárias de login_unificado
from login_unificado import (
    autenticar_usuario,
    registrar_usuario,
    upload_file_to_storage,
    db, # Instância do Firestore client
    timezone_brasilia # Objeto de fuso horário
)

# db e timezone_brasilia são importados de login_unificado, não precisa reinicializar aqui

def render():
    st.markdown("<h1 style='text-align: center;'>👤 Painel LGPD</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Verifica se os serviços do Firebase estão disponíveis
    if not db or not autenticar_usuario or not registrar_usuario or not upload_file_to_storage:
        st.error("❌ Ops! Um ou mais serviços essenciais (como banco de dados ou autenticação) não estão disponíveis. Verifique a configuração do Firebase e os logs.")
        st.stop() # Interrompe a execução da página se serviços críticos faltarem

    # Inicialização do estado da sessão para controle da aba de autenticação
    if "modo_auth_painel" not in st.session_state:
        st.session_state["modo_auth_painel"] = "login"

    # Se o usuário não estiver logado, mostra as opções de login/registro
    if not st.session_state.get("logado", False):
        st.subheader("Acesse ou crie sua conta para continuar")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Entrar no Painel", key="painel_btn_login_tab", use_container_width=True):
                st.session_state["modo_auth_painel"] = "login"
        with col2:
            if st.button("📝 Criar Conta", key="painel_btn_registro_tab", use_container_width=True):
                st.session_state["modo_auth_painel"] = "registro"
        st.markdown("---")

        # Aba de Login
        if st.session_state["modo_auth_painel"] == "login":
            with st.form("form_login_painel_lgpd"):
                st.subheader("🔑 Login")
                email_login = st.text_input("E-mail*", key="login_email_painel_lgpd")
                senha_login = st.text_input("Senha*", type="password", key="login_senha_painel_lgpd")
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
                            st.error(f"{user_data}") # Exibe a mensagem de erro de autenticar_usuario
        # Aba de Registro
        else: # modo_auth_painel == "registro"
            with st.form("form_registro_painel_lgpd"):
                st.subheader("📝 Registro de Novo Usuário")
                nome_reg = st.text_input("Nome completo*", key="reg_nome_painel")
                # Adicionar validação de CPF/CNPJ se necessário
                cpf_reg = st.text_input("CPF ou CNPJ*", max_chars=18, key="reg_cpf_painel")
                telefone_reg = st.text_input("Telefone*", key="reg_telefone_painel")
                email_reg = st.text_input("E-mail*", key="reg_email_painel_lgpd")
                senha_reg = st.text_input("Senha (mínimo 6 caracteres)*", type="password", key="reg_senha_painel")
                senha_conf_reg = st.text_input("Confirme a senha*", type="password", key="reg_senha_conf_painel")
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
                            email=email_reg,
                            senha=senha_reg,
                            nome=nome_reg,
                            telefone=telefone_reg,
                            cpf=cpf_reg, # Passa o CPF/CNPJ
                            tipo="cidadao" # Tipo padrão para registro via este painel
                        )
                        if sucesso:
                            st.success(msg)
                            st.session_state["modo_auth_painel"] = "login" # Muda para aba de login
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg)
        return # Interrompe a renderização do restante da página se não estiver logado

    # --- Usuário Logado ---
    # Obtém informações do usuário da sessão
    usuario_logado_email = st.session_state.get("email")
    usuario_logado_nome = st.session_state.get("nome_usuario")
    # tipo_usuario_logado = st.session_state.get("tipo_usuario") # Pode ser usado para lógicas futuras

    st.info(f"Bem-vindo(a) ao seu painel, {usuario_logado_nome}!")

    # Função para gerar protocolo (já existe em login_unificado, mas pode ser chamada daqui)
    # from login_unificado import gerar_protocolo_unico # Se movida para lá

    # Abas para "Nova Solicitação" e "Minhas Solicitações"
    tab_nova, tab_minhas = st.tabs(["📨 Nova Solicitação", "📜 Minhas Solicitações"])

    with tab_nova:
        st.markdown("<h2 style='text-align: center;'>📥 Enviar Nova Solicitação LGPD</h2>", unsafe_allow_html=True)
        with st.form("form_nova_solicitacao_lgpd", clear_on_submit=True):
            st.markdown("### 📋 Detalhes da Solicitação")

            # Busca dados do usuário no Firestore para pré-preenchimento
            # É uma boa prática buscar os dados mais recentes do DB
            user_doc_fs = db.collection("usuarios").document(usuario_logado_email).get()
            user_data_fs = user_doc_fs.to_dict() if user_doc_fs.exists else {}

            # Campos pré-preenchidos e desabilitados (ou habilitados para edição se desejado)
            st.text_input("Nome Completo*", value=user_data_fs.get("nome", usuario_logado_nome), disabled=True)
            st.text_input("E-mail*", value=user_data_fs.get("email", usuario_logado_email), disabled=True)
            # CPF/CNPJ também deve vir do Firestore e ser desabilitado
            st.text_input("CPF/CNPJ*", value=user_data_fs.get("cpf", "Não informado"), disabled=True)
            # Telefone pode ser editável se o usuário puder atualizá-lo aqui
            telefone_form = st.text_input("Telefone*", value=user_data_fs.get("telefone", "Não informado"))


            tipo_solicitacao = st.selectbox(
                "**Tipo de Solicitação***",
                options=["Acesso aos Dados", "Retificação de Dados", "Exclusão de Dados", "Outros"],
                index=0 # Primeira opção como padrão
            )
            descricao_inicial = st.text_area(
                "**Descrição Detalhada da Solicitação***",
                height=200,
                placeholder="Descreva sua solicitação aqui..."
            )
            uploaded_files_nova = st.file_uploader(
                "📎 Anexar documentos (Opcional - JPG, PNG, PDF)",
                type=["jpg", "jpeg", "png", "pdf"], # Adicionado jpeg
                accept_multiple_files=True,
                key="anexos_nova_solicitacao_painel"
            )

            enviar_solicitacao_btn = st.form_submit_button("📤 Enviar Solicitação")

            if enviar_solicitacao_btn:
                if not descricao_inicial.strip():
                    st.error("❌ A descrição detalhada é obrigatória!")
                else:
                    try:
                        # Gera protocolo usando a função de login_unificado
                        from login_unificado import gerar_protocolo_unico # Garante que está importada
                        protocolo = gerar_protocolo_unico()
                        data_envio_obj = datetime.datetime.now(timezone_brasilia)
                        data_envio_iso = data_envio_obj.isoformat()

                        anexos_finais_nova = []
                        if uploaded_files_nova:
                            for uploaded_file in uploaded_files_nova:
                                # Cria um nome de arquivo único para evitar sobrescritas
                                file_extension = os.path.splitext(uploaded_file.name)[1]
                                unique_filename = f"{uuid.uuid4()}{file_extension}"
                                destination_path = f"anexos_solicitacoes/{protocolo}/{unique_filename}"
                                url = upload_file_to_storage(uploaded_file, destination_path)
                                if url:
                                    anexos_finais_nova.append({"nome_arquivo": uploaded_file.name, "url": url})
                                else:
                                    st.warning(f"⚠️ Falha ao enviar o arquivo: {uploaded_file.name}. A solicitação continuará sem ele.")

                        nova_solicitacao_data = {
                            "protocolo": protocolo,
                            "nome_solicitante": user_data_fs.get("nome", usuario_logado_nome),
                            "email_solicitante": user_data_fs.get("email", usuario_logado_email),
                            "cpf_solicitante": user_data_fs.get("cpf", ""), # CPF/CNPJ do usuário
                            "telefone_solicitante": telefone_form, # Telefone do formulário
                            "tipo_solicitacao": tipo_solicitacao,
                            "data_envio_inicial": data_envio_iso,
                            "status": "pendente", # Status inicial
                            # "descricao_inicial": descricao_inicial, # Removido, pois o primeiro item do histórico já contém isso
                            "anexos_urls": anexos_finais_nova, # Anexos gerais da solicitação (primeira mensagem)
                            "historico": [{
                                "data": data_envio_iso,
                                "mensagem": descricao_inicial,
                                "remetente": "cidadao", # Quem enviou
                                "autor_email": usuario_logado_email,
                                "autor_nome": usuario_logado_nome,
                                "anexos_mensagem_urls": anexos_finais_nova # Anexos desta mensagem específica
                            }],
                            "ultima_atualizacao": firestore.SERVER_TIMESTAMP # Para ordenação e rastreio
                        }

                        db.collection("solicitacoes").document(protocolo).set(nova_solicitacao_data)
                        st.success(f"✅ Solicitação registrada com sucesso! Protocolo: **{protocolo}**")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Erro crítico ao enviar solicitação: {str(e)}")
                        # Considerar logar 'e' para depuração mais detalhada

    with tab_minhas:
        st.markdown("<h2 style='text-align: center;'>📜 Minhas Solicitações Enviadas</h2>", unsafe_allow_html=True)

        if not usuario_logado_email: # Verificação de segurança
            st.error("❌ E-mail do usuário não identificado. Faça login novamente.")
            st.stop()

        # Busca solicitações do usuário logado, ordenadas pela mais recente
        solicitacoes_query = db.collection("solicitacoes").where("email_solicitante", "==", usuario_logado_email).order_by("data_envio_inicial", direction=firestore.Query.DESCENDING)
        minhas_solicitacoes_docs = solicitacoes_query.stream()

        lista_minhas_solicitacoes = [doc.to_dict() for doc in minhas_solicitacoes_docs]

        if not lista_minhas_solicitacoes:
            st.info("ℹ️ Você ainda não enviou nenhuma solicitação.")
        else:
            status_opcoes_display = {
                "pendente": "🕒 Aguardando Resposta",
                "respondido": "🗣️ Respondido pelo IPEM", # Admin respondeu
                "resolvido": "✔️ Resolvido"
            }
            status_cores = {"pendente": "orange", "respondido": "blue", "resolvido": "green"}

            for s_data in lista_minhas_solicitacoes:
                protocolo_s = s_data.get("protocolo", "N/A")
                status_atual_s = s_data.get("status", "desconhecido")
                display_status_s = status_opcoes_display.get(status_atual_s, "🔘 Status Desconhecido")
                cor_status_s = status_cores.get(status_atual_s, "grey")

                # Usa a data da última atualização para exibição, ou a data de envio inicial
                data_para_exibir_str = s_data.get("ultima_atualizacao") # Pode ser um Timestamp do Firestore
                if not isinstance(data_para_exibir_str, datetime.datetime): # Se não for datetime (ex: string ISO ou None)
                    data_para_exibir_str = s_data.get("data_envio_inicial")

                try:
                    if isinstance(data_para_exibir_str, datetime.datetime): # Se já for datetime (do server timestamp)
                        data_obj_s = data_para_exibir_str.astimezone(timezone_brasilia) if data_para_exibir_str.tzinfo else timezone_brasilia.localize(data_para_exibir_str)
                    else: # Se for string ISO
                        data_obj_s = datetime.datetime.fromisoformat(data_para_exibir_str).astimezone(timezone_brasilia)
                    data_formatada_s = data_obj_s.strftime('%d/%m/%Y às %H:%M')
                except:
                    data_formatada_s = "Data Indisponível"


                expander_title = f"**Protocolo:** {protocolo_s} | **Última Interação:** {data_formatada_s} | **Status:** <span style='color:{cor_status_s};font-weight:bold;'>{display_status_s}</span>"

                with st.expander(expander_title, expanded=False):
                    st.markdown(f"#### Detalhes da Solicitação: {protocolo_s}")
                    st.markdown(f"**Tipo:** {s_data.get('tipo_solicitacao', 'N/A')}")

                    historico_conversa_s = s_data.get("historico", [])
                    if not historico_conversa_s:
                        st.write("_Nenhuma mensagem no histórico._")
                    else:
                        st.markdown("**Histórico da Conversa:**")
                        for msg in historico_conversa_s:
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
                                with st.container():
                                    st.markdown("_Anexos da mensagem:_")
                                    for anexo_item in anexos_msg_hist:
                                        st.markdown(f"- [{anexo_item.get('nome_arquivo', 'Ver Anexo')}]({anexo_item.get('url')})", unsafe_allow_html=True)
                        st.markdown("---")

                    # Permite ao cidadão enviar nova mensagem se não estiver resolvido
                    if status_atual_s != "resolvido":
                        with st.form(key=f"form_continuar_solicitacao_{protocolo_s}"):
                            nova_mensagem_cidadao = st.text_area(
                                "📝 Enviar nova mensagem ou responder:",
                                height=100,
                                key=f"nova_msg_cidadao_continua_{protocolo_s}"
                            )
                            uploaded_files_continua = st.file_uploader(
                                "📎 Anexar novos arquivos (Opcional)",
                                type=["jpg", "jpeg", "png", "pdf"],
                                accept_multiple_files=True,
                                key=f"anexos_continua_cidadao_{protocolo_s}"
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
                                            else:
                                                st.warning(f"⚠️ Falha ao enviar o arquivo: {uploaded_file_c.name}.")

                                    nova_entrada_historico = {
                                        "data": datetime.datetime.now(timezone_brasilia).isoformat(),
                                        "mensagem": nova_mensagem_cidadao,
                                        "remetente": "cidadao",
                                        "autor_email": usuario_logado_email,
                                        "autor_nome": usuario_logado_nome,
                                        "anexos_mensagem_urls": anexos_finais_continua
                                    }
                                    # Atualiza o Firestore
                                    db.collection("solicitacoes").document(protocolo_s).update({
                                        "historico": firestore.ArrayUnion([nova_entrada_historico]), # Adiciona ao array
                                        "status": "pendente", # Volta para pendente para o admin revisar
                                        "ultima_atualizacao": firestore.SERVER_TIMESTAMP
                                    })
                                    st.success("✅ Mensagem enviada! O IPEM foi notificado.")
                                    st.rerun()
                        # Botão para o cidadão marcar como resolvido (se ele mesmo puder fazer isso)
                        # Conforme sua descrição, apenas o admin marca como resolvido.
                        # Se o cidadão também puder, descomente e ajuste:
                        # if st.button(f"✔️ Marcar como Resolvido por Mim", key=f"cidadao_resolve_{protocolo_s}"):
                        #     db.collection("solicitacoes").document(protocolo_s).update({
                        #         "status": "resolvido",
                        #         "ultima_atualizacao": firestore.SERVER_TIMESTAMP,
                        #         "resolvido_por": "cidadao" # Adiciona quem resolveu
                        #     })
                        #     st.success(f"✅ Solicitação {protocolo_s} marcada como resolvida por você.")
                        #     st.rerun()

                    else: # Status é "resolvido"
                        st.success("✔️ Esta solicitação foi marcada como resolvida.")
                        st.markdown("💬 _Não é possível enviar novas mensagens para solicitações resolvidas._")
                    st.markdown("---") # Separador visual para cada solicitação
