import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("💡 1. Diagnóstico (AS-IS)")
    st.write("O objetivo deste módulo é analisar material bruto (anotações, e-mails, atas) para mapear o Processo Atual (AS-IS) e as Regras de Negócio do cliente, focando 100% no problema, sem sugerir tecnologia.")
    st.info("O resultado desta etapa é o input perfeito para o Módulo 6 (Governança).")
    
    process_input = st.text_area(
        "Cole o material bruto do processo aqui:", 
        height=300, 
        placeholder="Ex: Anotações da reunião com o cliente sobre o processo de faturamento..."
    )

    if st.button("Mapear Processo AS-IS"):
        if process_input:
            with st.spinner("Analisando o material e mapeando o processo AS-IS..."):
                
                prompt = f"""
                Você é um Analista de Negócios Sênior especialista em mapeamento de processos (AS-IS).
                Sua tarefa é analisar o material bruto fornecido (anotações de reunião, transcrições, etc.) e extrair DUAS seções principais:
                
                1.  **Mapeamento de Regras de Negócio (AS-IS):** Liste todas as regras, políticas e condições operacionais mencionadas.
                2.  **Mapeamento de Processo Atual (AS-IS):** Descreva o processo passo a passo atual, identificando gargalos ou pontos de intervenção manual.

                IMPORTANTE: Nesta etapa, NÃO sugira nenhuma tecnologia ou solução (NÃO mencione Power Automate, Analysis, RPA ou I.A.). O foco é 100% no diagnóstico do PROBLEMA.

                Material para Análise:
                ---
                {process_input}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Resultado do Diagnóstico (AS-IS)")
                st.markdown(response_text)
        else:
            st.warning("Por favor, insira o material bruto para análise.")