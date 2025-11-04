import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("🧪 5. QA & Testes")
    st.write("O objetivo deste módulo é gerar um Plano de Testes (UAT) completo com base no PDD (do Módulo 3), pensando em todos os cenários possíveis para garantir a qualidade da entrega.")
    st.info("O resultado desta etapa é o input perfeito para o Módulo 6 (Governança).")

    qa_pdd_input = st.text_area(
        "Cole o PDD / Fluxo 'To-Be' (Resultado do Módulo 3) aqui:",
        height=300,
        placeholder="Ex: Passo 1: Robô monitora a pasta de rede. Passo 2: Robô chama 'Analysis' para ler o PDF..."
    )

    if st.button("Gerar Cenários de Teste (UAT)"):
        if qa_pdd_input:
            with st.spinner("Elaborando o plano de testes..."):
                
                prompt = f"""
                Você é um Engenheiro de QA (Quality Assurance) Sênior, especialista em automação de processos.
                Sua tarefa é criar um plano de testes abrangente (Plano de UAT) com base no fluxo de processo 'To-Be' de um robô de RPA.

                Crie uma lista de cenários de teste, divididos nas seguintes categorias:
                1.  **Testes de Caminho Feliz (Happy Path):** Cenários onde tudo ocorre como esperado.
                2.  **Testes Negativos (Validação de Dados):** Cenários que testam o comportamento do robô com dados inválidos, ausentes ou mal formatados.
                3.  **Testes de Exceção (Resiliência do Sistema):** Cenários que testam como o robô lida com erros de sistema, timeouts ou falhas inesperadas.

                Para cada cenário, descreva brevemente a condição do teste e o resultado esperado.

                Fluxo de Processo 'To-Be' para Análise:
                ---
                {qa_pdd_input}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                
                st.divider()
                st.subheader("Plano de Testes Sugerido (UAT)")
                st.markdown(response_text)
        else:
            st.warning("Por favor, cole o PDD / Fluxo 'To-Be' para gerar os testes.")