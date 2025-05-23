import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.title("⚖️ Princípios Básicos da LGPD")
    st.markdown("---")
    st.markdown("""
    A LGPD estabelece 10 princípios fundamentais que devem orientar todo tratamento de dados pessoais no IPEM-MG:
    """)
    
    # CSS para cartões com hover
    st.markdown("""
    <style>
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    .card:hover {
        background-color: #eef6ff;
        transform: translateY(-3px);
    }
    .card h4 {
        margin-top: 0;
        color: #004080;
    }
    </style>
    """, unsafe_allow_html=True)

    principios = [
        ("Finalidade", "O tratamento de dados deve ser realizado para propósitos legítimos, específicos, explícitos e informados ao titular, sem possibilidade de tratamento posterior de forma incompatível com essas finalidades. "),
        ("Adequação", "Os dados coletados devem ser compatíveis com a finalidade declarada. Se o objetivo é contato profissional, não faz sentido solicitar dados de saúde."),
        ("Necessidade", "O tratamento deve ser restrito à coleta de dados estritamente necessários ao atendimento da finalidade pretendida, evitando a coleta excessiva. "),
        ("Livre Acesso", "Os titulares devem poder acessar facilmente seus dados, saber por quanto tempo serão armazenados e como estão sendo usados."),
        ("Qualidade dos Dados", "Os dados devem ser mantidos exatos, atualizados e relevantes para o tratamento. Informações incorretas devem ser corrigidas."),
        ("Transparência", "O cidadão deve receber informações claras e acessíveis sobre como seus dados estão sendo utilizados, inclusive por terceiros."),
        ("Segurança", "O tratamento deve garantir a segurança dos dados pessoais, utilizando medidas técnicas e organizacionais adequadas para evitar danos, perdas ou acesso não autorizado. "),
        ("Prevenção", "É necessário agir proativamente para evitar que incidentes com dados ocorram, com base na análise de riscos."),
        ("Não Discriminação", "Os dados não podem ser usados para fins discriminatórios, como segmentar ou excluir pessoas de forma injusta."),
        ("Responsabilização e Prestação de Contas", "O IPEM-MG deve ser capaz de demonstrar que adota práticas de proteção de dados eficazes e auditáveis."),
    ]

    for titulo, descricao in principios:
        st.markdown(f"""
        <div class="card">
            <h4>🔹 {titulo}</h4>
            <p>{descricao}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("""
    Esses princípios visam garantir que o tratamento de dados pessoais seja feito de forma justa, transparente e responsável, protegendo os direitos dos titulares e promovendo a confiança na utilização dos dados. 
    """)

    # Rodapé
    st.markdown("""
    <hr>
    <p style="text-align: center; color: gray;">
        © 2025 IPEM-MG. Promovendo privacidade e segurança de dados. Todos os Direitos Reservados.
    </p>
    """, unsafe_allow_html=True)
