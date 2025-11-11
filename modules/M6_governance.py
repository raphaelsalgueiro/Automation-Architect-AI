import streamlit as st
from utils.gemini_handler import call_gemini_api
from utils.sheets_handler import save_to_sheet
from utils.pdf_exporter import create_pdf_bytes  # <-- IMPORTAMOS O EXPORTADOR

def run():
    st.header("📜 6. Governança (Final)")
    st.write("O objetivo deste módulo é compilar automaticamente os outputs dos módulos anteriores em um único 'Documento de Governança Discovery-to-Delivery', seguindo o seu template padrão.")

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
            # Atualiza o clipboard caso o usuário tenha colado manualmente
            st.session_state.clipboard["diagnostico_asis"] = doc1_asis
            st.session_state.clipboard["design_pdd"] = doc2_design
            st.session_state.clipboard["delivery_docs"] = doc3_delivery
            st.session_state.clipboard["qa_plano"] = doc4_qa
            
            with st.spinner("Compilando seu Documento de Governança..."):
                
                current_date = st.session_state.get('current_date', 'Data não definida')
                
                prompt = f"""
                Você é Raphael Souza, especialista em Governança de Projetos da DMS Logistics .
                Sua tarefa é gerar um "Documento de Governança Discovery-to-Delivery" completo, profissional e formatado em Markdown, com base no template e nos 4 blocos de conteúdo fornecidos.

                TAREFA 1 (IA GERADORA): Você deve LER os [Bloco 1: Diagnóstico] e [Bloco 2: Design] para entender o problema e a solução. Com base neles, você deve **ESCREVER** as seções:
                * `### 1.3 Declaração do Problema e Objetivo do Projeto` (Resuma o Bloco 1) [based on source: 18-20].
                * `### 1.4 Escopo da Solução (End-to-End)` (Resuma o Bloco 2, focando em Inclusões e Exclusões) [based on source: 22-34].
                * `### 5.1. Glossário de Termos` (Sugira termos-chave com base em todos os blocos, ex: Analysis, Power Automate, FRS, RM, SAP, Unico Doc) [based on source: 152-163].

                TAREFA 2 (IA COMPILADORA): Ao inserir os 4 blocos de conteúdo, sua tarefa é **limpar o texto**. REMOVA quaisquer frases introdutórias ou meta-comentários (Ex: "Aqui está o PDD..."). Insira apenas o conteúdo de governança bruto.

                O documento DEVE seguir esta estrutura exata :

                ---
                (Início do Documento)

                # Documento de Governança Discovery-to-Delivery | {client_name} 
                **Projeto:** {project_name} 
                **Cliente:** {client_name} 
                **Data:** {current_date} 
                **Autor:** {author_name} 

                ---
                ## SEÇÃO 1: INTRODUÇÃO E GOVERNANÇA DO PROJETO 

                ### 1.1 Propósito deste Documento 
                Este artefato serve como a "Fonte Única da Verdade" (Single Source of Truth) para o projeto de automação {project_name}. Ele governa o ciclo de vida completo da solução, desde o diagnóstico inicial (Discovery) até a validação final (Delivery), garantindo que as equipes de Negócios, Desenvolvimento e Qualidade estejam perfeitamente alinhadas .

                ### 1.2 Metodologia: O Framework Discovery-to-Delivery 
                Este documento está estruturado para seguir o framework "Discovery-to-Delivery", que consiste em três fases principais:
                1.  **Fase 1: Discovery (Diagnóstico):** Mapeamento das regras de negócio e processos atuais (AS-IS) e identificação das lacunas .
                2.  **Fase 2: Delivery (Desenho):** Desenho da solução futura (TO-BE) e tradução em artefatos de engenharia (Épicos, Histórias de Usuário, NFRs) .
                3.  **Fase 3: Delivery (Validação):** Definição do Plano de Testes (UAT) para garantir que a solução atende rigorosamente aos requisitos de negócio .

                ### 1.3 Declaração do Problema e Objetivo do Projeto 
                (GERE ESTA SEÇÃO AUTOMATICAMENTE COM BASE NO [Bloco 1: Diagnóstico])

                ### 1.4 Escopo da Solução (End-to-End) 
                (GERE ESTA SEÇÃO AUTOMATICAMENTE COM BASE NO [Bloco 2: Design]. Detalhe "Escopo (Inclusões):" e "Fora de Escopo (Exclusões):") [based on source: 22-34]

                ### 1.5 Stakeholders Identificados 
                {stakeholders_input}

                ---
                ## SEÇÃO 2: FASE 1 - DISCOVERY (DIAGNÓSTICO) 
                
                {doc1_asis}

                ---
                ## SEÇÃO 3: FASE 2 - DELIVERY (DESENHO E REQUISITOS) 
                
                (INSIRA O [Bloco 2: Design] AQUI)
                {doc2_design}

                (INSIRA O [Bloco 3: Delivery] AQUI)
                {doc3_delivery}

                ---
                ## SEÇÃO 4: FASE 3 - DELIVERY (VALIDAÇÃO E ACEITE) 
                
                (INSIRA O [Bloco 4: QA & Testes] AQUI)
                {doc4_qa}

                ---
                ## SEÇÃO 5: ANEXOS E HISTÓRICO 

                ### 5.1. Glossário de Termos 
                (GERE ESTA SEÇÃO AUTOMATICAMENTE, sugerindo termos-chave como Power Automate, Analysis, FRS, RM, SAP, Unico Doc, VM, etc.) [based on source: 152-163]

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
        
        # Armazena o documento gerado em uma variável para reuso
        governance_doc_markdown = st.session_state.clipboard["governance_doc"]
        
        st.markdown(governance_doc_markdown)
        
        st.code(governance_doc_markdown, language="markdown")
        st.info("Use o botão no canto superior direito do bloco acima para copiar todo o texto.")
        
        # --- INÍCIO DA IMPLEMENTAÇÃO (EXPORTAR PDF) ---
        st.divider()
        st.subheader("Exportar Documento")

        # Usamos o 'project_name' do input para criar um nome de arquivo dinâmico
        # Se estiver vazio, usamos um nome padrão
        pdf_file_name = f"{project_name.replace(' ', '_') if project_name else 'Documento_Governança'}.pdf"
        
        # Geramos o PDF em memória (bytes)
        pdf_bytes = create_pdf_bytes(governance_doc_markdown)
        
        if pdf_bytes:
            st.download_button(
                label="Exportar para PDF",
                data=pdf_bytes,
                file_name=pdf_file_name,
                mime="application/pdf"
            )
        # --- FIM DA IMPLEMENTAÇÃO ---
        
        st.divider()
        st.subheader("Salvar este Documento de Governança")
        project_name_input = st.text_input(
            "Dê um nome para este Documento Final:", 
            placeholder="Ex: Doc Governança - Faturas Fornecedor X",
            key="gov_project_name"
        )
        
        if st.button("Salvar", key="gov_save_button"):
            if project_name_input:
                with st.spinner("Salvando na planilha..."):
                    success = save_to_sheet(
                        project_name=project_name_input, 
                        doc_type="Governança (Final)", 
                        content=governance_doc_markdown # Reusa a variável
                    )
                    if success:
                        st.success(f"Documento '{project_name_input}' salvo com sucesso!")
                    else:
                        st.error("Falha ao salvar o projeto.")
            else:
                st.warning("Por favor, dê um nome ao projeto para salvá-lo.")