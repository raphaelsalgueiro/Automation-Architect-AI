import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet

def run():
    st.header("✍️ 3. Design (TO-BE)")
    st.write("O objetivo deste módulo é detalhar a 'Arquitetura da Solução' em um PDD (Fluxo TO-BE), com tarefas claras para **Power Automate** e **Analysis**.")
    
    col1, col2 = st.columns(2)
    with col1:
        as_is_context = st.text_area(
            "1. Diagnóstico (AS-IS) (Contexto)",
            value=st.session_state.clipboard.get("diagnostico_asis", ""),
            height=300,
            placeholder="Cole o Diagnóstico AS-IS (M1)..."
        )
    with col2:
        solution_choice = st.text_area(
            "2. Arquitetura da Solução (Input)",
            value=st.session_state.clipboard.get("arquitetura_solucao", ""),
            height=300,
            placeholder="Cole a Arquitetura (M2)..."
        )

    if st.button("Desenhar Fluxo da Automação (PDD)"):
        if as_is_context and solution_choice:
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["diagnostico_asis"] = as_is_context
            st.session_state.clipboard["arquitetura_solucao"] = solution_choice

            with st.spinner("Desenhando o fluxo do processo TO-BE..."):
                
                # --- PROMPT REFINADO (V3.0) ---
                prompt = f"""
                Você é um Arquiteto de Soluções de Automação Sênior, especialista em PDDs para **Power Automate** e **Analysis**.
                Sua tarefa é criar um PDD detalhado (Process Design Document) com foco no fluxo "To-Be", seguindo a estrutura da Seção 3.1 e 3.2 do documento de governança .

                O PDD gerado deve conter:
                
                ---
                ### 3.1. Visão da Solução e Processo Futuro (TO-BE) 
                (Descreva o novo fluxo, como ele resolve as lacunas usando Power Automate e Analysis) .

                ### 3.2. Design Técnico Detalhado (TO-BE) 
                (Divida o design em duas responsabilidades claras):

                #### 3.2.1. Fluxo de Orquestração (Power Automate)
                (Descreva o fluxo passo a passo detalhado do Power Automate (Cloud e Desktop).
                Exemplo:
                * **Fase 1: Monitoramento (Cloud):** Monitora e-mail/pasta .
                * **Fase 2: Chamada ao Analysis (Cloud):** Envia anexo para o 'Analysis' .
                * **Fase 3: Validação (Cloud):** Valida o JSON recebido .
                * **Fase 4: Execução (Desktop):** Inicia o bot Desktop na VM para fazer login no SAP , tratar Rateio , e integrar com Unico Doc .
                * **Fase 5: Log e Notificação (Cloud):** Registra o log no Snowflake e notifica a equipe .

                #### 3.2.2. Requisitos de Extração (Analysis)
                (Descreva o que o Engenheiro de IA precisa configurar no "Analysis").
                Exemplo:
                * **Prompt/Agente Necessário:** (Ex: "Prompt Fatura Fornecedor X").
                * **Campos-Chave para Extração:** (Ex: PO , Linha, Valor, WBS ).
                * **Regras de Classificação:** (Ex: Deve classificar o documento entre "CTE" e "FRS" ).
                * **Requisito de Confiança:** (Ex: A extração deve ter > 80% de confiança para seguir, senão vai para Exceção A ).

                #### 3.2.3. Tratamento de Exceções (Power Automate)
                * (Exceção A: Falha no Analysis / Baixa Confiança) 
                * (Exceção B: Erro no SAP, ex: WBS bloqueado) 
                * (Exceção C: Falha na Integração Legada) 
                ---

                Contexto AS-IS:
                ---
                {as_is_context}
                ---

                Arquitetura da Solução para Detalhar:
                ---
                {solution_choice}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                st.session_state.clipboard["design_pdd"] = response_text
                
                # --- CORREÇÃO DO BUG/AVISO (V3.0) ---
                # Força a atualização dos widgets nos outros módulos
                st.session_state.delivery_pdd_input = response_text
                st.session_state.qa_pdd_input = response_text
                # --- FIM DA CORREÇÃO ---

        else:
            st.warning("Por favor, preencha ambos os campos: Contexto AS-IS e Arquitetura da Solução.")

    if st.session_state.clipboard["design_pdd"]:
        st.divider()
        st.subheader("Esboço do Process Design Document (PDD)")
        st.markdown(st.session_state.clipboard["design_pdd"])
        
        st.divider()
        st.subheader("Salvar este PDD")
        
        project_name_input = st.text_input(
            "Dê um nome para este projeto de Design (PDD):", 
            placeholder="Ex: PDD - Automação Faturas Fornecedor X",
            key="pdd_project_name"
        )
        
        if st.button("Salvar", key="pdd_save_button"):
            if project_name_input:
                with st.spinner("Salvando..."):
                    
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Design (PDD)", 
                        content=st.session_state.clipboard["design_pdd"]
                    )
                    
                    if success:
                        st.success(f"Projeto '{project_name_input}' salvo com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")