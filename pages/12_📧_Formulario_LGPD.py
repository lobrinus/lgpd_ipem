# SEÇÃO RESTRITA (apenas admins logados)
if st.session_state.get("logado"):
    st.markdown("---")
    st.subheader("📁 Solicitações Recebidas")

    br_tz = pytz.timezone("America/Sao_Paulo")

    # FILTRO POR DATA
    st.markdown("### 🔎 Filtrar por data")
    data_inicio = st.date_input("Data inicial", value=datetime.now(br_tz).date())
    data_fim = st.date_input("Data final", value=datetime.now(br_tz).date())

    # Convertendo para datetime com fuso
    dt_inicio = datetime.combine(data_inicio, datetime.min.time()).astimezone(br_tz)
    dt_fim = datetime.combine(data_fim, datetime.max.time()).astimezone(br_tz)

    # Busca documentos
    solicitacoes = db.collection("solicitacoes").order_by("data_envio", direction=firestore.Query.DESCENDING).stream()

    for doc in solicitacoes:
        dados = doc.to_dict()
        data_envio = dados.get("data_envio")

        # Converter para timezone-aware se necessário
        if isinstance(data_envio, datetime):
            if data_envio.tzinfo is None:
                data_envio = data_envio.replace(tzinfo=pytz.UTC)
            data_brasil = data_envio.astimezone(br_tz)

            # Filtro por intervalo de datas
            if not (dt_inicio <= data_brasil <= dt_fim):
                continue

            with st.expander(f"🧾 Solicitação de {dados.get('nome')} em {data_brasil.strftime('%d/%m/%Y %H:%M')}"):
                st.markdown(f"**📧 E-mail:** {dados.get('email')}")
                st.markdown(f"**📞 Telefone:** {dados.get('telefone')}")
                st.markdown(f"**🆔 CPF:** {dados.get('cpf')}")
                st.markdown(f"**💬 Mensagem:** {dados.get('mensagem')}")
                st.markdown(f"**📅 Data de envio:** {data_brasil.strftime('%d/%m/%Y %H:%M')}")

                # Botão para deletar a mensagem
                if st.button(f"🗑️ Deletar mensagem de {dados.get('nome')}", key=f"del_{doc.id}"):
                    db.collection("solicitacoes").document(doc.id).delete()
                    st.success("✅ Mensagem deletada com sucesso.")
                    st.experimental_rerun()
else:
    st.info("🔐 Área restrita. Faça login como administrador para visualizar as solicitações.")
