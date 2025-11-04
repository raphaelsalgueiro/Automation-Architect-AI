import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("📄 4. Delivery (Docs)")
    st.write("O objetivo deste módulo é traduzir o PDD (do Módulo 3) em artefatos técnicos detalhados para a equipe de desenvolvimento (Épico, Requisitos Funcionais, NFRs, User Stories e Critérios de Aceitação).")
    st.info("O resultado desta etapa é o input perfeito para o Módulo 6 (Governança).")
    
    pdd_input = st.text_area(
        "Cole o PDD / Fluxo 'To-Be' (Resultado do Módulo 3) aqui:",
        height=300,
        placeholder="Ex: Passo 1: Robô monitora a pasta de rede. Passo 2: Robô chama 'Analysis' para ler o PDF. Passo 3: Robô abre o SAP..."
    )

    if st.button("Gerar Artefatos para Desenvolvimento"):
        if pdd_input:
            with st.spinner("Gerando a documentação técnica detalhada..."):
                
                prompt = f"""
                Você é um Analista de Requisitos Ágil e Engenheiro de Software especialista em Engenharia de Requisitos.
                Sua tarefa é traduzir o PDD (Process Design Document) de uma automação em um conjunto completo de artefatos de desenvolvimento.

                Com base no PDD fornecido, gere os seguintes documentos de forma clara e detalhada, usando Markdown para formatação:
                1.  **Épico Principal:** (Um título e uma breve descrição para o projeto geral).
                2.  **Requisitos Funcionais (RFs):** (Uma lista detalhada do que o sistema DEVE fazer).
                3.  **Requisitos Não Funcionais (NFRs):** (Sugira NFRs importantes para esta automação: Segurança, Performance, Auditoria, Confiabilidade, etc.).
                4.  **Histórias de Usuário (User Stories):** (Quebre os RFs em User Stories lógicas no formato 'Como um [ator], eu quero [ação], para que [benefício]').
                5.  **Critérios de Aceitação (CAs):** (Para as User Stories mais importantes, detalhe os CAs no formato 'Dado que... Quando... Então...').

                PDD para Análise:
                ---
                {pdd_input}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Artefatos para a Equipe de Desenvolvimento")
                st.markdown(response_text)
        else:
            st.warning("Por favor, cole o PDD / Fluxo 'To-Be' para análise.")