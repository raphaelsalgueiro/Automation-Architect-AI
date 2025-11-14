# 🤖 Automation Architect AI (v7.1)

> Um co-piloto de I.A. para Gestores de Projeto de TI, focado em acelerar o fluxo de trabalho de documentação de "Discovery" até o "Delivery".

Este projeto, desenvolvido em Python e Streamlit, atua como uma ferramenta interna para a equipe de TI, automatizando a criação de toda a documentação de governança de projetos. A ferramenta é especializada em gerar soluções focadas na stack de **Power Automate (Cloud e Desktop)** e na ferramenta interna de IA, **"Analysis"**.

---

## 🏛️ Arquitetura Principal

A ferramenta é construída sobre dois conceitos-chave:

1.  **"Memória Dupla":**
    * **Curto Prazo (Clipboard):** Um dicionário Python (`st.session_state.clipboard`) que passa automaticamente os dados gerados entre os módulos (ex: o Diagnóstico do M1 é usado pelo M2, que gera a Arquitetura usada pelo M3).
    * **Longo Prazo (Histórico):** Uma planilha Google Sheets atua como nosso banco de dados permanente, salvando todos os artefatos e permitindo a reutilização inteligente de projetos.

2.  **"Arquitetura Flexível":**
    * O usuário não é forçado a um fluxo linear. Ele pode pular diretamente para qualquer módulo (ex: Módulo 3), colar seu próprio texto (`st.text_area`) e a ferramenta funcionará a partir daquele ponto.

## ✨ Funcionalidades (Módulos)

A aplicação é dividida em 8 abas principais:

* **📊 Módulo 0: Dashboard**
    * A página inicial. Lê o histórico do Google Sheets e exibe KPIs (Total de Projetos, Concluídos) usando `st.metric` e um gráfico de barras (`altair`) com a distribuição de documentos.

* **💡 Módulo 1: Diagnóstico (AS-IS)**
    * Recebe o "material bruto" do cliente através de um `st.text_area` (para anotações) ou `st.file_uploader` (para .pdf, .docx, .txt).
    * Usa a IA para gerar o "Mapeamento AS-IS" e as "Regras de Negócio" (Seção 2 do documento final).

* **🧠 Módulo 2: Arquitetura (Solução)**
    * O "cérebro" da aplicação. Ao receber o AS-IS, ele primeiro lê o histórico do Google Sheets.
    * A IA decide entre `[REUTILIZAR]` (se encontrar um projeto similar) ou `[NOVO]`.
    * Se `[REUTILIZAR]`, gera uma Análise de Impacto (para o usuário) e uma Arquitetura Limpa (para o clipboard), separando o contexto da solução final.
    * Se `[NOVO]`, gera uma arquitetura do zero, dividindo tarefas entre "Analysis" e "Power Automate".

* **✍️ Módulo 3: Design (TO-BE)**
    * Recebe a "Arquitetura Limpa" do M2 e a detalha em um PDD (Process Design Document) completo, focado em texto, com o fluxo TO-BE e as responsabilidades (Seções 3.1 e 3.2 do documento final).

* **📄 Módulo 4: Delivery (Docs)**
    * Traduz o PDD do M3 em todos os 5 artefatos técnicos, formatados em **Tabelas Markdown** para clareza: Épico, Requisitos Funcionais (RFs), Requisitos Não Funcionais (NFRs), Histórias de Usuário (USs) e Critérios de Aceitação (CAs) (Seções 3.3 a 3.7).

* **🧪 Módulo 5: QA & Testes**
    * Lê o PDD e gera um Plano de Testes (UAT) completo, dividido em Happy Path, Testes Negativos e Testes de Exceção, formatados em **Tabelas Markdown** (Seção 4).

* **📜 Módulo 6: Governança (Final)**
    * O "Redator Inteligente". Este módulo recebe os outputs limpos de todos os módulos anteriores (M1, M3, M4, M5).
    * Ele usa um "esqueleto fixo" baseado no template padrão (OUROMAR) e **escreve** o documento de governança final e profissional, encaixando o contexto nas seções corretas.
    * Permite a exportação do documento final para PDF usando `fpdf2`.

* **🔄 Módulo 7: Refinar**
    * Um fluxo "fast-track" que permite ao usuário carregar qualquer projeto do histórico, descrever as mudanças, e gerar um novo documento de governança adaptado.

---

## 🛠️ Stack Tecnológica

O projeto utiliza as seguintes bibliotecas (conforme `requirements.txt`):

* **Front-End:** `streamlit`
* **IA Generativa:** `google-generativeai`
* **Base de Dados:** `gspread` (para Google Sheets)
* **Gráficos:** `altair`
* **Leitura de Arquivos:** `pdfplumber`, `python-docx`
* **Exportação de PDF:** `fpdf2`
* **Utilitários:** `markdown2`