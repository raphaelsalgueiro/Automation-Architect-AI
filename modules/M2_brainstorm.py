import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("🧠 2. Arquitetura (Solução)")
    st.write("O objetivo deste módulo é analisar o Diagnóstico AS-IS (do Módulo 1) e propor a **melhor arquitetura de solução unificada** (Power Automate + Analysis).")
    st.info("O resultado desta etapa é o input perfeito para o Módulo 3 (Design).")

    col1, col2 = st.columns(2)

    with col1:
        as_is_input = st.text_area(
            "Cole o Mapeamento AS-IS (Resultado do Módulo 1):",
            height=300,
            placeholder="Cole o diagnóstico AS-IS e as Regras de Negócio aqui..."
        )
    
    with col2:
        client_request = st.text_area(
            "Descreva o direcionamento do cliente (Opcional):",
            height=300,
            placeholder="Ex: O cliente mencionou especificamente que quer automatizar a extração de PDFs..."
        )

    if st.button("Gerar Arquitetura da Solução"):
        if as_is_input:
            with st.spinner("Analisando o problema e desenhando a arquitetura recomendada..."):
                
                # --- PROMPT ATUALIZADO ---
                # Pede UMA solução unificada, dividida em fases.
                
                prompt = f"""
                Você é um Arquiteto de Soluções Sênior, especialista em Power Automate e na I.A. "Analysis".
                Sua tarefa é analisar o mapeamento do processo atual (AS-IS) de um cliente e propor **A MELHOR e MAIS COESA "Arquitetura de Solução Recomendada"**.

                A solução deve ser um **plano unificado** para resolver os gargalos identificados, usando Power Automate e "Analysis".
                Se um direcionamento do cliente for fornecido, leve-o em consideração na sua solução.

                A sua resposta deve ser um único documento estruturado, contendo:
                1.  **Visão Geral da Solução:** (Um parágrafo resumindo a solução completa).
                2.  **Arquitetura Recomendada (dividida em Fases):** (Ex: "Fase 1: Intake e Aprovação (Quick Win)", "Fase 2: Lançamento no SAP (Estratégico)").
                3.  **Para cada Fase, detalhe:**
                    * **Objetivo da Fase:**
                    * **Ferramentas Envolvidas:** (Power Automate, Analysis, etc.)
                    * **Justificativa de Valor e Avaliação:** (Impacto/Esforço)

                IMPORTANTE: Não dê múltiplas "possibilidades" concorrentes. Dê UMA arquitetura recomendada, dividida em fases lógicas de implementação.

                Mapeamento AS-IS para Análise:
                ---
                {as_is_input}
                ---

                Direcionamento Opcional do Cliente:
                ---
                {client_request if client_request else "Nenhum direcionamento específico fornecido."}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Arquitetura de Solução Recomendada")
                st.markdown(response_text)
        else:
            st.warning("Por favor, insira pelo menos o Mapeamento AS-IS para análise.")