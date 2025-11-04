import streamlit as st
from utils.gemini_handler import call_gemini_api

def run():
    st.header("📜 6. Governança (Final)")
    st.write("O objetivo deste módulo é compilar os outputs dos módulos anteriores em um único 'Documento de Governança Discovery-to-Delivery', seguindo o padrão da sua empresa.")
    st.info("Preencha os metadados e os 4 outputs para gerar o documento final.")

    st.subheader("1. Metadados do Projeto")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        project_name = st.text_input("Nome do Projeto:", placeholder="Ex: Automação Inteligente SAP")
    with col2:
        client_name = st.text_input("Nome do Cliente:", placeholder="Ex: Technipfmc (TFMC)")
    with col3:
        author_name = st.text_input("Autor:", value="Raphael Souza / Quality and Innovation")
    
    # --- CAMPO MANUAL REMOVIDO ---
    # O campo "Problem Statement" foi removido. A I.A. vai gerar isso.

    st.subheader("2. Conteúdo dos Módulos Anteriores")

    discovery_content = st.text_area(
        "Módulo 💡 1. Diagnóstico (AS-IS):",
        height=200,
        placeholder="Cole o resultado do módulo 'Diagnóstico' (Regras de Negócio, AS-IS, Gaps) aqui..."
    )
    
    design_content = st.text_area(
        "Módulo ✍️ 3. Design (TO-BE):",
        height=200,
        placeholder="Cole o resultado do módulo 'Design' (Fluxo TO-BE) aqui..."
    )

    delivery_content = st.text_area(
        "Módulo 📄 4. Delivery (Docs):",
        height=200,
        placeholder="Cole o resultado do módulo 'Delivery' (Épico, User Stories, NFRs) aqui..."
    )

    qa_content = st.text_area(
        "Módulo 🧪 5. QA & Testes:",
        height=200,
        placeholder="Cole o resultado do módulo 'QA & Testes' (Plano de UAT) aqui..."
    )

    if st.button("Gerar Documento de Governança Completo", type="primary"):
        # Verificação atualizada: removemos o 'problem_statement'
        if discovery_content and design_content and delivery_content and qa_content and project_name and client_name:
            with st.spinner("Compilando seu Documento de Governança..."):
                
                current_date = st.session_state.get('current_date', 'Data não definida')
                
                # --- PROMPT MESTRE ATUALIZADO ---
                # Agora a I.A. tem a tarefa de ESCREVER a Seção 1.3
                
                prompt = f"""
                Você é Raphael Souza, especialista em Governança de Projetos da DMS Logistics.
                Sua tarefa é gerar um "Documento de Governança Discovery-to-Delivery" completo, profissional e formatado em Markdown, com base no template e nos 4 blocos de conteúdo fornecidos.

                O documento DEVE seguir esta estrutura exata:

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
                Este artefato serve como a "Fonte Única da Verdade" (Single Source of Truth) para o projeto de automação {project_name}. Ele governa o ciclo de vida completo da solução, desde o diagnóstico inicial (Discovery) até a validação final (Delivery).

                ### 1.2 Metodologia: O Framework Discovery-to-Delivery
                Este documento está estruturado para seguir o framework "Discovery-to-Delivery", que consiste em três fases principais:
                1.  **Fase 1: Discovery (Diagnóstico):** Mapeamento das regras de negócio e processos atuais (AS-IS) e identificação das lacunas.
                2.  **Fase 2: Delivery (Desenho):** Desenho da solução futura (TO-BE) e tradução em artefatos de engenharia (Épicos, Histórias de Usuário, NFRS).
                3.  **Fase 3: Delivery (Validação):** Definição do Plano de Testes (UAT) para garantir que a solução atende rigorosamente aos requisitos de negócio.

                ### 1.3 Declaração do Problema e Objetivo do Projeto
                **SUA TAREFA AQUI:** Com base no conteúdo do [Bloco 1: Discovery], escreva um parágrafo conciso (3-5 frases) que resuma a "principal dor" (os gargalos) e o "objetivo do projeto" (o que a automação visa resolver), similar ao exemplo da TFMC.
                
                ---
                ## SEÇÃO 2: FASE 1 - DISCOVERY (DIAGNÓSTICO)
                **SUA TAREFA AQUI:** Insira o [Bloco 1: Discovery] abaixo. Limpe o texto, removendo quaisquer frases introdutórias ou meta-comentários (Ex: "Este diagnóstico é focado 100%...", "Como especialista..."). Insira apenas o conteúdo de governança bruto (Mapeamento de Regras de Negócio, Mapeamento de Processo AS-IS).
                
                {discovery_content}

                ---
                ## SEÇÃO 3: FASE 2 - DELIVERY (DESENHO E REQUISITOS)

                ### 3.1. Visão da Solução e Processo Futuro (TO-BE)
                **SUA TAREFA AQUI:** Insira o [Bloco 2: Design] abaixo. Limpe o texto de quaisquer meta-comentários.
                
                {design_content}

                ### 3.2. Artefatos de Desenvolvimento (Épico, User Stories, NFRs)
                **SUA TAREFA AQUI:** Insira o [Bloco 3: Delivery] abaixo. Limpe o texto de quaisquer meta-comentários.
                
                {delivery_content}

                ---
                ## SEÇÃO 4: FASE 3 - DELIVERY (VALIDAÇÃO E ACEITE)
                **SUA TAREFA AQUI:** Insira o [Bloco 4: QA & Testes] abaixo. Limpe o texto de quaisquer meta-comentários.
                
                {qa_content}

                ---
                ## SEÇÃO 5: ANEXOS E HISTÓRICO

                ### 5.1. Histórico de Versões
                | Versão | Data | Autor | Mudanças Realizadas |
                | :--- | :--- | :--- | :--- |
                | 1.0 | {current_date} | {author_name} | Geração inicial do documento via Automation Architect AI |

                (Fim do Documento)
                ---
                """
                
                response_text = call_gemini_api(prompt)
                st.divider()
                st.subheader("Documento de Governança Gerado")
                st.markdown(response_text)
                
                st.code(response_text, language="markdown")
                st.info("Use o botão no canto superior direito do bloco acima para copiar todo o texto.")
        else:
            st.warning("Por favor, preencha todos os campos de metadados e os 4 campos de conteúdo para gerar o documento.")