# 🤖 Automation Architect AI

## 🎯 Sobre o Projeto

O **Automation Architect AI** é uma ferramenta de protótipo construída com Python, Streamlit e I.A. Generativa (Google Gemini), projetada para atuar como um co-piloto para Gestores de Projetos, Analistas de Requisitos e Consultores de Automação.

Esta ferramenta foi criada para resolver um desafio central no desenvolvimento de projetos de automação e I.A.: a tradução de necessidades de negócio em artefatos técnicos claros e acionáveis. O objetivo é acelerar o ciclo de vida do projeto, desde a identificação de oportunidades até a criação de um backlog pronto para a equipe de desenvolvimento, garantindo qualidade e padronização.

## ✨ Funcionalidades Principais

A ferramenta é dividida em um fluxo de trabalho de 4 etapas:

* **💡 Discovery:** Analisa descrições de processos de negócio em linguagem natural e identifica oportunidades de automação (RPA) e aplicação de I.A. (Machine Learning).
* **✍️ Design:** Transforma uma oportunidade selecionada em um blueprint técnico detalhado (esboço de PDD), descrevendo o fluxo do processo "To-Be" da automação.
* **📄 Delivery:** Pega o blueprint do design e gera automaticamente os artefatos para a equipe de desenvolvimento Ágil: Épico, User Stories, Requisitos Não Funcionais (NFRs) e Critérios de Aceitação.
* **🧪 QA & Testes:** Com base no mesmo blueprint, gera um plano de testes abrangente, com cenários de caminho feliz, testes negativos e testes de exceção para garantir a robustez da solução.

## 🛠️ Tecnologias Utilizadas

* **Front-End:** Streamlit
* **Back-End / I.A.:** Python, Google Generative AI (Gemini)

## 🚀 Como Executar o Projeto

1.  Clone este repositório.
2.  Crie um ambiente virtual e instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crie uma cópia do arquivo de configuração de ambiente e insira sua API Key do Google AI.
4.  Execute o aplicativo:
    ```bash
    streamlit run app.py
    ```
