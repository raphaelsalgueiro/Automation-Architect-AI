import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet

def run():
    st.header("📄 4. Delivery (Docs)")
    st.write("O objetivo deste módulo é traduzir o PDD em **todos** os artefatos técnicos (RFs, NFRs, USs, CAs) para a equipe de **Inovação**.")
    

    pdd_input_widget_value = st.text_area(
        "3. Design (PDD)",
        height=300,
        placeholder="Gerado pelo Módulo 3 ou colado manualmente...",
        key="delivery_pdd_input"  # Lê o valor que o M3 definiu para este 'key'
    )

    if st.button("Gerar Artefatos para Desenvolvimento"):
        if pdd_input_widget_value:
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["design_pdd"] = pdd_input_widget_value
            
            with st.spinner("Gerando a documentação técnica detalhada..."):
                
                # --- PROMPT REFINADO (V3.0) ---
                prompt = f"""
                Você é um Analista de Requisitos Ágil especialista em projetos **Power Automate** e **Analysis**.
                Sua tarefa é traduzir o PDD (Process Design Document) em um conjunto completo de 5 artefatos de desenvolvimento.

                Com base no PDD fornecido, gere os seguintes documentos:
                
                ---
                ### 3.3. Épico de Desenvolvimento 
                (Gere um Épico, Objetivo e Valor de Negócio, focado no que o Power Automate e o Analysis irão resolver) .

                ### 3.X. Requisitos Funcionais (RFs)
                [cite_start](Gere uma lista detalhada do que o sistema DEVE fazer. Ex: "RF-01: O sistema DEVE extrair os campos X, Y, Z do documento." ou "RF-02: O sistema DEVE classificar documentos entre FRS e RM" [cite: 88-91]).

                ### 3.5. Requisitos Não-Funcionais (NFRs) 
                (Sugira NFRs cruciais para esta automação).
                Exemplos:
                * NFR003 (Confiabilidade): "Retry de 3 tentativas para SAP e Unico Doc." 
                * NFR004 (Segurança): "Credenciais via Cofre de Credenciais (Vault)." 
                * NFR005 (Auditabilidade): "Log de todas as ações no Snowflake." 

                ### 3.4. Histórias de Usuário (Divididas por Função) 
                
                #### Histórias de Usuário (Power Automate)
                (Gere Histórias de Usuário técnicas no formato 'Como automação [Power Automate], eu quero...').
                Exemplos:
                * US-01: "...monitorar a caixa de entrada..." 
                * US-06: "...processar dados que exigem Rateio... executando o script de input específico no SAP..." 
                * US-09: "...acessar o Unico Doc (Oracle) e inserir os metadados..." 

                #### Histórias de Usuário (Analysis)
                (Gere Histórias de Usuário técnicas no formato 'Como Engenheiro de IA, eu quero...').
                Exemplos:
                * US-A1: "...configurar um agente do Analysis para extrair os campos X, Y, Z do Fornecedor B."
                * US-A2: "...treinar o Analysis para classificar corretamente documentos entre 'CTE' e 'FRS'." 

                ### 3.X. Critérios de Aceitação (CAs)
                (Para as 2-3 Histórias de Usuário mais críticas, detalhe os CAs no formato 'Dado que... Quando... Então...').
                Exemplo:
                * **CA para US-09 (Integração Unico Doc):**
                    * **Dado que** o Power Automate criou a FRS 12345 no SAP.
                    * **Quando** o robô acessar o Unico Doc.
                    * **Então** ele deve inserir "12345" no campo 'Número do Documento' e salvar o registro.
                ---
                
                PDD para Análise:
                ---
                {pdd_input_widget_value}
                ---
                """
                
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