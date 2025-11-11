import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet
from utils.file_parser import parse_file  # <-- IMPORTAMOS NOSSO NOVO PARSER

def run():
    st.header("💡 1. Diagnóstico (AS-IS)")
    st.write("O objetivo deste módulo é analisar material bruto (anotações, e-mails, atas) para mapear o Processo Atual (AS-IS) e as Regras de Negócio do cliente, focando 100% no problema, sem sugerir tecnologia.")
    
    process_input = st.text_area(
        "Cole o material bruto do processo aqui (anotações de reunião, etc):", 
        height=250, 
        placeholder="Ex: Anotações da reunião com o cliente sobre o processo de faturamento..."
    )

    uploaded_files = st.file_uploader(
        "Ou anexe arquivos (PDF, DOCX, TXT) que o cliente enviou:",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("Mapear Processo AS-IS"):
        
        # --- LÓGICA REFINADA (COMBINA OS DOIS INPUTS) ---
        if not process_input and not uploaded_files:
            st.warning("Por favor, cole um texto ou anexe pelo menos um arquivo para análise.")
            st.stop()

        all_text_parts = []
        
        # 1. Adiciona o texto colado
        if process_input:
            all_text_parts.append(process_input)
            
        # 2. Adiciona o texto dos arquivos anexados
        if uploaded_files:
            with st.spinner(f"Lendo {len(uploaded_files)} arquivo(s)..."):
                for file in uploaded_files:
                    extracted_text = parse_file(file)
                    if extracted_text:
                        all_text_parts.append(extracted_text)
        
        # 3. Combina tudo em um super-texto
        combined_text = "\n\n".join(all_text_parts)
        
        # st.expander("Ver Texto Combinado Enviado para a IA"):
        #     st.text(combined_text) # (Descomente esta linha se quiser debugar)

        with st.spinner("Analisando o material e mapeando o processo AS-IS..."):
            
            prompt = f"""
            Você é um Analista de Negócios Sênior especialista em mapeamento de processos (AS-IS).
            Sua tarefa é analisar o material bruto fornecido (que pode incluir anotações e texto de documentos anexados) e extrair DUAS seções principais, seguindo o padrão do documento de governança :

            1.  **2.1 Mapeamento de Regras de Negócio (AS-IS):** Liste todas as regras, políticas e condições operacionais mencionadas (ex: Regra 2.1.1...).
            2.  **2.2 Mapeamento de Processo Atual (AS-IS):** Descreva o processo passo a passo atual, identificando gargalos ou pontos de intervenção manual.

            IMPORTANTE: Nesta etapa, NÃO sugira nenhuma tecnologia ou solução (NÃO mencione Power Automate, Analysis, RPA ou I.A.). O foco é 100% no diagnóstico do PROBLEMA.

            Material para Análise:
            ---
            {combined_text}
            ---
            """
            
            response_text = call_gemini_api(prompt)
            st.session_state.clipboard["diagnostico_asis"] = response_text

    if st.session_state.clipboard["diagnostico_asis"]:
        st.divider()
        st.subheader("Resultado do Diagnóstico (AS-IS)")
        st.markdown(st.session_state.clipboard["diagnostico_asis"])

        st.divider()
        st.subheader("Salvar este Diagnóstico")
        project_name_input = st.text_input(
            "Dê um nome para este Diagnóstico:", 
            placeholder="Ex: Diagnóstico - Faturas Fornecedor X",
            key="diag_project_name"
        )
        
        if st.button("Salvar", key="diag_save_button"):
            if project_name_input:
                with st.spinner("Salvando na planilha..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Diagnóstico (AS-IS)", 
                        content=st.session_state.clipboard["diagnostico_asis"]
                    )
                    if success:
                        st.success(f"Diagnóstico '{project_name_input}' salvo com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")