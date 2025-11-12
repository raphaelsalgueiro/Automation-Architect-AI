# 🤖 Automation Architect AI (v5.0)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automation-architect-ai-emhu7fwq2hpyzs447qkep5.streamlit.app/)

Uma ferramenta de I.A. (co-piloto) para Gestores de Projetos, Analistas de Requisitos e Desenvolvedores de Automação, especializada em acelerar o ciclo de vida "Discovery-to-Delivery" para a stack de **Power Automate** e **Analysis** (IA interna).

---

### ✨ Funcionalidades Principais (v5.0)

Esta ferramenta evoluiu de um simples gerador de documentos para um assistente inteligente com memória de longo prazo e capacidade de visualização de dados.

* **Página Inicial (Dashboard de Projetos):** A ferramenta agora abre em um dashboard (Módulo 0) que lê o histórico do Google Sheets e exibe KPIs gerenciais (Total de Projetos, Concluídos) e um gráfico de distribuição (via Altair).
* **Busca Inteligente no Histórico (Módulo 2):** Ao invés de sempre criar do zero, a ferramenta agora **verifica o histórico** por projetos similares. Se encontrar uma automação compatível, ela sugere a **reutilização**, gerando um plano de adaptação.
* **Geração de Backlog por Função (Módulo 4):** A ferramenta gera Histórias de Usuário separadas para o **Desenvolvedor Power Automate** e para o **Engenheiro do Analysis**, com numeração lógica e sequencial (corrigido na v4.2).
* **Upload de Múltiplos Formatos (Módulo 1):** O usuário pode **colar texto** ou fazer **upload de arquivos** (`.pdf`, `.docx`, `.txt`), e a ferramenta combina os inputs para a IA.
* **Exportação para PDF (Módulo 6):** O Documento de Governança final pode ser **exportado como um arquivo PDF** (estável, 100% Python via `fpdf2`).
* **Arquitetura de "Memória Dupla":**
    * **Memória de Sessão:** (Clipboard) Passa dados automaticamente entre os módulos.
    * **Memória de Longo Prazo:** (Google Sheets) Salva o trabalho para alimentar o Dashboard e a "Busca Inteligente".
* **Arquitetura Flexível:** O usuário pode pular etapas e começar o fluxo de qualquer módulo (ex: colar um PDD direto no Módulo 4).

### ⚙️ O Fluxo de Trabalho (Módulos)

1.  **📊 0. Dashboard:**
    * A "página inicial" da aplicação. Mostra KPIs e gráficos baseados no histórico do Google Sheets.

2.  **💡 1. Diagnóstico (AS-IS):**
    * Recebe anotações (texto) ou arquivos (`.pdf`, `.docx`). A IA lê tudo e gera o "Processo AS-IS".

3.  **🧠 2. Arquitetura (Solução):**
    * **Passo 1 (Busca Inteligente):** Compara o "AS-IS" com o histórico do Google Sheets.
    * **Passo 2 (Decisão):**
        * **SE** encontrar um projeto similar, sugere a **reutilização**.
        * **SE NÃO** encontrar, gera uma nova arquitetura (Power Automate + Analysis).
        * O usuário sempre tem o botão **"Gerar Arquitetura do Zero"** (override).

4.  **✍️ 3. Design (TO-BE):**
    * Gera o PDD (Process Design Document) 100% em **texto**, com seções claras para o `Fluxo de Orquestração (Power Automate)` e os `Requisitos de Extração (Analysis)`.

5.  **📄 4. Delivery (Docs):**
    * Gera **todos os 5 artefatos de entrega** (Épico, RFs, NFRs, USs, CAs) em uma **sequência numérica lógica e corrigida (v4.2)**.

6.  **🧪 5. QA & Testes:**
    * Gera o Plano de Testes (UAT) focado na stack (Exceções do Analysis, falhas de UI do Power Automate).

7.  **📜 6. Governança (Final):**
    * Compila os 4 artefatos em um Documento de Governança final (baseado no template TFMC).
    * Permite o **download imediato do documento em PDF**.

8.  **🔄 7. Refinar:**
    * Fluxo "fast-track" para carregar um projeto antigo, descrever mudanças e gerar um novo Documento de Governança adaptado (em texto), destacando as `**[MUDANÇAS]**`.

### 🛠️ Tecnologias Utilizadas

* **Front-End:** Streamlit
* **Visualização:** Altair (para o Dashboard)
* **Back-End / Lógica:** Python
* **Inteligência:** Google Generative AI (Gemini)
* **Armazenamento (Longo Prazo):** Google Sheets API (`gspread`)
* **Processamento de Arquivos:** `pdfplumber`, `python-docx`
* **Geração de PDF:** `fpdf2`, `markdown2`

### 🚀 Como Executar o Projeto Localmente

**1. Clone o Repositório:**