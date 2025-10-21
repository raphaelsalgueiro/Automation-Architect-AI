import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("💡 Identificador de Oportunidades de Automação")
    st.write("Descreva um processo de negócio para que a I.A. identifique os melhores pontos para automação e inovação.")
    
    process_input = st.text_area(
        "Cole a descrição do processo, transcrição de reunião ou suas anotações aqui:", 
        height=250, 
        placeholder="Ex: O processo de contas a pagar envolve receber a fatura por e-mail, abrir o PDF, digitar os dados na planilha X, conferir com o sistema Y e aprovar o pagamento."
    )

    if st.button("Identificar Oportunidades"):
        if process_input:
            with st.spinner("Analisando o processo..."):
                prompt = f"""
                Você é um Consultor de Automação e Inovação Sênior. Sua principal habilidade é analisar processos de negócio e identificar oportunidades claras para otimização.
                Analise a seguinte descrição de processo e identifique as melhores oportunidades para (1) Automação de Processos Robóticos (RPA) e (2) Inteligência Artificial (Machine Learning/IA).
                Para cada oportunidade encontrada, forneça:
                - **Oportunidade:** Descreva a tarefa ou etapa do processo.
                - **Tecnologia Sugerida:** (RPA ou I.A.).
                - **Justificativa:** Explique brevemente por que a tarefa é uma boa candidata para a tecnologia sugerida.
                Descrição do Processo para Análise: --- {process_input} ---
                """
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Oportunidades de Automação Encontradas")
                st.markdown(response_text)
        else:
            st.warning("Por favor, insira a descrição de um processo.")