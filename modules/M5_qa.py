import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet

def run():
    st.header("🧪 5. QA & Testes")
    st.write("O objetivo deste módulo é gerar um Plano de Testes (UAT) completo com base no PDD, focado em **Power Automate** e **Analysis**.")

    # --- CORREÇÃO DO BUG/AVISO (V3.0) ---
    # O 'value' foi removido. O widget agora lê seu estado do 'key'.
    # O Módulo 3 (M3_design.py) é responsável por ATUALIZAR o 'st.session_state.qa_pdd_input'.
    pdd_input_widget_value = st.text_area(
        "3. Design (PDD)",
        height=300,
        placeholder="Gerado pelo Módulo 3 ou colado manualmente...",
        key="qa_pdd_input" # Lê o valor que o M3 definiu para este 'key'
    )

    if st.button("Gerar Cenários de Teste (UAT)"):
        if pdd_input_widget_value:
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["design_pdd"] = pdd_input_widget_value
            
            with st.spinner("Elaborando o plano de testes..."):
                
                # O prompt "v2.0" já estava bom e incluía testes para o Analysis 
                prompt = f"""
                Você é um Engenheiro de QA (Quality Assurance) Sênior, especialista em automação de processos com **Power Automate** e **Analysis**.
                Sua tarefa é criar um plano de testes (UAT) com base no PDD (Fluxo 'To-Be'), seguindo a estrutura da Seção 4 do documento de governança .

                Crie uma lista de cenários de teste, divididos nas seguintes categorias:

                ---
                ### 4.1. Testes de Caminho Feliz (Happy Path) 
                (Cenários onde tudo ocorre como esperado).
                Exemplos:
                * HP-01: "Criação de FRS Padrão (Sucesso E2E - Power Automate + Analysis + SAP + Unico Doc)" 
                * HP-03: "Processamento em Lote Misto (Power Automate processa FRS e RM no mesmo ciclo)" 
                * HP-04: "Tratamento de Rateio" 

                ### 4.2. Testes Negativos (Validação de Dados) 
                (Cenários que testam o comportamento com dados inválidos ou ausentes).
                Exemplos:
                * NEG-01: "Dados Incompletos (Analysis não encontra campo 'Valor Total')" 
                * NEG-02: "Validação de WBS Inválido" 
                * NEG-03: "Anexo Corrompido (PDF ilegível pelo Analysis)" 
                
                ### 4.3. Testes de Exceção (Resiliência do Sistema) 
                (Cenários que testam como o Power Automate lida com falhas).
                Exemplos:
                * EXC-01: "Baixa Confiança do Analysis (Abaixo de 80%)" 
                * EXC-02: "Erro de Lançamento no SAP (Ex: WBS Bloqueado)" 
                * EXC-03: "Falha de Integração com Unico Doc (Power Automate aplica Retry 3x e falha)" 
                * EXC-04: "Falha de Login Crítica (Power Automate Desktop não consegue logar na VM/SAP)" 
                ---
                
                Fluxo de Processo 'To-Be' para Análise:
                ---
                {pdd_input_widget_value}
                ---
                """
                
                response_text = call_gemini_api(prompt)
                st.session_state.clipboard["qa_plano"] = response_text
        else:
            st.warning("O PDD do Módulo 3 está vazio. Por favor, cole ou gere o PDD primeiro.")
    
    if st.session_state.clipboard.get("qa_plano"):
        st.divider()
        st.subheader("Plano de Testes Sugerido (UAT)")
        st.markdown(st.session_state.clipboard["qa_plano"])
        
        st.divider()
        st.subheader("Salvar este Plano de Testes")
        project_name_input = st.text_input(
            "Dê um nome para este Plano de Testes:", 
            placeholder="Ex: Plano de Testes - Faturas Fornecedor X",
            key="qa_project_name"
        )
        
        if st.button("Salvar", key="qa_save_button"):
            if project_name_input:
                with st.spinner("Salvando..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="QA (Plano de Testes)", 
                        content=st.session_state.clipboard["qa_plano"]
                    )
                    if success:
                        st.success(f"Plano de Testes '{project_name_input}' salvo com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")