import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet, load_from_sheet 

# --- PROMPT 1: GERAR ARQUITETURA DO ZERO ---
# (Este prompt está 100% correto, sem mudanças)
def get_original_architecture_prompt(as_is_input, client_request):
    """Gera o prompt original do Módulo 2 (criar do zero)."""
    return f"""
    Você é um Arquiteto de Soluções Sênior, especialista em **Power Automate (Cloud e Desktop)** e na ferramenta de IA interna **"Analysis"** .
    Sua tarefa é analisar o mapeamento do processo atual (AS-IS) e propor A MELHOR "Arquitetura de Solução Recomendada" usando **EXCLUSIVAMENTE** essa stack.

    A sua resposta deve ser um único documento estruturado, contendo:
    1.  **Visão Geral da Solução:** (Um parágrafo resumindo a solução completa) .
    2.  **Arquitetura Recomendada (Fases):** (Ex: "Fase 1: Extração com Analysis", "Fase 2: Lançamento com Power Automate Desktop").
    3.  **Divisão de Responsabilidades (IMPORTANTE):**
        * **Responsabilidades do "Analysis" (Engenheiro de IA):** (O que o Analysis fará? Ex: Extrair campos X, Y, Z , classificar documentos , requerer prompts customizados para Fornecedor B).
        * **Responsabilidades do "Power Automate" (Desenvolvedor RPA):** (O que o Power Automate fará? Ex: Monitorar a fonte , orquestrar as chamadas ao Analysis, fazer login no SAP , tratar exceções, integrar com o Unico Doc ).
    4.  **Justificativa de Valor e Avaliação:** (Impacto/Esforço).

    Mapeamento AS-IS para Análise:
    ---
    {as_is_input}
    ---

    Direcionamento Opcional do Cliente:
    ---
    {client_request if client_request else "Nenhum direcionamento específico fornecido."}
    ---
    """

# --- PROMPT 2: BUSCAR E REUTILIZAR (PROMPT LIMPO V7.1) ---
def get_finder_prompt(as_is_input, client_request, historical_docs_string):
    """
    Gera o novo prompt "inteligente" (v7.1) que busca no histórico,
    gera uma ANÁLISE DE IMPACTO (para exibição) e uma ARQUITETURA LIMPA (para o clipboard),
    separadas por um token.
    """
    # --- INÍCIO DA ATUALIZAÇÃO (LIMPEZA DE CITAÇÕES) ---
    return f"""
    Você é um Arquiteto de Soluções Sênior especialista em Power Automate e Analysis.

    Sua primeira tarefa é analisar o [Novo Diagnóstico AS-IS] e compará-lo com o [Histórico de Projetos Anteriores].
    
    1.  **Analise o [Novo Diagnóstico AS-IS]:** Entenda o problema central.
    2.  **Compare com o [Histórico]:** Procure por um projeto no histórico que seja altamente similar (mais de 80% de sobreposição) e que possa ser REAPROVEITADO.
    3.  **Tome uma Decisão:**

        * **SE VOCÊ ENCONTRAR UM PROJETO SIMILAR:**
            Sua resposta deve começar **EXATAMENTE** com a tag `[REUTILIZAR]`.
            Após a tag, gere DUAS SEÇÕES, separadas por '---ARQUITETURA-LIMPA---'.

            **SEÇÃO 1: ANÁLISE DE IMPACTO (PARA O GESTOR)**
            (Esta seção é um rascunho de análise para o Gestor de Projetos. NÃO é o documento final.)
            
            **Projeto Base Identificado:** (Ex: "Baseado no projeto 'Automação OUROMAR'...")
            
            **Análise de Impacto da Adaptação:**
            (Descreva o que muda na stack para atender ao novo diagnóstico. Use tags [MUDANÇA] ou [NOVO].)
            * `[MUDANÇA] Analysis:` (Ex: O modelo precisará ser retreinado para o novo layout do Fornecedor B.)
            * `[NOVO] Power Automate:` (Ex: A Fase 4 deve ser nova para logar no Oracle em vez do SAP.)
            * `[MUDANÇA] Regras de Negócio:` (Ex: A Regra 2.1.2 muda de 90 para 30 dias.)

            ---ARQUITETURA-LIMPA---

            **SEÇÃO 2: ARQUITETURA DE SOLUÇÃO (PARA O MÓDULO 3)**
            (Gere a **nova** "Arquitetura de Solução Recomendada" para o **novo projeto**, já com as adaptações incorporadas, mas de forma LIMPA, sem tags [MUDANÇA] ou "projeto correlato". 
            Siga a mesma estrutura do Prompt 1: Visão Geral, Fases e Divisão de Responsabilidades.)
            
            **Visão Geral da Solução:** (Ex: "A solução para o Fornecedor B irá...")
            **Arquitetura Recomendada (Fases):** (Ex: "Fase 1: Extração Analysis", "Fase 2: Login Oracle...")
            **Divisão de Responsabilidades:**
            * **Responsabilidades do "Analysis":** (Ex: "Extrair campos A, B, C do Fornecedor B.")
            * **Responsabilidades do "Power Automate":** (Ex: "Orquestrar, logar no Oracle...")
            **Justificativa de Valor:** (Impacto/Esforço para o novo projeto.)


        * **SE NENHUM PROJETO FOR SIMILAR O SUFICIENTE:**
            Sua resposta deve ser **APENAS** a tag `[NOVO]`.

    ---
    [Novo Diagnóstico AS-IS]
    {as_is_input}
    
    [Direcionamento Opcional do Cliente para o Novo Diagnóstico]
    {client_request if client_request else "Nenhum."}
    ---

    ---
    [Histórico de Projetos Anteriores (Documentos de Governança)]
    
    {historical_docs_string}
    ---
    """
    # --- FIM DA ATUALIZAÇÃO ---

