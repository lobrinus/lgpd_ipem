import streamlit as st
from login_unificado import autenticar_usuario, registrar_usuario

def render():
    st.markdown("""
    <h1 style='text-align: center;'>✅ O Que Fazer e Não Fazer</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")  
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ O Que Fazer")
        st.markdown("""
        - Coletar apenas dados necessários para a finalidade declarada
        - Manter os dados atualizados e precisos
        - Armazenar em ambiente seguro com acesso controlado
        - Excluir dados quando não forem mais necessários
        - Registrar todas as operações de tratamento
        - Comunicar incidentes ao Encarregado imediatamente
        - Usar canais seguros para compartilhar dados
        - Solicitar orientação em caso de dúvidas
        """)
    
    with col2:
        st.subheader("❌ O Que Não Fazer")
        st.markdown("""
        - Coletar dados sem base legal ou consentimento
        - Manter dados além do tempo necessário
        - Armazenar em locais não autorizados (ex: pendrives)
        - Compartilhar dados sem verificar a necessidade
        - Enviar dados por e-mail não criptografado
        - Ignorar solicitações de titulares
        - Deixar sistemas desprotegidos ou sem senha
        - Tentar esconder violações ou incidentes
        """)
    
    st.markdown("---")
    st.subheader("Situações Comuns")
    st.markdown("""
    <strong>Recebimento de solicitação de titular:</strong><br>
    ✅ Encaminhar imediatamente ao Encarregado<br>
    ❌ Tentar resolver por conta própria ou ignorar<br><br>
    
    <strong>Identificação de dado desatualizado:</strong><br>
    ✅ Atualizar ou marcar para correção<br>
    ❌ Manter o dado incorreto no sistema<br><br>
    
    <strong>Necessidade de compartilhar dados com terceiro:</strong><br>
    ✅ Verificar contrato/cláusula de proteção<br>
    ❌ Enviar sem medidas de segurança adequadas<br><br>
    
    <strong>Descoberta de violação:</strong><br>
    ✅ Comunicar imediatamente ao DPO<br>
    ❌ Tentar resolver sem registro ou tentar esconder
    """, unsafe_allow_html=True)

    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 40px;">
        © 2025 IPEM-MG. Todos os direitos reservados.<br>
        R. Cristiano França Teixeira Guimarães, 80 - Cinco, Contagem - MG, 32010-130<br> 
        CNPJ: 17.322.264/0001-64 | Telefone:  (31) 3399-7134 / 08000 335 335
    </div>
    """, unsafe_allow_html=True)
