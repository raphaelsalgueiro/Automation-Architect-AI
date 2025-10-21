import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("📄 Fábrica de Documentos para Desenvolvimento")
    st.write("Cole o fluxo do processo 'To-Be' gerado no módulo de Design para criar os artefatos para a equipe de desenvolvimento.")
    
    pdd_input = st.text_area(
        "Cole o fluxo do processo 'To-Be' aqui:",
        height=300,
        placeholder="Ex: Passo 1: Robô monitora a pasta de rede. Passo 2: Robô abre o PDF e extrai os dados. Passo 3: Robô faz login no CRM..."
    )

    if st.button("Gerar Artefatos para Devs"):
        if pdd_input:
            with st.spinner("Escrevendo as User Stories e Requisitos..."):
                prompt = f"""
                Você é um Analista de Requisitos Sênior. Sua tarefa é traduzir um documento de design de processo (PDD) em artefatos claros para uma equipe de desenvolvimento Ágil.
                Com base no fluxo de processo 'To-Be' abaixo, gere os seguintes documentos, usando Markdown para formatação:
                1. **Épico Principal:**
                2. **Histórias de Usuário (User Stories):**
                3. **Requisitos Não Funcionais (NFRs):**
                4. **Critérios de Aceitação:**
                Fluxo de Processo para Análise: --- {pdd_input} ---
                """
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Artefatos para a Equipe de Desenvolvimento")
                st.markdown(response_text)
        else:
            st.warning("Por favor, cole o fluxo do processo 'To-Be'.")