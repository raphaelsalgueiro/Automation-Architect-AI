import streamlit as st
from utils.sheets_handler import load_from_sheet
import pandas as pd
import altair as alt # <-- Importamos o Altair

def run():
    st.header("📊 Dashboard de Projetos de Automação")
    st.write("Visão geral de todos os projetos registrados no Histórico.")

    try:
        # 1. Carregar os dados (vem como lista de dicionários)
        records = load_from_sheet()

        if not records:
            st.info("Nenhum projeto encontrado no seu histórico. Salve um documento no Módulo 6 para começar.")
            st.stop()
        
        # 2. Converter em DataFrame do Pandas para fácil análise
        df = pd.DataFrame(records)

        # 3. Garantir que as colunas esperadas existam
        if 'Tipo_De_Documento' not in df.columns or 'Data' not in df.columns or 'Nome_Do_Projeto' not in df.columns:
            st.error("Erro: A planilha 'Historico_Automation_AI' não contém as colunas necessárias (Tipo_De_Documento, Data, Nome_Do_Projeto).")
            st.stop()

        # --- Renderizar os KPIs ---
        st.subheader("Visão Geral do Pipeline")
        
        # 4. Calcular KPIs
        total_projetos = len(df)
        projetos_concluidos = df[df['Tipo_De_Documento'] == 'Governança (Final)'].shape[0]
        projetos_rascunho = total_projetos - projetos_concluidos

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Projetos", total_projetos)
        col2.metric("Projetos Concluídos", projetos_concluidos)
        col3.metric("Projetos em Rascunho", projetos_rascunho)

        st.divider()

        # --- INÍCIO DA MUDANÇA (Gráfico Altair) ---
        st.subheader("Distribuição de Documentos")
        
        # 5. Calcular dados do gráfico
        chart_data = df['Tipo_De_Documento'].value_counts().reset_index()
        chart_data.columns = ['Tipo_De_Documento', 'Quantidade']

        # 6. Definir a ordem lógica do funil (do início ao fim)
        order = [
            'Diagnóstico (AS-IS)', 
            'Arquitetura (Solução)', 
            'Design (PDD)', 
            'Delivery (Artefatos)', 
            'QA (Plano de Testes)', 
            'Governança (Final)',
            'Governança (Adaptado)',
            'Refinamento (Análise de Impacto)'
        ]

        # 7. Criar o gráfico Altair
        chart = alt.Chart(chart_data).mark_bar().encode(
            # Eixo X: Ordenado pela nossa lista 'order'
            x=alt.X('Tipo_De_Documento', sort=order),
            # Eixo Y: Quantidade
            y=alt.Y('Quantidade'),
            # Cor: Uma cor diferente para cada tipo
            color=alt.Color('Tipo_De_Documento', legend=None), # Remove a legenda de cor (redundante)
            # Tooltip: O que aparece ao passar o mouse
            tooltip=['Tipo_De_Documento', 'Quantidade']
        ).interactive() # Permite zoom e pan

        st.altair_chart(chart, use_container_width=True)
        # --- FIM DA MUDANÇA ---

        st.divider()

        # --- Renderizar a Tabela de Projetos Recentes ---
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
            # Configuração para formatar a data de volta para o padrão Brasil
            column_config={
                "Data": st.column_config.DatetimeColumn(
                    "Data",
                    format="DD/MM/YYYY HH:mm:ss",
                )
            }
        )

    except Exception as e:
        st.error(f"Erro ao carregar o dashboard: {e}")
        st.error("Verifique se a planilha Google Sheets está acessível e se as credenciais em 'secrets.toml' estão corretas.")