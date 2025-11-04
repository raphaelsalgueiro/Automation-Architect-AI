import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("✍️ 3. Design (TO-BE)")
    st.write("O objetivo deste módulo é detalhar a 'Solução Proposta' (do Módulo 2) em um PDD (Fluxo TO-BE), usando o 'Diagnóstico AS-IS' (do Módulo 1) como contexto.")
    st.info("O resultado desta etapa é o input perfeito para os Módulos 4 (Delivery) e 5 (QA).")
    
    col1, col2 = st.columns(2)

    with col1:
        as_is_context = st.text_area(
            "Cole o Mapeamento AS-IS (Resultado do Módulo 1) aqui:",
            height=300,
            placeholder="Cole o diagnóstico AS-IS para dar contexto à I.A...."
        )
    
    with col2:
        solution_choice = st.text_area(
            "Cole a 'Solução Proposta' (Resultado do Módulo 2) aqui:",
            height=300,
            placeholder="Cole a solução específica que você escolheu no Módulo 2 para detalhar..."
        )

    if st.button("Desenhar Fluxo da Automação (PDD)"):
        if as_is_context and solution_choice:
            with st.spinner("Desenhando o fluxo do processo TO-BE..."):
                
                # --- PROMPT ATUALIZADO ---
                # Agora usa os dois inputs para gerar o PDD
                
                prompt = f"""
                Você é um Arquiteto de Soluções de Automação Sênior. Sua tarefa é criar um esboço detalhado de um Process Design Document (PDD) com foco no fluxo "To-Be".

                Para fazer isso, você receberá dois blocos de informação:
                1.  **Contexto AS-IS:** O mapeamento do processo atual.
                2.  **Solução Proposta:** A descrição da solução que você deve detalhar.

                Use o Contexto AS-IS para entender o cenário, e foque em detalhar a Solução Proposta. O PDD gerado deve conter:
                -   **Visão Geral da Solução:** (Nome do Processo, Objetivo, Ferramentas: Power Automate e "Analysis").
                -   **Fluxo de Processo 'To-Be' (Passo a Passo):** Detalhe as fases.
                -   **Tratamento de Exceções e Erros:** Detalhe os caminhos de erro.

                Contexto AS-IS:
                ---
                {as_is_context}
                ---

                Solução Proposta para Detalhar:
                ---
                {solution_choice}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Esboço do Process Design Document (PDD)")
                st.markdown(response_text)
        else:
            st.warning("Por favor, preencha ambos os campos: Contexto AS-IS e Solução Proposta.")