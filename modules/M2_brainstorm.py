import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet, load_from_sheet # <-- IMPORTAMOS O load_from_sheet

# --- NOVAS FUNÇÕES DE PROMPT ---

def get_original_architecture_prompt(as_is_input, client_request):
    """Gera o prompt original do Módulo 2 (criar do zero)."""
    return f"""
    Você é um Arquiteto de Soluções Sênior, especialista em **Power Automate (Cloud e Desktop)** e na ferramenta de IA interna **"Analysis"** .
    Sua tarefa é analisar o mapeamento do processo atual (AS-IS) e propor A MELHOR "Arquitetura de Solução Recomendada" usando **EXCLUSIVAMENTE** essa stack.

    A sua resposta deve ser um único documento estruturado, contendo:
    1.  **Visão Geral da Solução:** (Um parágrafo resumindo a solução completa) .
    2.  **Arquitetura Recomendada (Fases):** (Ex: "Fase 1: Extração com Analysis", "Fase 2: Lançamento com Power Automate Desktop").
    3.  **Divisão de Responsabilidades (IMPORTANTE):**
        * **Responsabilidades do "Analysis":** (O que o Analysis fará? Ex: Extrair campos X, Y, Z , classificar documentos , requerer prompts customizados para Fornecedor B).
        * **Responsabilidades do "Power Automate":** (O que o Power Automate fará? Ex: Monitorar a fonte , orquestrar as chamadas ao Analysis, fazer login no SAP , tratar exceções, integrar com o Unico Doc ).
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

def get_finder_prompt(as_is_input, client_request, historical_docs_string):
    """
    Gera o novo prompt "inteligente" que busca no histórico ANTES
    de decidir criar um novo.
    """
    return f"""
    Você é um Arquiteto de Soluções Sênior especialista em Power Automate e Analysis (Ferramenta de Inteligência Artificial).

    Sua primeira tarefa é analisar o [Novo Diagnóstico AS-IS] e compará-lo com o [Histórico de Projetos Anteriores].
    
    1.  **Analise o [Novo Diagnóstico AS-IS]:** Entenda o problema central.
    2.  **Compare com o [Histórico]:** Procure por um projeto no histórico que seja altamente similar (mais de 70% de sobreposição de processo ou regras) e que possa ser REAPROVEITADO.
    3.  **Tome uma Decisão:**

        * **SE VOCÊ ENCONTRAR UM PROJETO SIMILAR:**
            Sua resposta deve começar **EXATAMENTE** com a tag `[REUTILIZAR]`.
            Após a tag, gere um "Documento de Adaptação" (baseado no Módulo 7):
            - Identifique o projeto similar (ex: "Baseado no projeto 'Automação Fornecedor A'...")
            - Gere um novo Documento de Governança (Seções 1-5 ) adaptado para o novo diagnóstico.
            - [cite_start]DESTAQUE todas as mudanças necessárias usando `**[MUDANÇA]**` ou `**[NOVO]**` (ex: "O Power Automate deve agora acessar o SharePoint em vez do SAP" [cite: 1-170]).

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

# --- FUNÇÃO PRINCIPAL DO MÓDULO ---

def run():
    st.header("🧠 2. Arquitetura (Solução)")
    st.write("O objetivo deste módulo é propor a melhor arquitetura de solução, usando **Power Automate** e **Analysis**. A ferramenta irá primeiro verificar seu histórico por projetos reaproveitáveis.")

    # Inicializa os estados da sessão para este módulo
    if 'm2_suggestion_made' not in st.session_state:
        st.session_state.m2_suggestion_made = False
        st.session_state.m2_suggestion_text = ""

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
            # Limpa os estados anteriores
            st.session_state.m2_suggestion_made = False
            st.session_state.m2_suggestion_text = ""
            st.session_state.clipboard["arquitetura_solucao"] = ""
            
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["diagnostico_asis"] = as_is_input

            with st.spinner("Analisando o histórico por projetos similares..."):
                # 1. Carregar Histórico
                all_records = load_from_sheet()
                gov_records = [
                    r['Conteudo_Gerado'] for r in all_records 
                    if r.get('Tipo_De_Documento') == 'Governança (Final)'
                ]
                
                final_response = ""

                if gov_records:
                    # 2. Se o histórico existir, rodar a "Busca Inteligente"
                    historical_docs_string = "\n\n".join(
                        [f"--- PROJETO ANTIGO {i+1} ---\n{doc}" for i, doc in enumerate(gov_records)]
                    )
                    finder_prompt = get_finder_prompt(as_is_input, client_request, historical_docs_string)
                    finder_response = call_gemini_api(finder_prompt)

                    if finder_response.strip() == "[NOVO]":
                        # 3a. Nenhum projeto similar, gerar do zero
                        with st.spinner("Nenhum projeto similar encontrado. Gerando nova arquitetura..."):
                            original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                            final_response = call_gemini_api(original_prompt)
                            st.session_state.clipboard["arquitetura_solucao"] = final_response
                    
                    elif finder_response.startswith("[REUTILIZAR]"):
                        # 3b. Projeto similar encontrado! Mostrar sugestão.
                        st.session_state.m2_suggestion_made = True
                        st.session_state.m2_suggestion_text = finder_response.replace("[REUTILIZAR]", "").strip()
                    
                    else:
                        # Fallback: Se a IA não retornar as tags certas, apenas gere do zero
                        st.warning("A IA não retornou uma tag válida. Gerando arquitetura do zero.")
                        original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                        final_response = call_gemini_api(original_prompt)
                        st.session_state.clipboard["arquitetura_solucao"] = final_response

                else:
                    # 4. Histórico vazio, gerar do zero
                    st.info("Nenhum projeto de governança encontrado no histórico. Gerando nova arquitetura...")
                    original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                    final_response = call_gemini_api(original_prompt)
                    st.session_state.clipboard["arquitetura_solucao"] = final_response
        else:
            st.warning("Por favor, insira pelo menos o Mapeamento AS-IS para análise.")

    # --- LÓGICA DE RENDERIZAÇÃO PÓS-BOTÃO ---

    # CASO 1: Mostra a sugestão de reutilização
    if st.session_state.m2_suggestion_made:
        st.divider()
        st.subheader("Sugestão de Reaproveitamento (Baseado no Histórico)")
        st.info("💡 Encontramos um projeto similar no seu histórico! Você pode adaptar este projeto ou gerar uma nova arquitetura do zero.")
        st.markdown(st.session_state.m2_suggestion_text)
        
        st.divider()
        if st.button("Gerar Arquitetura do Zero (Ignorar Sugestão)", type="primary"):
            with st.spinner("Ignorando sugestão e gerando nova arquitetura do zero..."):
                original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                final_response = call_gemini_api(original_prompt)
                st.session_state.clipboard["arquitetura_solucao"] = final_response
                st.session_state.m2_suggestion_made = False
                st.rerun() # Recarrega a página para mostrar o resultado final

    # CASO 2: Mostra o resultado final (seja ele gerado do zero ou após ignorar a sugestão)
    if st.session_state.clipboard["arquitetura_solucao"] and not st.session_state.m2_suggestion_made:
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
                with st.spinner("Salvando na planilha..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Arquitetura (Solução)", 
                        content=st.session_state.clipboard["arquitetura_solucao"]
                    )
                    if success:
                        st.success(f"Arquitetura '{project_name_input}' salva com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")