import streamlit as st
import datetime
import pytz # Para fusos horários
import os # Para manipulação de caminhos e extensões de arquivo
import uuid # Para nomes de arquivo únicos
from firebase_admin import firestore # Apenas firestore se db já importado
# Importa as funções e variáveis necessárias de login_unificado
from login_unificado import (
    db, # Instância do Firestore client
    timezone_brasilia, # Objeto de fuso horário
    upload_file_to_storage # Função para upload de arquivos
)

def render():
    st.markdown("<h1 style='text-align: center;'>Painel Administrador (Administração)</h1>", unsafe_allow_html=True)

    # Verifica se os serviços do Firebase estão disponíveis
    if not db or not upload_file_to_storage: # A autenticação é verificada pela sessão
        st.error("❌ Ops! Um ou mais serviços essenciais (como banco de dados ou armazenamento) não estão disponíveis. Verifique a configuração do Firebase e os logs.")
        st.stop()

    # --- Controle de Acesso: Apenas Administradores ---
    if not st.session_state.get("logado", False) or st.session_state.get("tipo_usuario") != "admin":
        st.error("🚫 Acesso Negado! Esta página é exclusiva para administradores.")
        st.info("➡️ Por favor, faça login como administrador para visualizar as solicitações.")
        # Adicionar um botão para redirecionar para a página de login principal, se houver
        # Exemplo: if st.button("Ir para Login"): st.switch_page("login_principal")
        return # Interrompe a renderização

    # Informações do administrador logado
    admin_nome = st.session_state.get("nome_usuario", "Admin")
    admin_email = st.session_state.get("email", "N/A")
    st.success(f"🔑 Logado como Administrador: {admin_nome} ({admin_email})")
    st.markdown("---")

    st.markdown("## 🔍 Filtro e Visualização de Solicitações")

    # --- Controles de Filtragem ---
    col_filtro1, col_filtro2, col_filtro_btn = st.columns([2,2,1])
    with col_filtro1:
        filtro_campo = st.selectbox(
            "Buscar por:",
            ["Todas", "Protocolo", "Nome do Solicitante", "CPF do Solicitante", "Status"],
            key="admin_filtro_campo_tipo"
        )
    termo_busca_admin = ""
    if filtro_campo != "Todas":
        with col_filtro2:
            if filtro_campo == "Status":
                termo_busca_admin = st.selectbox(
                    "Selecione o Status:",
                    ["pendente", "respondido", "resolvido"], # Valores exatos do status
                    key="admin_termo_busca_status_select"
                )
            else:
                termo_busca_admin = st.text_input(f"Digite o {filtro_campo}:", key="admin_termo_busca_texto_input")

    with col_filtro_btn:
        st.write("") # Espaçador para alinhar o botão
        st.write("")
        if st.button("🔄 Atualizar", key="admin_btn_atualizar_lista", use_container_width=True):
            st.rerun()

    # --- Busca de Solicitações no Firestore ---
    solicitacoes_ref_fs = db.collection("solicitacoes")

    # Aplica filtros de consulta do Firestore quando possível
    if termo_busca_admin:
        if filtro_campo == "Protocolo":
            # Firestore é case-sensitive para IDs de documento (protocolo)
            solicitacoes_ref_fs = solicitacoes_ref_fs.where("protocolo", "==", termo_busca_admin.strip())
        elif filtro_campo == "Status":
            solicitacoes_ref_fs = solicitacoes_ref_fs.where("status", "==", termo_busca_admin)
        # Para Nome e CPF, a filtragem será feita no lado do cliente (Python)
        # pois o Firestore não suporta 'contains' ou 'like' de forma nativa e eficiente para todos os casos.
        # Se houver muitos dados, considere usar um serviço de busca como Algolia.

    # Ordena as solicitações (ex: pela última atualização ou data de envio inicial)
    # Usar "ultima_atualizacao" para ver as mais recentes primeiro
    query_ordenada = solicitacoes_ref_fs.order_by("ultima_atualizacao", direction=firestore.Query.DESCENDING)
    solicitacoes_docs_fs = query_ordenada.stream()

    lista_solicitacoes_admin = []
    for doc_fs in solicitacoes_docs_fs:
        data_s = doc_fs.to_dict()
        data_s["id_doc"] = doc_fs.id # O ID do documento é o protocolo

        # Filtragem no lado do cliente para campos que não usam '==' no Firestore
        if termo_busca_admin:
            if filtro_campo == "Nome do Solicitante":
                if termo_busca_admin.lower() not in data_s.get("nome_solicitante", "").lower():
                    continue # Pula este documento
            elif filtro_campo == "CPF do Solicitante": # Geralmente busca exata, mas pode ser parcial
                if termo_busca_admin not in data_s.get("cpf_solicitante", ""):
                    continue # Pula este documento

        lista_solicitacoes_admin.append(data_s)

    if not lista_solicitacoes_admin:
        st.info("ℹ️ Nenhuma solicitação encontrada com os filtros aplicados.")
        return

    # --- Exibição das Solicitações ---
    status_opcoes_display_admin = {
        "pendente": "🕒 Pendente de Resposta",
        "respondido": "🗣️ Respondido ao Cidadão",
        "resolvido": "✔️ Resolvido"
    }
    status_cores_admin = {"pendente": "orange", "respondido": "blue", "resolvido": "green"}

    for s_data_admin in lista_solicitacoes_admin:
        protocolo_admin = s_data_admin.get("id_doc", "N/A")
        status_atual_admin = s_data_admin.get("status", "desconhecido")
        display_status_admin = status_opcoes_display_admin.get(status_atual_admin, "🔘 Status Desconhecido")
        cor_status_admin = status_cores_admin.get(status_atual_admin, "grey")
        nome_solicitante_admin = s_data_admin.get("nome_solicitante", "N/A")

        # Data para exibição no expander (última interação)
        data_interacao_admin_str = s_data_admin.get("ultima_atualizacao") # Pode ser Timestamp
        if not isinstance(data_interacao_admin_str, datetime.datetime):
            data_interacao_admin_str = s_data_admin.get("data_envio_inicial")

        try:
            if isinstance(data_interacao_admin_str, datetime.datetime):
                data_obj_admin = data_interacao_admin_str.astimezone(timezone_brasilia) if data_interacao_admin_str.tzinfo else timezone_brasilia.localize(data_interacao_admin_str)
            else:
                data_obj_admin = datetime.datetime.fromisoformat(data_interacao_admin_str).astimezone(timezone_brasilia)
            data_formatada_admin = data_obj_admin.strftime('%d/%m/%Y às %H:%M')
        except:
            data_formatada_admin = "Data Indisponível"

        expander_title_admin = (f"**Protocolo:** {protocolo_admin} | **Solicitante:** {nome_solicitante_admin} | "
                                f"**Última Interação:** {data_formatada_admin} | "
                                f"**Status:** <span style='color:{cor_status_admin};font-weight:bold;'>{display_status_admin}</span>")

        with st.expander(expander_title_admin, expanded=False):
            st.markdown(f"#### Detalhes da Solicitação: {protocolo_admin}")
            st.markdown(f"**👤 Nome do Solicitante:** {s_data_admin.get('nome_solicitante', '---')}")
            st.markdown(f"**📧 E-mail:** {s_data_admin.get('email_solicitante', '---')}")
            st.markdown(f"**🪪 CPF/CNPJ:** {s_data_admin.get('cpf_solicitante', '---')}")
            st.markdown(f"**📞 Telefone:** {s_data_admin.get('telefone_solicitante', '---')}")
            st.markdown(f"**📄 Tipo de Solicitação:** {s_data_admin.get('tipo_solicitacao', '---')}")

            try:
                data_envio_obj_admin = datetime.datetime.fromisoformat(s_data_admin.get("data_envio_inicial")).astimezone(timezone_brasilia)
                data_envio_formatada_admin = data_envio_obj_admin.strftime('%d/%m/%Y às %H:%M')
                st.markdown(f"**📅 Data da Solicitação Inicial:** {data_envio_formatada_admin}")
            except:
                st.markdown(f"**📅 Data da Solicitação Inicial:** Data Inválida")

            anexos_iniciais_admin = s_data_admin.get("anexos_urls", [])
            if anexos_iniciais_admin:
                st.markdown("**📎 Anexos Iniciais da Solicitação:**")
                for anexo_ini in anexos_iniciais_admin:
                    st.markdown(f"- [{anexo_ini.get('nome_arquivo', 'Ver Anexo')}]({anexo_ini.get('url')})", unsafe_allow_html=True)
            st.markdown("---")

            st.subheader("📜 Histórico da Conversa:")
            historico_conversa_admin = s_data_admin.get("historico", [])
            if not historico_conversa_admin:
                st.info("Nenhuma mensagem no histórico ainda.")
            else:
                for msg_hist in historico_conversa_admin:
                    remetente_display_hist = f"👤 **{msg_hist.get('autor_nome', 'Cidadão')}**" if msg_hist.get("remetente") == "cidadao" else f"🏢 **{msg_hist.get('autor_nome', 'Admin')} (IPEM-MG)**"
                    try:
                        data_msg_obj_hist = datetime.datetime.fromisoformat(msg_hist.get("data")).astimezone(timezone_brasilia)
                        data_msg_formatada_hist_view = data_msg_obj_hist.strftime('%d/%m/%Y às %H:%M')
                    except:
                        data_msg_formatada_hist_view = "Data Inválida"

                    st.markdown(f"--- \n _{remetente_display_hist} em {data_msg_formatada_hist_view}_:")
                    st.markdown(f"> {msg_hist.get('mensagem', '_Mensagem vazia_')}")

                    anexos_msg_hist_view = msg_hist.get("anexos_mensagem_urls", [])
                    if anexos_msg_hist_view:
                        with st.container():
                            st.markdown("_Anexos da mensagem:_")
                            for anexo_msg_item_view in anexos_msg_hist_view:
                                st.markdown(f"- [{anexo_msg_item_view.get('nome_arquivo', 'Ver Anexo')}]({anexo_msg_item_view.get('url')})", unsafe_allow_html=True)
                st.markdown("---")

            # --- Ações do Administrador: Responder e Marcar como Resolvido ---
            if status_atual_admin != "resolvido":
                st.subheader("📬 Responder ao Cidadão / Adicionar Observação")
                with st.form(key=f"form_resposta_admin_panel_{protocolo_admin}"):
                    nova_resposta_txt_admin = st.text_area(
                        "Digite sua resposta ou observação:",
                        key=f"resp_txt_admin_{protocolo_admin}",
                        height=150
                    )
                    uploaded_files_admin_resp = st.file_uploader(
                        "📎 Anexar arquivos à resposta (Opcional)",
                        type=["jpg", "jpeg", "png", "pdf"],
                        accept_multiple_files=True,
                        key=f"anexos_admin_resp_panel_{protocolo_admin}"
                    )

                    col_btn_resp, col_btn_resolv = st.columns(2)
                    with col_btn_resp:
                        enviar_resposta_admin_btn = st.form_submit_button("💬 Enviar Resposta ao Cidadão", use_container_width=True)
                    with col_btn_resolv:
                        marcar_resolvido_admin_btn = st.form_submit_button("✔️ Marcar Como Resolvido", use_container_width=True)

                    if enviar_resposta_admin_btn:
                        if not nova_resposta_txt_admin.strip():
                            st.warning("⚠️ Digite uma resposta antes de enviar.")
                        else:
                            anexos_finais_admin_resp = []
                            if uploaded_files_admin_resp:
                                for uploaded_file_ar in uploaded_files_admin_resp:
                                    file_extension_ar = os.path.splitext(uploaded_file_ar.name)[1]
                                    unique_filename_ar = f"{uuid.uuid4()}{file_extension_ar}"
                                    destination_path_ar = f"anexos_solicitacoes/{protocolo_admin}/admin_resp/{unique_filename_ar}"
                                    url_ar = upload_file_to_storage(uploaded_file_ar, destination_path_ar)
                                    if url_ar:
                                        anexos_finais_admin_resp.append({"nome_arquivo": uploaded_file_ar.name, "url": url_ar})

                            nova_entrada_hist_admin = {
                                "data": datetime.datetime.now(timezone_brasilia).isoformat(),
                                "mensagem": nova_resposta_txt_admin.strip(),
                                "remetente": "admin",
                                "autor_email": admin_email,
                                "autor_nome": admin_nome,
                                "anexos_mensagem_urls": anexos_finais_admin_resp
                            }
                            db.collection("solicitacoes").document(protocolo_admin).update({
                                "historico": firestore.ArrayUnion([nova_entrada_hist_admin]),
                                "status": "respondido", # Cidadão recebeu uma resposta
                                "ultima_atualizacao": firestore.SERVER_TIMESTAMP
                            })
                            st.success(f"✅ Resposta enviada para o protocolo {protocolo_admin}.")
                            st.rerun()

                    if marcar_resolvido_admin_btn:
                        # Adiciona uma nota final ao histórico se houver texto, ou uma nota padrão
                        mensagem_resolucao = nova_resposta_txt_admin.strip() if nova_resposta_txt_admin.strip() else "Solicitação marcada como resolvida pelo administrador."
                        
                        anexos_finais_admin_resolv = []
                        if uploaded_files_admin_resp: # Se houver anexos ao marcar como resolvido
                             for uploaded_file_ar_res in uploaded_files_admin_resp:
                                file_extension_ar_res = os.path.splitext(uploaded_file_ar_res.name)[1]
                                unique_filename_ar_res = f"{uuid.uuid4()}{file_extension_ar_res}"
                                destination_path_ar_res = f"anexos_solicitacoes/{protocolo_admin}/admin_resolve/{unique_filename_ar_res}"
                                url_ar_res = upload_file_to_storage(uploaded_file_ar_res, destination_path_ar_res)
                                if url_ar_res:
                                    anexos_finais_admin_resolv.append({"nome_arquivo": uploaded_file_ar_res.name, "url": url_ar_res})


                        entrada_resolvido_hist = {
                            "data": datetime.datetime.now(timezone_brasilia).isoformat(),
                            "mensagem": mensagem_resolucao,
                            "remetente": "admin",
                            "autor_email": admin_email,
                            "autor_nome": admin_nome,
                            "anexos_mensagem_urls": anexos_finais_admin_resolv
                        }
                        db.collection("solicitacoes").document(protocolo_admin).update({
                            "status": "resolvido",
                            "historico": firestore.ArrayUnion([entrada_resolvido_hist]),
                            "ultima_atualizacao": firestore.SERVER_TIMESTAMP,
                            "data_resolucao": firestore.SERVER_TIMESTAMP # Data específica da resolução
                        })
                        st.success(f"✅ Protocolo {protocolo_admin} marcado como Resolvido.")
                        st.balloons()
                        st.rerun()
            else: # Status é "resolvido"
                st.success("✔️ Esta solicitação já foi resolvida.")
                st.markdown("💬 _Não é possível enviar novas respostas ou alterar o status de solicitações resolvidas._")
            st.markdown("---") # Separador visual para cada solicitação
