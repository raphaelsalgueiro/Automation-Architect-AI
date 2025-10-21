import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("🧪 Gerador de Cenários de Teste")
    st.write("Cole o fluxo do processo 'To-Be' para que a I.A. gere um plano de testes completo.")

    qa_pdd_input = st.text_area(
        "Cole o fluxo do processo 'To-Be' aqui para gerar os testes:",
        height=300,
        placeholder="Ex: Passo 1: Robô monitora a pasta de rede. Passo 2: Robô abre o PDF e extrai os dados..."
    )

    if st.button("Gerar Cenários de Teste"):
        if qa_pdd_input:
            with st.spinner("Elaborando o plano de testes..."):
                prompt = f"""
                Você é um Engenheiro de QA (Quality Assurance) Sênior, especialista em automação.
                Sua tarefa é criar um plano de testes abrangente com base no fluxo de processo de um robô de RPA.
                Crie uma lista de cenários de teste, divididos nas seguintes categorias:
                1. **Testes de Caminho Feliz (Happy Path):**
                2. **Testes Negativos:**
                3. **Testes de Exceção:**
                Para cada cenário, descreva brevemente a condição do teste e o resultado esperado.
                Fluxo de Processo para Análise: --- {qa_pdd_input} ---
                """
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Plano de Testes Sugerido")
                st.markdown(response_text)
        else:
            st.warning("Por favor, cole o fluxo do processo 'To-Be' para gerar os testes.")