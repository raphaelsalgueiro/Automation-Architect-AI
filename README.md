# 🤖 Automation Architect AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automation-architect-ai-emhu7fwq2hpyzs447qkep5.streamlit.app/)

Uma ferramenta de I.A. construída com Python e Streamlit para atuar como um co-piloto para Gestores de Projetos, Analistas de Requisitos e Consultores de Automação.

### 🎯 Sobre o Projeto

O **Automation Architect AI** resolve um desafio central no desenvolvimento de projetos de automação e I.A.: a tradução de necessidades de negócio em artefatos técnicos claros e acionáveis. O objetivo é acelerar o ciclo de vida do projeto, desde a identificação de oportunidades até a criação de um backlog pronto para a equipe de desenvolvimento.

### ✨ Funcionalidades Principais

A ferramenta guia o usuário através de um fluxo de trabalho de 4 etapas:

1.  **💡 Discovery:** Analisa descrições de processos de negócio e identifica oportunidades de automação (RPA) e I.A. (Machine Learning).
2.  **✍️ Design:** Transforma uma oportunidade em um blueprint técnico detalhado (esboço de PDD), descrevendo o fluxo do processo "To-Be".
3.  **📄 Delivery:** Gera automaticamente os artefatos para a equipe de desenvolvimento Ágil: Épico, User Stories, Requisitos Não Funcionais (NFRs) e Critérios de Aceitação.
4.  **🧪 QA & Testes:** Com base no mesmo blueprint, gera um plano de testes abrangente com cenários de caminho feliz, testes negativos e de exceção.

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

**2. Instale as Dependências:**
```bash
pip install -r requirements.txt
```

**3. Configure a Chave de API:**
* Crie uma pasta chamada `.streamlit` na raiz do projeto.
* Dentro dela, crie um arquivo chamado `secrets.toml`.
* Adicione sua chave do Google AI neste arquivo, da seguinte forma:
    ```toml
    GOOGLE_API_KEY = "SUA_CHAVE_DE_API_VAI_AQUI"
    ```

**4. Execute o Aplicativo:**
```bash
streamlit run app.py
```
