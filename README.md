# 🤖 Automation Architect AI (v4.0)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automation-architect-ai-emhu7fwq2hpyzs447qkep5.streamlit.app/)

Uma ferramenta de I.A. (co-piloto) para Gestores de Projetos, Analistas de Requisitos e Desenvolvedores de Automação, especializada em acelerar o ciclo de vida "Discovery-to-Delivery" para a stack de **Power Automate** e **Analysis** (IA interna).

---

### ✨ Funcionalidades Principais (v4.0)

Esta ferramenta evoluiu de um simples gerador de documentos para um assistente inteligente com memória de longo prazo.

* **Busca Inteligente no Histórico (Módulo 2):** Ao invés de sempre criar do zero, a ferramenta agora **verifica o histórico** (Google Sheets) por projetos similares. Se encontrar uma automação 80% compatível, ela sugere a **reutilização**, gerando um plano de adaptação (lógica do Módulo 7) automaticamente.
* **Geração de Backlog por Função (Módulo 4):** A ferramenta entende a divisão de tarefas da equipe. O Módulo de Delivery agora gera Histórias de Usuário separadas para o **Desenvolvedor Power Automate** e para o **Engenheiro do Analysis**.
* **Upload de Múltiplos Formatos (Módulo 1):** O usuário não está mais restrito a colar texto. O Módulo de Diagnóstico agora aceita o **upload de arquivos** (`.pdf`, `.docx`, `.txt`), extraindo o texto automaticamente.
* **Exportação para PDF (Módulo 6):** O Documento de Governança final, gerado no Módulo 6, pode ser **exportado como um arquivo PDF** com um único clique.
* **Arquitetura de "Memória Dupla":**
    * **Memória de Sessão:** (Clipboard) Passa dados automaticamente entre os módulos (M1 -> M2 -> M3...).
    * **Memória de Longo Prazo:** (Google Sheets) Salva o trabalho de forma permanente para consulta e para alimentar a "Busca Inteligente".
* **Arquitetura Flexível:** O usuário pode pular etapas e começar o fluxo de qualquer módulo (ex: colar um PDD direto no Módulo 4).

### ⚙️ O Fluxo de Trabalho (Módulos)

1.  **💡 1. Diagnóstico (AS-IS):**
    * Recebe anotações de reunião (via `st.text_area`) **OU** arquivos de requisitos do cliente (via `st.file_uploader`).
    * A I.A. lê todo o material e gera o "Processo AS-IS" e as "Regras de Negócio".

2.  **🧠 2. Arquitetura (Solução):**
    * **Passo 1 (Busca Inteligente):** Compara o "AS-IS" com todos os projetos salvos no Google Sheets.
    * **Passo 2 (Decisão):**
        * **SE** encontrar um projeto similar, sugere a **reutilização** e gera o plano de adaptação. O usuário pode aceitar ou clicar em **"Gerar Arquitetura do Zero"** (override).
        * **SE NÃO** encontrar, gera uma nova arquitetura do zero, focada em **Power Automate + Analysis**.

3.  **✍️ 3. Design (TO-BE):**
    * Gera o PDD (Process Design Document) completo.
    * O PDD agora é dividido em `3.2.1. Fluxo de Orquestração (Power Automate)` e `3.2.2. Requisitos de Extração (Analysis)`.

4.  **📄 4. Delivery (Docs):**
    * Gera **todos os 5 artefatos de entrega**: Épico, Requisitos Funcionais (RFs), Requisitos Não Funcionais (NFRs), Histórias de Usuário (USs) e Critérios de Aceitação (CAs).
    * As Histórias de Usuário são divididas por função (Power Automate vs. Analysis).

5.  **🧪 5. QA & Testes:**
    * Gera o Plano de Testes (UAT) focado na stack (ex: "O que acontece se o Analysis tiver baixa confiança?" ou "E se o Power Automate não encontrar o seletor?").

6.  **📜 6. Governança (Final):**
    * Compila todos os inputs do fluxo em um Documento de Governança final, seguindo o template padrão (TFMC).
    * Permite o **download imediato do documento em PDF**.

7.  **🔄 7. Refinar:**
    * Um fluxo "fast-track" (agora também usado pelo Módulo 2) para carregar um projeto antigo, descrever as mudanças (ex: "novo fornecedor") e gerar um **novo Documento de Governança completo e adaptado**, destacando as mudanças com `**[MUDANÇA]**`.

### 🛠️ Tecnologias Utilizadas

* **Front-End:** Streamlit
* **Back-End / Lógica:** Python
* **Inteligência:** Google Generative AI (Gemini)
* **Armazenamento (Longo Prazo):** Google Sheets API (`gspread`)
* **Processamento de Arquivos:** `pdfplumber`, `python-docx`
* **Geração de PDF:** `fpdf2`, `markdown2`

### 🚀 Como Executar o Projeto Localmente

**1. Clone o Repositório:**
```bash
git clone [https://github.com/raphaelsalgueiro/Automation-Architect-AI.git](https://github.com/raphaelsalgueiro/Automation-Architect-AI.git)
cd Automation-Architect-AI