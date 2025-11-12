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

# --- PROMPT 2: BUSCAR E REUTILIZAR (PROMPT REFINADO V4.2) ---
# (Este prompt foi melhorado para ser mais rigoroso e completo)
def get_finder_prompt(as_is_input, client_request, historical_docs_string):
    """
    Gera o novo prompt "inteligente" (v4.2) que busca no histórico
    e gera uma análise de impacto completa (resolvendo o Ponto 3).
    """
    return f"""
    Você é um Arquiteto de Soluções Sênior especialista em Power Automate e Analysis.

    Sua primeira tarefa é analisar o [Novo Diagnóstico AS-IS] e compará-lo com o [Histórico de Projetos Anteriores].
    
    1.  **Analise o [Novo Diagnóstico AS-IS]:** Entenda o problema central.
    2.  **Compare com o [Histórico]:** Procure por um projeto no histórico que seja altamente similar (mais de 80% de sobreposição de processo ou regras) e que possa ser REAPROVEITADO.
    3.  **Tome uma Decisão:**

        * **SE VOCÊ ENCONTRAR UM PROJETO SIMILAR:**
            Sua resposta deve começar **EXATAMENTE** com a tag `[REUTILIZAR]`.
            Após a tag, gere um "Documento de Adaptação" completo (baseado no template TFMC ).
            
            **ESTRUTURA OBRIGATÓRIA DA RESPOSTA [REUTILIZAR]:**

            **Projeto Similar Identificado:** (Ex: "Baseado no projeto 'Automação Fornecedor A'...")
            
            **Análise de Impacto da Adaptação (Ponto 3):**
            [cite_start](Descreva o que muda em *todas* as seções do documento de governança [cite: 1-170] para atender ao novo diagnóstico).
            * [cite_start]**Seção 3 (Design/PDD):** (Ex: `**[MUDANÇA]**` O fluxo do Power Automate deve ser alterado para acessar o SharePoint em vez do Oracle EBS [cite: 1-170].)
            * **Seção 4 (Delivery Docs):** (Ex: `**[NOVO]**` Novas Histórias de Usuário (US-P7, US-A5) serão necessárias para a integração com o SharePoint. Os RFs 04 e 05 precisam ser atualizados.)
            * **Seção 5 (QA & Testes):** (Ex: `**[NOVO]**` Novos cenários de teste (HP-05, EXC-07) devem ser criados para validar a integração com o SharePoint.)

            **Documento de Governança Adaptado (Rascunho):**
            [cite_start](Gere o documento de governança completo, Seções 1-5 [cite: 1-170], já com as adaptações e as tags `**[MUDANÇA]**` ou `**[NOVO]**` aplicadas no texto.)

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
    st.write("O objetivo deste módulo é propor a melhor arquitetura de solução, usando **Power Automate** e **Analysis** (IA Interna). A ferramenta irá primeiro verificar seu histórico por projetos reaproveitáveis.")

    # Estado para controlar se o botão "Gerar do Zero" deve ser mostrado
    if 'm2_show_override_button' not in st.session_state:
        st.session_state.m2_show_override_button = False

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
            st.session_state.m2_show_override_button = False
            st.session_state.clipboard["arquitetura_solucao"] = ""
            
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
                        with st.spinner("Nenhum projeto similar encontrado. Gerando nova arquitetura..."):
                            original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                            final_response = call_gemini_api(original_prompt)
                            st.session_state.clipboard["arquitetura_solucao"] = final_response
                            st.session_state.m2_show_override_button = False # Não mostre o override
                    
                    elif finder_response.startswith("[REUTILIZAR]"):
                        # --- INÍCIO DA CORREÇÃO (Ponto 1 e 2) ---
                        st.session_state.m2_show_override_button = True # Mostre o override
                        suggestion_text = finder_response.replace("[REUTILIZAR]", "").strip()
                        
                        # Salva a sugestão no clipboard principal para o Módulo 3
                        st.session_state.clipboard["arquitetura_solucao"] = suggestion_text
                        # --- FIM DA CORREÇÃO ---
                    
                    else:
                        st.warning("A IA não retornou uma tag válida. Gerando arquitetura do zero.")
                        original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                        final_response = call_gemini_api(original_prompt)
                        st.session_state.clipboard["arquitetura_solucao"] = final_response
                        st.session_state.m2_show_override_button = False

                else:
                    st.info("Nenhum projeto de governança encontrado no histórico. Gerando nova arquitetura...")
                    original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                    final_response = call_gemini_api(original_prompt)
                    st.session_state.clipboard["arquitetura_solucao"] = final_response
                    st.session_state.m2_show_override_button = False
        else:
            st.warning("Por favor, insira pelo menos o Mapeamento AS-IS para análise.")

    # --- LÓGICA DE RENDERIZAÇÃO PÓS-BOTÃO (REFINADA V4.2) ---

    # Esta seção agora renderiza SEMPRE que o clipboard tiver conteúdo,
    # resolvendo o Ponto 1 (Botão Salvar) e Ponto 2 (Módulo 3).
    if st.session_state.clipboard["arquitetura_solucao"]:
        
        # Mostra o botão "Gerar do Zero" SE uma sugestão foi feita
        if st.session_state.m2_show_override_button:
            st.divider()
            st.info("💡 **Sugestão de Reaproveitamento (Baseado no Histórico):** Encontramos um projeto similar! O plano de adaptação (abaixo) foi carregado. Você pode aceitá-lo (e ir para o Módulo 3) ou gerar uma arquitetura do zero.")
            
            if st.button("Gerar Arquitetura do Zero (Ignorar Sugestão)", type="primary"):
                with st.spinner("Ignorando sugestão e gerando nova arquitetura do zero..."):
                    original_prompt = get_original_architecture_prompt(as_is_input, client_request)
                    final_response = call_gemini_api(original_prompt)
                    st.session_state.clipboard["arquitetura_solucao"] = final_response
                    st.session_state.m2_show_override_button = False # Esconde o botão
                    st.rerun() # Recarrega a página para mostrar o novo resultado

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