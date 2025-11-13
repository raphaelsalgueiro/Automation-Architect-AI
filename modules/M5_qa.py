import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet

def run():
    st.header("🧪 5. QA & Testes")
    st.write("O objetivo deste módulo é gerar um Plano de Testes (UAT) completo com base no PDD, focado em **Power Automate** e **Analysis**.")

    pdd_input_widget_value = st.text_area(
        "3. Design (PDD)",
        height=300,
        placeholder="Gerado pelo Módulo 3 ou colado manualmente...",
        key="qa_pdd_input" 
    )

    if st.button("Gerar Cenários de Teste (UAT)"):
        if pdd_input_widget_value:
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["design_pdd"] = pdd_input_widget_value
            
            with st.spinner("Elaborando o plano de testes..."):
                
                # --- INÍCIO DA ATUALIZAÇÃO (LIMPEZA DE CITAÇÃO V7.1) ---
                prompt = f"""
                Você é um Engenheiro de QA (Quality Assurance) Sênior, especialista em automação com **Power Automate** e **Analysis**.
                Sua tarefa é criar um plano de testes (UAT) com base no PDD (Fluxo 'To-Be'), seguindo a estrutura da Seção 4 do documento de governança.

                **REGRAS DE FORMATAÇÃO CRÍTICAS:**
                1.  **Tabelas Markdown:** Você DEVE usar Tabelas Markdown para estruturar todos os cenários de teste. NÃO use listas ou bullet points.
                2.  **Estrutura:** Siga a estrutura de colunas do template OUROMAR (ID, CENÁRIO, OBJETIVO, CRITÉRIOS/RESULTADO).

                Crie as seguintes seções:

                ---
                ### 4.1. Testes de Caminho Feliz (Happy Path) 
                (Gere uma tabela Markdown com: ID, CENÁRIO DE TESTE, OBJETIVO, CRITÉRIOS DE SUCESSO (E2E))
                (Ex: HP-01: Processamento E2E Completo, HP-02: Consolidação de CTEs)

                ### 4.2. Testes Negativos (Validação de Dados) 
                (Gere uma tabela Markdown com: ID, CENÁRIO DE TESTE, OBJETIVO, AÇÃO ESPERADA (RESULTADO))
                (Ex: NEG-01: Anexo Corrompido, NEG-02: Dados Incompletos)
                
                ### 4.3. Testes de Exceção (Resiliência do Sistema) 
                (Gere uma tabela Markdown com: ID, CENÁRIO DE TESTE, OBJETIVO, FLUXO DE EXCEÇÃO ATIVADO)
                (Ex: EXC-01: Baixa Confiança (Analysis), EXC-02: Erro de Lançamento no SAP)
                ---
                
                Fluxo de Processo 'To-Be' para Análise:
                ---
                {pdd_input_widget_value}
                ---
                """
                # --- FIM DA ATUALIZAÇÃO ---
                
                response_text = call_gemini_api(prompt)
                st.session_state.clipboard["qa_plano"] = response_text
        else:
            st.warning("O PDD do Módulo 3 está vazio. Por favor, cole ou gere o PDD primeiro.")
    
    if st.session_state.clipboard.get("qa_plano"):
        st.divider()
        st.subheader("Plano de Testes Sugerido (UAT)")
        st.markdown(st.session_state.clipboard["qa_plano"])
        
        st.divider()
        st.subheader("Salvar este Plano de Testes")
        project_name_input = st.text_input(
            "Dê um nome para este Plano de Testes:", 
            placeholder="Ex: Plano de Testes - Faturas Fornecedor X",
            key="qa_project_name"
        )
        
        if st.button("Salvar", key="qa_save_button"):
            if project_name_input:
                with st.spinner("Salvando..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="QA (Plano de Testes)", 
                        content=st.session_state.clipboard["qa_plano"]
                    )
                    if success:
                        st.success(f"Plano de Testes '{project_name_input}' salvo com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")