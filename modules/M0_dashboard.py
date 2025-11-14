import streamlit as st
from utils.sheets_handler import load_from_sheet
import pandas as pd
import altair as alt 

def run():
    st.header("📊 Dashboard de Projetos de Automação")
    st.write("Visão geral de todos os projetos registrados no Histórico.")

    try:
        records = load_from_sheet()

        if not records:
            st.info("Nenhum projeto encontrado no seu histórico. Salve um documento no Módulo 6 para começar.")
            st.stop()
        
        df = pd.DataFrame(records)

        if 'Tipo_De_Documento' not in df.columns or 'Data' not in df.columns or 'Nome_Do_Projeto' not in df.columns:
            st.error("Erro: A planilha 'Historico_Automation_AI' não contém as colunas necessárias (Tipo_De_Documento, Data, Nome_Do_Projeto).")
            st.stop()

        st.subheader("Visão Geral do Pipeline")
        
        total_projetos = len(df)
        projetos_concluidos = df[df['Tipo_De_Documento'] == 'Governança (Final)'].shape[0]
        projetos_rascunho = total_projetos - projetos_concluidos

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Projetos", total_projetos)
        col2.metric("Projetos Concluídos", projetos_concluidos)
        col3.metric("Projetos em Rascunho", projetos_rascunho)

        st.divider()

        st.subheader("Distribuição de Documentos")
        
        chart_data = df['Tipo_De_Documento'].value_counts().reset_index()
        chart_data.columns = ['Tipo_De_Documento', 'Quantidade']


        order = [
            'Diagnóstico (AS-IS)', 
            'Arquitetura (Solução)', 
            'Design (PDD)', 
            'Delivery (Artefatos)', 
            'QA (Plano de Testes)', 
            'Governança (Final)',
            'Governança (Adaptado)',
            'Refinamento (Análise de Impacto)' # Este é um tipo de documento antigo? Se não, remover.
        ]

        chart = alt.Chart(chart_data).mark_bar().encode(
    
            x=alt.X('Tipo_De_Documento', sort=order),
    
            y=alt.Y('Quantidade'),
    
            color=alt.Color('Tipo_De_Documento', legend=None), 
 
            tooltip=['Tipo_De_Documento', 'Quantidade']
        ).interactive() 

        st.altair_chart(chart, use_container_width=True)
 

        st.divider()

        st.subheader("Últimos Projetos Salvos")
        
        try:
            df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S')
            df_recent = df.sort_values(by='Data', ascending=False)
        except ValueError:
            df_recent = df.tail(10) 
            
        st.dataframe(
            df_recent[['Data', 'Nome_Do_Projeto', 'Tipo_De_Documento']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Data": st.column_config.DatetimeColumn(
                    "Data",
                    format="DD/MM/YYYY HH:mm:ss",
                )
            }
        )
        
        # --- INÍCIO DA ATUALIZAÇÃO (VISUALIZADOR DE HISTÓRICO) ---
        st.divider()
        st.subheader("Consultar Histórico de Documentos")
        st.write("Selecione um projeto salvo para visualizar o conteúdo gerado.")

        # Reusa os 'records' carregados no início da página
        project_names = [
            f"{r['Nome_Do_Projeto']} ({r['Tipo_De_Documento']}) - {r['Data']}" 
            for r in reversed(records) # Inverte para mostrar os mais novos primeiro
        ]
        
        selected_project_name = st.selectbox(
            "Selecione um projeto para consultar:", 
            options=project_names,
            index=None, 
            placeholder="Selecione um projeto da lista...", 
            key="dashboard_select_project"
        )

        if selected_project_name: 
            # Encontra o registro completo
            selected_record = next(
                r for r in reversed(records) if f"{r['Nome_Do_Projeto']} ({r['Tipo_De_Documento']}) - {r['Data']}" == selected_project_name
            )
            
            content = selected_record.get('Conteudo_Gerado', 'Erro: Conteúdo não encontrado.')

            # Lógica de limpeza (igual ao M7) para mostrar apenas o documento limpo
            if "---DOCUMENTO-LIMPO---" in content:
                content = content.split("---DOCUMENTO-LIMPO---", 1)[1].strip()
            elif "---ARQUITETURA-LIMPA---" in content:
                 content = content.split("---ARQUITETURA-LIMPA---", 1)[1].strip()

            st.markdown(content)
            st.code(content, language="markdown")
        # --- FIM DA ATUALIZAÇÃO ---

    except Exception as e:
        st.error(f"Erro ao carregar o dashboard: {e}")
        st.error("Verifique se a planilha Google Sheets está acessível e se as credenciais em 'secrets.toml' estão corretas.")