import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import load_from_sheet, save_to_sheet
from utils.pdf_exporter import create_pdf_bytes 

@st.cache_data(ttl=60) 
def get_history_records_cached():
    """Esta função é cacheada e só vai chamar a planilha a cada 60 segundos."""
    return load_from_sheet()

def run():
    st.header("📚 7. Histórico & Refinar")
    st.write("O objetivo deste módulo é carregar um Documento de Governança salvo e adaptá-lo para um novo cenário (ex: novo fornecedor), gerando um novo documento completo.")
    st.info("Este é um fluxo 'fast-track' que não depende dos Módulos 1-6.")

    if 'refine_output_generated' not in st.session_state:
        st.session_state.refine_output_generated = False
    
    if 'refine_analysis_display' not in st.session_state:
        st.session_state.refine_analysis_display = ""
    
    if 'refine_save_success' not in st.session_state:
        st.session_state.refine_save_success = False

    if st.session_state.refine_output_generated:
        st.subheader("Documento de Governança Adaptado (Rascunho)")
        
        if st.session_state.refine_analysis_display:
            with st.expander("Ver Análise de Impacto da Adaptação"):
                st.markdown(st.session_state.refine_analysis_display)

        refined_doc_markdown = st.session_state.clipboard["refine_output"]
        
        st.markdown(refined_doc_markdown)
        st.code(refined_doc_markdown, language="markdown")
        
        st.divider()
        st.subheader("Salvar ou Exportar este Documento")
        
        if st.session_state.get("clear_refine_name", False):
            st.session_state.refine_save_name = ""  
            st.session_state.clear_refine_name = False 

        refine_name_input = st.text_input(
            "1. Dê um nome para este novo Documento de Governança:", 
            placeholder="Ex: Doc Governança - (Adaptado)",
            key="refine_save_name"
        )

        # --- INÍCIO DA ATUALIZAÇÃO (LAYOUT V9.0) ---
        col1_act, col2_act = st.columns([1, 1]) # 50% / 50%
        
        with col1_act: # Bloco de Ação na Esquerda
            if st.button("2. Salvar", key="refine_save_button"):
                if st.session_state.refine_save_name: 
                    with st.spinner("Salvando..."):
                        
                        content_to_save = refined_doc_markdown

                        success = save_to_sheet(
                            project_name=st.session_state.refine_save_name, 
                            doc_type="Governança (Adaptado)", 
                            content=content_to_save 
                        )
                        if success:
                            st.success(f"Documento '{st.session_state.refine_save_name}' salvo com sucesso!")
                            st.session_state.refine_save_success = True 
                        else:
                            st.error("Falha ao salvar o projeto.")
                            st.session_state.refine_save_success = False
                else:
                    st.warning("Por favor, dê um nome ao documento para salvá-lo.")
                    st.session_state.refine_save_success = False

            # Agrupa o botão Exportar logo abaixo do Salvar
            if st.session_state.refine_save_success and st.session_state.refine_save_name:
                pdf_file_name = f"{st.session_state.refine_save_name.replace(' ', '_')}.pdf"
                pdf_bytes = create_pdf_bytes(refined_doc_markdown)
                
                if pdf_bytes:
                    st.download_button(
                        label="3. Exportar para PDF",
                        data=pdf_bytes,
                        file_name=pdf_file_name,
                        mime="application/pdf"
                    )
        
        # col2_act (Coluna da Direita) fica intencionalmente vazia
        # --- FIM DA ATUALIZAÇÃO ---
        
        st.divider()
        
        col_nav1, col_nav_btn, col_nav3 = st.columns([2, 1, 2]) 

        with col_nav_btn:
            if st.button("Refinar Outro Projeto", type="primary"):
                st.session_state.refine_output_generated = False
                st.session_state.clipboard["refine_output"] = ""
                st.session_state.refine_analysis_display = "" 
                st.session_state.clear_refine_name = True 
                st.session_state.refine_save_success = False 
                st.rerun()
            
        st.stop() 


    st.subheader("Carregar Projeto do Histórico")

    records = get_history_records_cached()

    if not records:
        st.info("Nenhum projeto encontrado no seu histórico. Salve um projeto em outro módulo para vê-lo aqui.")
        st.info("Se você acabou de salvar, aguarde 60 segundos para o cache atualizar ou clique em 'Limpar cache'.")
    else:
        
        project_names = [
            f"{r['Nome_Do_Projeto']} ({r['Tipo_De_Documento']}) - {r['Data']}" 
            for r in reversed(records) 
        ]
        
        selected_project_name = st.selectbox(
            "Selecione um projeto para refinar:", 
            options=project_names,
            index=None, 
            placeholder="Selecione um projeto da lista...", 
            key="refine_select_project"
        )

        if selected_project_name: 
            
            selected_record = next(
                r for r in reversed(records) if f"{r['Nome_Do_Projeto']} ({r['Tipo_De_Documento']}) - {r['Data']}" == selected_project_name
            )
            
            original_content = selected_record['Conteudo_Gerado']
            
            if "---DOCUMENTO-LIMPO---" in original_content:
                original_content = original_content.split("---DOCUMENTO-LIMPO---", 1)[1].strip()
            elif "---ARQUITETURA-LIMPA---" in original_content:
                 original_content = original_content.split("---ARQUITETURA-LIMPA---", 1)[1].strip()


            st.divider()
            st.subheader("Refinar Automação Carregada")
            st.write("O documento original está carregado abaixo. Descreva as mudanças para a I.A. gerar uma nova versão.")

            col1, col2 = st.columns(2)

            with col1:
                st.text_area(
                    "Documento Original Carregado:",
                    value=original_content,
                    height=400,
                    key="refine_original_text"
                )
            
            with col2:
                new_requirements = st.text_area(
                    "Descreva as Mudanças / Novas Regras de Negócio:",
                    height=400,
                    placeholder="Ex: Adaptar para Fornecedor B. Diferenças: Sistema SAP (não Oracle), layout do PDF diferente, adicionar validação com Compras.",
                    key="refine_new_reqs_text"
                )

            if st.button("Gerar Documento de Governança Adaptado", key="refine_generate_button", type="primary"):
                if new_requirements:
                    with st.spinner("Analisando o original e gerando o novo Documento de Governança..."):
                        
                        # --- INÍCIO DA ATUALIZAÇÃO (PROMPT V9.0) ---
                        prompt = f"""
                        Você é o especialista em Governança de Projetos da DMS Logistics, focado em **Power Automate** e **Analysis**.
                        Sua tarefa é gerar um NOVO "Documento de Governança Discovery-to-Delivery" completo, adaptado para um novo cenário.

                        Você receberá:
                        1.  **[Documento Original]:** Um documento de Governança completo de um projeto existente.
                        2.  **[Novas Regras de Negócio]:** Uma lista de mudanças necessárias.

                        REGRAS CRÍTICAS PARA O OUTPUT:
                        
                        1.  **NÃO INVENTE INFORMAÇÕES (REGRA MAIS IMPORTANTE):**
                            Apegue-se estritamente aos fatos fornecidos no [Documento Original] e nas [Novas Regras de Negócio]. NÃO infira, calcule ou adicione NENHUMA informação que não esteja explicitamente declarada.
                            * **Exemplo 1 (Nomes):** Se a nova regra diz "Nome: CHATDOWNBLIS", use "CHATDOWNBLIS" e NADA MAIS (não "CHATDOWNBLIS FREIGHT").
                            * **Exemplo 2 (Quantidades):** Se a nova regra diz "recebe todos os dias", apenas substitua a frequência original por "todos os dias". NÃO calcule um total mensal (como "102 documentos").

                        2.  **PRIORIDADE TOTAL ÀS NOVAS REGRAS:** Se houver qualquer conflito entre o [Documento Original] e as [Novas Regas de Negócio], as [Novas Regras de Negócio] **SEMPRE VENCEM**.

                        3.  **Formato Duplo:** Gere DUAS SEÇÕES, separadas pelo token '---DOCUMENTO-LIMPO---'.
                        
                        **SEÇÃO 1: ANÁLISE DE IMPACTO (PARA O GESTOR)**
                        (Aqui, você DEVE destacar explicitamente todas as mudanças. Use marcadores em Markdown (ex: `**[MUDANÇA]**` ou `**[NOVO]**`) antes de cada parágrafo ou item que foi alterado. Mantenha o restante do texto que não mudou SEM marcadores.)

                        ---DOCUMENTO-LIMPO---
                        
                        (NÃO COLOQUE NENHUM TÍTULO AQUI. Comece DIRETAMENTE com o documento de governança.)
                        (Gere o documento completo (Seção 1 a 5) com as mudanças já aplicadas, mas de forma LIMPA, **SEM NENHUMA TAG** `[MUDANÇA]` ou `[NOVO]`.)

                        4.  **Foco na Stack:** As mudanças devem refletir adaptações nos fluxos do **Power Automate** ou nos prompts do **Analysis**.

                        ---
                        [Documento Original]
                        {original_content}
                        ---

                        ---
                        [Novas Regras de Negócio / Mudanças]
                        {new_requirements}
                        ---
                        """
                        # --- FIM DA ATUALIZAÇÃO ---
                        
                        response_text = call_gemini_api(prompt)
                        
                        if "---DOCUMENTO-LIMPO---" in response_text:
                            parts = response_text.split("---DOCUMENTO-LIMPO---", 1)
                            analysis_display = parts[0].strip()
                            clean_doc_output = parts[1].strip()

                            st.session_state.refine_analysis_display = analysis_display
                            st.session_state.clipboard["refine_output"] = clean_doc_output
                        else:
                            st.warning("A IA não gerou o separador de documento limpo. O documento pode conter tags de [MUDANÇA].")
                            st.session_state.refine_analysis_display = ""
                            st.session_state.clipboard["refine_output"] = response_text
                        
                        st.session_state.refine_output_generated = True
                        st.session_state.clear_refine_name = True 
                        st.session_state.refine_save_success = False 
                        st.rerun() 
                        
                else:
                    st.warning("Por favor, descreva as mudanças necessárias.")