import streamlit as st

def render():
    st.title("⚖️ Princípios Básicos da LGPD")
    st.markdown("---")
    st.markdown("""
    A LGPD estabelece 10 princípios fundamentais que devem orientar todo tratamento de dados pessoais no IPEM-MG:
    """)

    principios = [
        ("Finalidade", "O tratamento de dados deve ser realizado para propósitos legítimos, específicos, explícitos e informados ao titular, sem possibilidade de tratamento posterior de forma incompatível com essas finalidades."),
        ("Adequação", "Os dados coletados devem ser compatíveis com a finalidade declarada. Se o objetivo é contato profissional, não faz sentido solicitar dados de saúde."),
        ("Necessidade", "O tratamento deve ser restrito à coleta de dados estritamente necessários ao atendimento da finalidade pretendida, evitando a coleta excessiva."),
        ("Livre Acesso", "Os titulares devem poder acessar facilmente seus dados, saber por quanto tempo serão armazenados e como estão sendo usados."),
        ("Qualidade dos Dados", "Os dados devem ser mantidos exatos, atualizados e relevantes para o tratamento. Informações incorretas devem ser corrigidas."),
        ("Transparência", "O cidadão deve receber informações claras e acessíveis sobre como seus dados estão sendo utilizados, inclusive por terceiros."),
        ("Segurança", "O tratamento deve garantir a segurança dos dados pessoais, utilizando medidas técnicas e organizacionais adequadas para evitar danos, perdas ou acesso não autorizado."),
        ("Prevenção", "É necessário agir proativamente para evitar que incidentes com dados ocorram, com base na análise de riscos."),
        ("Não Discriminação", "Os dados não podem ser usados para fins discriminatórios, como segmentar ou excluir pessoas de forma injusta."),
        ("Responsabilização e Prestação de Contas", "O IPEM-MG deve ser capaz de demonstrar que adota práticas de proteção de dados eficazes e auditáveis."),
    ]

    for titulo, descricao in principios:
        with st.container():
            st.subheader(f"🔹 {titulo}")
            st.markdown(descricao)
            st.markdown("---")

    st.info("""
    Esses princípios visam garantir que o tratamento de dados pessoais seja feito de forma justa, transparente e responsável, protegendo os direitos dos titulares e promovendo a confiança na utilização dos dados.
    """)

    # Rodapé simples
    st.caption("© 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.")