# --- FUNÇÃO PRINCIPAL DO MÓDULO (LÓGICA DE SPLIT ATUALIZADA) ---

def run():
    st.header("🧠 2. Arquitetura (Solução)")
    st.write("O objetivo deste módulo é propor a melhor arquitetura de solução, usando **Power Automate** e **Analysis** (IA Interna). A ferramenta irá primeiro verificar seu histórico por projetos reaproveitáveis.")

    if 'm2_show_override_button' not in st.session_state:
        st.session_state.m2_show_override_button = False
    
    if 'm2_display_analysis' not in st.session_state:
        st.session_state.m2_display_analysis = ""

    as_is_input = st.text_area(
        "1. Diagnóstico (AS-IS)",
        value=st.session_state.clipboard.get("diagnostico_asis", ""),
        height=300,
        placeholder="Cole o Diagnóstico AS-IS aqui ou gere-o no Módulo 1..."
    )
    
    client_request = st.text_area(
        "2. Direcionamento do cliente (Opcional):",
        height=150,
        placeholder="Ex: O cliente mencionou que o sistema é SAP e que os PDFs são de baixa qualidade..."
    )

    if st.button("Gerar Arquitetura da Solução"):
        if as_is_input:
            st.session_state.m2_show_override_button = False
            st.session_state.clipboard["arquitetura_solucao"] = ""
            st.session_state.m2_display_analysis = "" 
            
            st.session_state.clipboard["diagnostico_asis"] = as_is_input

            with st.spinner("Analisando o histórico por projetos similares..."):
                all_records = load_from_sheet()
                gov_records = [
                    r['Conteudo_Gerado'] for r in all_records 
                    if r.get('Tipo_De_Documento') == 'Governança (Final)'
                ]
                
                final_response = ""

                if gov_records:
                    historical_docs_string = "\n\n".join(
                        [f"--- PROJETO ANTIGO {i+1} ---\n{doc}" for i, doc in enumerate(gov_records)]
                    )
                    finder_prompt = get_finder_prompt(as_is_input, client_request, historical_docs_string)
                    finder_response = call_gemini_api(finder_prompt)

                    if finder_response.strip() == "[NOVO]":
                        st.session_state.m2_show_override_button = False
                        st.session_state.m2_display_analysis = ""
                        with st.spinner("Nenhum projeto similar encontrado. Gerando nova arquitetura..."):
                            original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                            final_response = call_gemini_api(original_prompt)
                            st.session_state.clipboard["arquitetura_solucao"] = final_response
                    
                    elif finder_response.startswith("[REUTILIZAR]"):
                        st.session_state.m2_show_override_button = True 
                        
                        full_response_text = finder_response.replace("[REUTILIZAR]", "").strip()

                        if "---ARQUITETURA-LIMPA---" in full_response_text:
                            parts = full_response_text.split("---ARQUITETURA-LIMPA---", 1)
                            display_analysis = parts[0].strip()
                            clipboard_architecture = parts[1].strip()
                            
                            st.session_state.m2_display_analysis = display_analysis
                            st.session_state.clipboard["arquitetura_solucao"] = clipboard_architecture
                        else:
                            st.warning("A IA não gerou o separador de arquitetura. O Módulo 3 pode receber contexto extra.")
                            st.session_state.m2_display_analysis = ""
                            st.session_state.clipboard["arquitetura_solucao"] = full_response_text
                    
                    else:
                        st.warning("A IA não retornou uma tag válida. Gerando arquitetura do zero.")
                        st.session_state.m2_show_override_button = False
                        st.session_state.m2_display_analysis = ""
                        original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                        final_response = call_gemini_api(original_prompt)
                        st.session_state.clipboard["arquitetura_solucao"] = final_response

                else:
                    st.info("Nenhum projeto de governança encontrado no histórico. Gerando nova arquitetura...")
                    st.session_state.m2_show_override_button = False
                    st.session_state.m2_display_analysis = ""
                    original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                    final_response = call_gemini_api(original_prompt)
                    st.session_state.clipboard["arquitetura_solucao"] = final_response
        else:
            st.warning("Por favor, insira pelo menos o Mapeamento AS-IS para análise.")


    if st.session_state.clipboard["arquitetura_solucao"]:
        
        if st.session_state.m2_show_override_button:
            st.divider()
            st.info("💡 **Sugestão de Reaproveitamento (Baseado no Histórico):** Encontramos um projeto similar! A análise e a nova arquitetura foram geradas.")
            
            if st.session_state.m2_display_analysis:
                with st.expander("Ver Análise de Impacto da Adaptação"):
                    st.markdown(st.session_state.m2_display_analysis)

            if st.button("Gerar Arquitetura do Zero (Ignorar Sugestão)", type="primary"):
                with st.spinner("Ignorando sugestão e gerando nova arquitetura do zero..."):
                    original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                    final_response = call_gemini_api(original_prompt)
                    st.session_state.clipboard["arquitetura_solucao"] = final_response
                    st.session_state.m2_show_override_button = False 
                    st.session_state.m2_display_analysis = "" 
                    st.rerun() 

        st.divider()
        st.subheader("Arquitetura de Solução Recomendada")
        st.markdown(st.session_state.clipboard["arquitetura_solucao"])
        
        st.divider()
        st.subheader("Salvar esta Arquitetura")
        project_name_input = st.text_input(
            "Dê um nome para esta Arquitetura de Solução:", 
            placeholder="Ex: Arquitetura - Faturas Fornecedor X",
            key="arch_project_name"
        )
        
        if st.button("Salvar", key="arch_save_button"):
            if project_name_input:
                with st.spinner("Salvando..."):
                    content_to_save = (
                        f"{st.session_state.m2_display_analysis}\n\n"
                        f"---ARQUITETURA-LIMPA---\n\n"
                        f"{st.session_state.clipboard['arquitetura_solucao']}"
                    ) if st.session_state.m2_display_analysis else st.session_state.clipboard['arquitetura_solucao']

                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Arquitetura (Solução)", 
                        content=content_to_save 
                    )
                    if success:
                        st.success(f"Arquitetura '{project_name_input}' salva com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")