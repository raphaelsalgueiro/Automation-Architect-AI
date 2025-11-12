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
                
                # --- PROMPT REFINADO (V4.2) ---
                # Corrigida a numeração para continuar do PDD (3.3, 3.4...)
                # Corrigida a formatação dos CAs (para bullet points)
                prompt = f"""
                Você é um Analista de Requisitos Ágil especialista em projetos **Power Automate** e **Analysis**.
                Sua tarefa é traduzir o PDD (Process Design Document) em um conjunto completo de 5 artefatos de desenvolvimento.

                Gere os seguintes documentos, continuando a numeração do PDD. Comece com `3.3. Épico de Desenvolvimento`, `3.4. Requisitos Funcionais`, e assim por diante.

                ---
                ### 3.3. Épico de Desenvolvimento
                (Gere um Épico, Objetivo e Valor de Negócio, focado no que o Power Automate e o Analysis irão resolver) .

                ### 3.4. Requisitos Funcionais (RFs)
                (Gere uma lista detalhada do que o sistema DEVE fazer. Ex: "RF-01: O sistema DEVE classificar documentos...") [cite_start][cite: 88-91].

                ### 3.5. Requisitos Não Funcionais (NFRs)
                (Sugira NFRs cruciais para esta automação, focados em Segurança, Confiabilidade, Auditoria, etc.) .

                ### 3.6. Histórias de Usuário (Divididas por Função) 
                
                #### 3.6.1. Histórias de Usuário (Power Automate)
                (Gere Histórias de Usuário técnicas no formato 'Como automação [Power Automate], eu quero...').
                Exemplos:
                * "...processar dados que exigem Rateio... executando o script de input específico no SAP..." 
                * "...acessar o Unico Doc (Oracle) e inserir os metadados..." 

                #### 3.6.2. Histórias de Usuário (Analysis)
                (Gere Histórias de Usuário técnicas no formato 'Como Engenheiro de IA, eu quero...').
                Exemplos:
                * "...configurar um agente do Analysis para extrair os campos X, Y, Z."
                * "...treinar o Analysis para classificar corretamente documentos entre 'CTE' e 'FRS'." 

                ### 3.7. Critérios de Aceitação (CAs)
                (Para as Histórias de Usuário mais críticas, detalhe os CAs. **IMPORTANTE: Use listas (bullet points), NÃO use tabelas Markdown.**)
                
                Exemplo de Formato de CA (use este formato):
                **CA para US-P3 (Workflow de Aprovação):**
                * **Cenário 1: Limiar Ativado**
                    * **Dado que** o Analysis retorna o `Valor Total` de R$ 50.000,01.
                    * **Quando** o Power Automate aplica a validação R 2.1.1.
                    * **Então** o fluxo DEVE iniciar o bloco `Power Automate Approvals` e pausar a execução.
                * **Cenário 2: Limiar Desativado**
                    * **Dado que** o Analysis retorna o `Valor Total` de R$ 49.999,99.
                    * **Quando** o Power Automate aplica a validação R 2.1.1.
                    * **Então** o fluxo DEVE ignorar o bloco `Power Automate Approvals` e seguir para a próxima etapa.
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
                with st.spinner("Salvando na planilha..."):
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