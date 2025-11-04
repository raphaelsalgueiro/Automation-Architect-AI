import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("🔄 7. Refinar (Adaptação)")
    st.write("O objetivo deste módulo é adaptar um projeto existente (PDD ou User Stories) para um novo cenário (ex: novo fornecedor, novo sistema), gerando uma 'Análise de Impacto' das mudanças.")
    st.info("Este é um fluxo 'fast-track' que não segue as etapas 1-6.")

    col1, col2 = st.columns(2)

    with col1:
        original_automation = st.text_area(
            "Cole o PDD ou as User Stories da Automação Original aqui:",
            height=400,
            placeholder="Ex: PDD do processo de criação de cliente no CRM para Fornecedor A..."
        )
    
    with col2:
        new_requirements = st.text_area(
            "Descreva as Mudanças / Novas Regras de Negócio:",
            height=400,
            placeholder="Ex: Adaptar para Fornecedor B. Diferenças: Sistema SAP (não Oracle), layout do PDF diferente, adicionar validação com Compras."
        )

    if st.button("Gerar Análise de Impacto e Adaptação"):
        if original_automation and new_requirements:
            with st.spinner("Analisando o original e aplicando as modificações..."):
                
                prompt = f"""
                Você é um Arquiteto de Soluções Sênior. Sua tarefa é analisar o 'Documento Original' (um PDD ou lista de User Stories) e compará-lo com as 'Novas Regras de Negócio' de um cenário similar.

                NÃO gere um novo PDD completo. Em vez disso, gere uma **"Análise de Impacto e Lista de Adaptações"**.
                
                O seu relatório deve:
                1.  **Identificar** quais seções/módulos do documento original são impactados (ex: Extração de Dados, Interação com Sistema, Tratamento de Exceções).
                2.  **Descrever** o impacto (ex: Alto, Médio, Baixo).
                3.  **Listar** as adaptações específicas necessárias (ex: "A lógica de extração de PDF deve ser refeita para DOCX", "A interação com Salesforce deve ser substituída por T-Codes do SAP").
                4.  **Identificar** funcionalidades que são 100% novas.

                Documento Original:
                ---
                {original_automation}
                ---

                Novas Regras de Negócio / Mudanças:
                ---
                {new_requirements}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Análise de Impacto e Lista de Adaptações")
                st.markdown(response_text)
        else:
            st.warning("Por favor, preencha ambos os campos: Automação Original e Novos Requisitos.")