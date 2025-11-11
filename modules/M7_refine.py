import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import load_from_sheet, save_to_sheet

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
    
    if st.session_state.refine_output_generated:
        st.subheader("Documento de Governança Adaptado (Rascunho)")
        st.markdown(st.session_state.clipboard["refine_output"])
        
        st.divider()
        st.subheader("Salvar este Documento Adaptado")
        refine_name_input = st.text_input(
            "Dê um nome para este novo Documento de Governança:", 
            placeholder="Ex: Doc Governança - (Adaptado)",
            key="refine_save_name"
        )
        
        col1_btn, col2_btn = st.columns(2)
        with col1_btn:
            if st.button("Salvar", key="refine_save_button"):
                if refine_name_input:
                    with st.spinner("Salvando..."):
                        success = save_to_sheet(
                            project_name=refine_name_input, 
                            doc_type="Governança (Adaptado)", 
                            content=st.session_state.clipboard["refine_output"]
                        )
                        if success:
                            st.success(f"Documento '{refine_name_input}' salvo com sucesso!")
                        else:
                            st.error("Falha ao salvar o projeto.")
                else:
                    st.warning("Por favor, dê um nome ao documento para salvá-lo.")
        
        with col2_btn:
            if st.button("Refinar Outro Projeto", type="primary"):
                st.session_state.refine_output_generated = False
                st.session_state.clipboard["refine_output"] = ""
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
                        
                        prompt = f"""
                        Você é o especialista em Governança de Projetos da DMS Logistics , focado em **Power Automate** e **Analysis**.
                        Sua tarefa é gerar um NOVO "Documento de Governança Discovery-to-Delivery" completo, adaptado para um novo cenário (ex: um novo fornecedor ou processo).

                        Você receberá:
                        1.  **[Documento Original]:** Um documento de governança completo de um projeto existente .
                        2.  **[Novas Regras de Negócio]:** Uma lista de mudanças necessárias.

                        Sua tarefa é REESCREVER o [Documento Original] aplicando as [Novas Regras de Negócio].

                        REGRAS CRÍTICAS PARA O OUTPUT:
                        1.  **Formato Completo:** O resultado final DEVE ser um documento de governança completo (Seção 1 a 5) .
                        2.  **Destacar Mudanças:** Esta é a regra mais importante. Ao reescrever o documento, você DEVE **destacar explicitamente** todas as mudanças. Use marcadores em Markdown (ex: `**[MUDANÇA]**` ou `**[NOVO]**`) antes de cada parágrafo, item de lista ou seção que foi alterado ou adicionado com base nas novas regras.
                        3.  **Manter o Restante:** Se uma seção do [Documento Original] não for impactada (ex: "1.1 Propósito deste Documento" ), reutilize-a como está (e sem marcadores de mudança).
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
                        
                        response_text = call_gemini_api(prompt)
                        st.session_state.clipboard["refine_output"] = response_text
                        st.session_state.refine_output_generated = True
                        st.rerun() 
                else:
                    st.warning("Por favor, descreva as mudanças necessárias.")