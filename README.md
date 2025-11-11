# 🤖 Automation Architect AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automation-architect-ai-emhu7fwq2hpyzs447qkep5.streamlit.app/)

Uma ferramenta de I.A. construída com Python e Streamlit para atuar como um co-piloto para Gestores de Projetos, Analistas de Requisitos e Consultores de Automação, especializada no stack Power Automate e I.A.s customizadas.

---

### 🎯 Sobre o Projeto

O **Automation Architect AI** resolve um desafio central no desenvolvimento de projetos de automação e I.A.: a tradução de necessidades de negócio em artefatos técnicos claros e acionáveis.

A ferramenta guia o usuário por um fluxo de trabalho de ponta a ponta que espelha um processo de governança "Discovery-to-Delivery", desde o mapeamento do problema (AS-IS) até a geração de um documento de governança final e pronto para a equipe de desenvolvimento.

### ✨ Funcionalidades Principais

A ferramenta é dividida em um fluxo de trabalho principal de 6 etapas e um módulo de utilidade "fast-track".

**Fluxo Principal:**

1.  **💡 1. Diagnóstico (AS-IS):**
    * Analisa material bruto (atas de reunião, anotações, e-mails) e usa a I.A. para mapear o **Processo Atual (AS-IS)** e as **Regras de Negócio**, focando 100% no problema.

2.  **🧠 2. Arquitetura (Solução):**
    * Pega o diagnóstico AS-IS e usa a I.A. para propor a **melhor arquitetura de solução unificada**, já focada no stack (Power Automate + Analysis) e com uma avaliação de **Impacto vs. Esforço** para cada fase.

3.  **✍️ 3. Design (TO-BE):**
    * Recebe o AS-IS (para contexto) e a Arquitetura da Solução escolhida. A I.A. então gera o **PDD (Process Design Document)** detalhado, com o fluxo "To-Be" passo a passo e um plano robusto de tratamento de exceções.

4.  **📄 4. Delivery (Docs):**
    * Traduz o PDD em um **backlog de desenvolvimento Ágil completo**: Épico, Requisitos Funcionais, Requisitos Não Funcionais (NFRs), Histórias de Usuário e Critérios de Aceitação detalhados.

5.  **🧪 5. QA & Testes:**
    * Usa o mesmo PDD para gerar um **Plano de Testes (UAT)** profissional, cobrindo cenários de Caminho Feliz, Testes Negativos (dados inválidos) e Testes de Exceção (falhas de sistema).

6.  **📜 6. Governança (Final):**
    * O módulo final. O usuário cola os outputs dos Módulos 1, 3, 4 e 5. A I.A. então compila tudo em um **Documento de Governança Discovery-to-Delivery** único, padronizado e profissional, escrevendo automaticamente a "Declaração do Problema" com base nos inputs.

**Módulo de Utilidade (Adaptação):**

* **🔄 7. Refinar:**
    * Um fluxo "fast-track" para adaptar um projeto existente. O usuário cola um PDD antigo e as novas regras de negócio (ex: novo fornecedor, novo sistema), e a I.A. gera uma **"Análise de Impacto"** detalhada das mudanças necessárias.

### 🛠️ Tecnologias Utilizadas

* **Front-End:** Streamlit
* **Back-End / I.A.:** Python, Google Generative AI (Gemini)

### 🚀 Como Executar o Projeto Localmente

Para rodar este projeto no seu computador, siga os passos abaixo:

**1. Clone o Repositório:**
```bash
git clone [https://github.com/raphaelsalgueiro/Automation-Architect-AI.git](https://github.com/raphaelsalgueiro/Automation-Architect-AI.git)
cd Automation-Architect-AI
```

**2. Crie e Ative um Ambiente Virtual (Recomendado):**
```bash
python -m venv .venv
# No Windows:
.\.venv\Scripts\activate
# No macOS/Linux:
# source .venv/bin/activate
```

**3. Instale as Dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure a Chave de API:**
* Crie uma pasta chamada `.streamlit` na raiz do projeto.
* Dentro dela, crie um arquivo chamado `secrets.toml`.
* Adicione sua chave do Google AI neste arquivo, da seguinte forma:
    ```toml
    GOOGLE_API_KEY = "SUA_CHAVE_DE_API_VAI_AQUI"
    ```

**5. Execute o Aplicativo:**
```bash
streamlit run app.py
```
