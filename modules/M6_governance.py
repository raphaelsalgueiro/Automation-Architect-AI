import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet
from utils.pdf_exporter import create_pdf_bytes 

def run():
    st.header("📜 6. Governança (Final)")
    st.write("O objetivo deste módulo é compilar automaticamente os outputs dos módulos anteriores em um único 'Documento de Governança Discovery-to-Delivery', seguindo o template padrão.")

    # --- INÍCIO DA ATUALIZAÇÃO (CORREÇÃO DE LAYOUT) ---
    # Inicializa as flags de estado para o fluxo de Salvar/Exportar
    if 'gov_save_success' not in st.session_state:
        st.session_state.gov_save_success = False
    if 'clear_gov_name' not in st.session_state:
        st.session_state.clear_gov_name = False
    # --- FIM DA ATUALIZAÇÃO ---

    st.subheader("1. Metadados do Projeto")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        project_name = st.text_input("Nome do Projeto:", placeholder="Ex: Automação Inteligente SAP - Fornecedor X")
    with col2:
        client_name = st.text_input("Nome do Cliente:", placeholder="Ex: Technipfmc (TFMC)")
    with col3:
        author_name = st.text_input("Autor:", value="Raphael Souza / Quality and Innovation")
    
    stakeholders_input = st.text_area(
        "Stakeholders Identificados:", 
        value="• Cliente: \n• DMS Logistics: Raphael Souza, ",
        height=100,
        placeholder="Liste os stakeholders (ex: • Technipfmc: Isabela Floriano...)"
    )

    st.subheader("2. Componentes da Governança (Carregados da Sessão)")
    st.write("Os campos abaixo são preenchidos automaticamente pelo 'Clipboard de Sessão'. Você pode colar/editar o conteúdo se estiver começando por este módulo.")

    doc1_asis = st.text_area(
        "Componente 1: Diagnóstico (AS-IS) (do Módulo 1)",
        value=st.session_state.clipboard.get("diagnostico_asis", ""),
        height=200
    )
    
    doc2_design = st.text_area(
        "Componente 2: Design (PDD / TO-BE) (do Módulo 3)",
        value=st.session_state.clipboard.get("design_pdd", ""),
        height=200
    )

    doc3_delivery = st.text_area(
        "Componente 3: Delivery (Épico, USs, NFRs) (do Módulo 4)",
        value=st.session_state.clipboard.get("delivery_docs", ""),
        height=200
    )

    doc4_qa = st.text_area(
        "Componente 4: QA & Testes (do Módulo 5)",
        value=st.session_state.clipboard.get("qa_plano", ""),
        height=200
    )
    
    all_docs_loaded = all([doc1_asis, doc2_design, doc3_delivery, doc4_qa])
    if not all_docs_loaded:
        st.warning("Um ou mais componentes dos módulos anteriores não foram gerados nesta sessão. Você pode colá-los manualmente acima para prosseguir.")

    if st.button("Gerar Documento de Governança Completo", type="primary"):
        if not all([doc1_asis, doc2_design, doc3_delivery, doc4_qa, project_name, client_name, stakeholders_input]):
            st.error("ERRO: Preencha todos os 5 campos (Metadados e Componentes) antes de gerar o documento.")
        else:
            # Reseta as flags ao gerar um novo documento
            st.session_state.gov_save_success = False
            st.session_state.clear_gov_name = True

            st.session_state.clipboard["diagnostico_asis"] = doc1_asis
            st.session_state.clipboard["design_pdd"] = doc2_design
            st.session_state.clipboard["delivery_docs"] = doc3_delivery
            st.session_state.clipboard["qa_plano"] = doc4_qa
            
            with st.spinner("Compilando seu Documento de Governança..."):
                
                current_date = st.session_state.get('current_date', 'Data não definida')
                
                prompt = f"""
                Você é o "Redator Final" de Governança de Projetos da DMS Logistics.
                Sua tarefa é **ESCREVER** um "Documento de Governança Discovery-to-Delivery" completo e profissional.

                **REGRAS CRÍTICAS:**
                1.  **NÃO COPIE E COLE:** Sua tarefa é **ENTENDER** o [Contexto Bruto] (dos Módulos 1-5) e **ESCREVER** o documento final, **adaptando** o conteúdo para que se encaixe perfeitamente nas seções corretas do [Template Padrão] abaixo.
                2.  **SIGA O TEMPLATE:** O output DEVE seguir a estrutura exata do [Template Padrão] (ex: `### 1.1`, `### 1.2`, `### 2.1`, etc.).
                3.  **SEJA O ESCRITOR:** Você deve escrever ativamente as seções de resumo (`1.3`, `1.4`, `5.1`) com base no contexto.
                4.  **SEJA O REDATOR:** Você deve pegar o conteúdo bruto das seções `2`, `3` e `4` e formatá-lo profissionalmente dentro do template, mantendo as tabelas Markdown geradas.

                ---
                [Contexto Bruto - Módulo 1: Diagnóstico AS-IS]
                {doc1_asis}
                ---
                [Contexto Bruto - Módulo 3: Design PDD]
                {doc2_design}
                ---
                [Contexto Bruto - Módulo 4: Delivery Docs]
                {doc3_delivery}
                ---
                [Contexto Bruto - Módulo 5: QA & Testes]
                {doc4_qa}
                ---

                ---
                [Template Padrão (ESQUELETO OBRIGATÓRIO)]
                (Início do Documento)

                # Documento de Governança Discovery-to-Delivery | {client_name}
                **Projeto:** {project_name}
                **Cliente:** {client_name}
                **Data:** {current_date}
                **Autor:** {author_name}

                ---
                ## SEÇÃO 1: INTRODUÇÃO E GOVERNANÇA DO PROJETO

                ### 1.1 Propósito deste Documento
                Este artefato serve como a "Fonte Única da Verdade" (Single Source of Truth) para o projeto de automação {project_name}. Ele governa o ciclo de vida completo da solução, desde o diagnóstico inicial (Discovery) até a validação final (Delivery), garantindo que as equipes de Negócios, Desenvolvimento e Qualidade estejam perfeitamente alinhadas.

                ### 1.2 Metodologia: O Framework Discovery-to-Delivery
                Este documento está estruturado para seguir o framework "Discovery-to-Delivery", que consiste em três fases principais:
                1.  **Fase 1: Discovery (Diagnóstico):** Mapeamento das regras de negócio e processos atuais (AS-IS) e identificação das lacunas.
                2.  **Fase 2: Delivery (Desenho):** Desenho da solução futura (TO-BE) e tradução em artefatos de engenharia (Épicos, Histórias de Usuário, NFRs).
                3.  **Fase 3: Delivery (Validação):** Definição do Plano de Testes (UAT) para garantir que a solução atende rigorosamente aos requisitos de negócio.

                ### 1.3 Declaração do Problema e Objetivo do Projeto
                (ESCREVA esta seção. Use o [Contexto Bruto - Módulo 1] para resumir o problema e o objetivo do projeto)

                ### 1.4 Escopo da Solução (End-to-End)
                (ESCREVA esta seção. Use o [Contexto Bruto - Módulo 3] para detalhar "Escopo (Inclusões):" e "Fora de Escopo (Exclusões):")

                ### 1.5 Stakeholders Identificados
                {stakeholders_input}

                ---
                ## SEÇÃO 2: FASE 1 - DISCOVERY (DIAGNÓSTICO)
                
                (REESCREVA o [Contexto Bruto - Módulo 1] aqui, garantindo que ele se encaixe perfeitamente na estrutura `### 2.1 Mapeamento de Regras de Negócio` e `### 2.2 Mapeamento de Processo Atual`)

                ---
                ## SEÇÃO 3: FASE 2 - DELIVERY (DESENHO E REQUISITOS)
                
                (REESCREVA o [Contexto Bruto - Módulo 3] e [Contexto Bruto - Módulo 4] aqui, garantindo que eles se encaixem perfeitamente na estrutura `### 3.1` até `### 3.7`)

                ---
                ## SEÇÃO 4: FASE 3 - DELIVERY (VALIDAÇÃO E ACEITE)
                
                (REESCREVA o [Contexto Bruto - Módulo 5] aqui, garantindo que ele se encaixe perfeitamente na estrutura `### 4.1` até `### 4.3`)

                ---
                ## SEÇÃO 5: ANEXOS E HISTÓRICO

                ### 5.1. Glossário de Termos
                (ESCREVA esta seção. Use o contexto de TODOS os módulos para identificar e definir termos-chave como Analysis, Power Automate, SAP, SSLOG, etc.)

                ### 5.2. Histórico de Versões
| Versão | Data | Autor | Mudanças Realizadas |
| :--- | :--- | :--- | :--- |
| 1.0 | {current_date} | {author_name} | Geração inicial do documento via Automation Architect AI |

                (Fim do Documento)
                ---
                """
                
                response_text = call_gemini_api(prompt)
                st.session_state.clipboard["governance_doc"] = response_text

    if st.session_state.clipboard.get("governance_doc"):
        st.divider()
        st.subheader("Documento de Governança Gerado")
        
        governance_doc_markdown = st.session_state.clipboard["governance_doc"]
        
        st.markdown(governance_doc_markdown)
        st.code(governance_doc_markdown, language="markdown")
        st.info("Use o botão no canto superior direito do bloco acima para copiar todo o texto.")
        
        # --- INÍCIO DA ATUALIZAÇÃO (LAYOUT V9.0) ---
        st.divider()
        st.subheader("Salvar ou Exportar este Documento")

        # Verifica a flag ANTES de desenhar o widget
        if st.session_state.get("clear_gov_name", False):
            st.session_state.gov_project_name = ""  # Limpa o valor (permitido aqui)
            st.session_state.clear_gov_name = False # Reseta a flag

        project_name_input = st.text_input(
            "1. Dê um nome para este Documento Final:", 
            placeholder="Ex: Doc Governança - Faturas Fornecedor X",
            key="gov_project_name"
        )
        
        col1_act, col2_act = st.columns([1, 1]) # 50% / 50%
        
        with col1_act: # Bloco de Ação na Esquerda
            if st.button("2. Salvar", key="gov_save_button"):
                if st.session_state.gov_project_name:
                    with st.spinner("Salvando..."):
                        success = save_to_sheet(
                            project_name=st.session_state.gov_project_name, 
                            doc_type="Governança (Final)", 
                            content=governance_doc_markdown 
                        )
                        if success:
                            st.success(f"Documento '{st.session_state.gov_project_name}' salvo com sucesso!")
                            st.session_state.gov_save_success = True
                        else:
                            st.error("Falha ao salvar o projeto.")
                            st.session_state.gov_save_success = False
                else:
                    st.warning("Por favor, dê um nome ao projeto para salvá-lo.")
                    st.session_state.gov_save_success = False

            # Mostra o botão Exportar logo abaixo do Salvar, mas só após o sucesso
            if st.session_state.gov_save_success and st.session_state.gov_project_name:
                pdf_file_name = f"{st.session_state.gov_project_name.replace(' ', '_')}.pdf"
                pdf_bytes = create_pdf_bytes(governance_doc_markdown)
                
                if pdf_bytes:
                    st.download_button(
                        label="3. Exportar para PDF",
                        data=pdf_bytes,
                        file_name=pdf_file_name,
                        mime="application/pdf"
                    )
        
        # col2_act fica intencionalmente vazia
        # --- FIM DA ATUALIZAÇÃO ---