import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("✍️ Arquiteto de Soluções de Automação")
    st.write("Descreva a automação que você quer construir para que a I.A. detalhe o fluxo do processo passo a passo (PDD).")
    
    automation_goal = st.text_area(
        "Descreva o objetivo e o comportamento esperado da automação:",
        height=250,
        placeholder="Ex: Automatizar o processo de criação de cliente no CRM. O robô deve monitorar uma pasta, ler os dados do contrato (PDF), abrir o sistema CRM, inserir os dados nos campos corretos e, ao final, enviar um e-mail de notificação."
    )

    if st.button("Desenhar Fluxo da Automação"):
        if automation_goal:
            with st.spinner("Desenhando o fluxo do processo..."):
                prompt = f"""
                Você é um Arquiteto de Soluções de RPA. Sua tarefa é criar um esboço de um Process Design Document (PDD).
                Com base no objetivo da automação descrito abaixo, detalhe o fluxo do processo 'To-Be' (como será com o robô) em um formato de passo a passo claro e numerado, incluindo tratamento de exceções.
                Objetivo da Automação: --- {automation_goal} ---
                """
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Esboço do Process Design Document (PDD)")
                st.markdown(response_text)
        else:
            st.warning("Por favor, descreva o objetivo da automação.")