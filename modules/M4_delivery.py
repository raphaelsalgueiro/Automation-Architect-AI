import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet

def run():
    st.header("📄 4. Delivery (Docs)")
    st.write("O objetivo deste módulo é traduzir o PDD em **todos** os artefatos técnicos (RFs, NFRs, USs, CAs) para as equipes de **Power Automate** e **Analysis**.")
    
    pdd_input_widget_value = st.text_area(
        "3. Design (PDD)",
        height=300,
        placeholder="Gerado pelo Módulo 3 ou colado manualmente...",
        key="delivery_pdd_input" 
    )

    if st.button("Gerar Artefatos para Desenvolvimento"):
        if pdd_input_widget_value:
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["design_pdd"] = pdd_input_widget_value
            
            with st.spinner("Gerando a documentação técnica detalhada..."):
                
                # --- INÍCIO DA ATUALIZAÇÃO (PROMPT V7.0) ---
                # Força o uso de Tabelas Markdown para consistência
                prompt = f"""
                Você é um Analista de Requisitos Ágil especialista em projetos **Power Automate** e **Analysis**.
                Sua tarefa é traduzir o PDD (Process Design Document) em um conjunto completo de 5 artefatos de desenvolvimento, formatados para clareza técnica.

                **REGRAS DE FORMATAÇÃO CRÍTICAS:**
                1.  **Numeração:** Continue a numeração do PDD. Comece EXATAMENTE com `### 3.3. Épico de Desenvolvimento`, `### 3.4. Requisitos Funcionais`, e assim por diante.
                2.  **Tabelas Markdown:** Para os Requisitos (RFs, NFRs), Histórias de Usuário (USs) e Critérios de Aceitação (CAs), use **Tabelas Markdown** para estruturar os dados. NÃO use listas ou bullet points para estes itens.

                Gere os seguintes documentos (baseado no template OUROMAR ):

                ---
                ### 3.3. Épico de Desenvolvimento
                (Gere uma tabela Markdown com: Título do Épico, Objetivo, Valor de Negócio, Escopo (In-Scope)) [cite: 180]

                ### 3.4. Requisitos Funcionais (RFs)
                (Gere uma tabela Markdown com: ID, REQUISITO FUNCIONAL. Agrupe-os por função, ex: "RFs de Coleta", "RFs de Extração") [cite: 183-192]

                ### 3.5. Requisitos Não Funcionais (NFRs)
                (Gere uma tabela Markdown com: ID, CATEGORIA, REQUISITO NÃO-FUNCIONAL) [cite: 194]

                ### 3.6. Histórias de Usuário (Divididas por Função) 
                
                #### 3.6.1. Histórias de Usuário (Power Automate)
                (Gere uma tabela Markdown com: ID, História de Usuário (Power Automate)) [cite: 201]

                #### 3.6.2. Histórias de Usuário (Analysis)
                (Gere uma tabela Markdown com: ID, História de Usuário (Analysis)) [cite: 206]

                ### 3.7. Critérios de Aceitação (CAs)
                (Gere uma tabela Markdown para os CAs mais críticos. Ex: CA para US-P4)
                (Use o formato de tabela: Condição (Dado que...), Ação (Quando...), Resultado (Então...)) [cite: 210]
                ---
                
                PDD para Análise:
                ---
                {pdd_input_widget_value}
                ---
                """
                # --- FIM DA ATUALIZAÇÃO ---
                
                response_text = call_gemini_api(prompt)
                st.session_state.clipboard["delivery_docs"] = response_text
        else:
            st.warning("O PDD do Módulo 3 está vazio. Por favor, cole ou gere o PDD primeiro.")
    
    if st.session_state.clipboard["delivery_docs"]:
        st.divider()
        st.subheader("Artefatos para a Equipe de Desenvolvimento")
        st.markdown(st.session_state.clipboard["delivery_docs"])
        
        st.divider()
        st.subheader("Salvar estes Artefatos")
        project_name_input = st.text_input(
            "Dê um nome para este conjunto de Artefatos:", 
            placeholder="Ex: Artefatos - Faturas Fornecedor X",
            key="delivery_project_name"
        )
        
        if st.button("Salvar", key="delivery_save_button"):
            if project_name_input:
                with st.spinner("Salvando..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Delivery (Artefatos)", 
                        content=st.session_state.clipboard["delivery_docs"]
                    )
                    if success:
                        st.success(f"Artefatos '{project_name_input}' salvos com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")