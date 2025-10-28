import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("🔄 Refinar Automação Existente")
    st.write("Cole uma automação existente (PDD ou User Stories) e descreva as mudanças necessárias para adaptá-la a um novo cenário.")

    col1, col2 = st.columns(2)

    with col1:
        original_automation = st.text_area(
            "Cole o PDD ou as User Stories da Automação Original aqui:",
            height=400,
            placeholder="Ex: PDD do processo de criação de cliente no CRM para Fornecedor A..."
        )
    
    with col2:
        new_requirements = st.text_area(
            "Descreva as Mudanças / Novos Requisitos:",
            height=400,
            placeholder="Ex: Adaptar para Fornecedor B. Diferenças: Sistema SAP (não Oracle), layout do PDF diferente, adicionar validação com Compras."
        )

    if st.button("Refinar Automação"):
        if original_automation and new_requirements:
            with st.spinner("Analisando o original e aplicando as modificações..."):
                prompt = f"""
                Você é um Arquiteto de Soluções e Analista de Requisitos Sênior.
                Sua tarefa é refinar um documento de automação existente (PDD ou User Stories) com base em novos requisitos.

                Analise o documento original abaixo e as modificações solicitadas. Gere uma nova versão do documento que incorpore as mudanças de forma coesa, mantendo a estrutura e o detalhamento do original. Se possível, destaque ou liste as principais alterações realizadas.

                Documento Original:
                ---
                {original_automation}
                ---

                Modificações Solicitadas:
                ---
                {new_requirements}
                ---
                """
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Versão Refinada da Automação")
                st.markdown(response_text)
        else:
            st.warning("Por favor, preencha ambos os campos: Automação Original e Novos Requisitos.")