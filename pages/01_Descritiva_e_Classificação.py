import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página para o modo wide
st.set_page_config(layout="wide")

# Cabeçalho e descrição na página principal
st.title("Análise Locais")

# Adicionando o uploader na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel ou CSV", type=['xlsx', 'csv'])

if 'uploaded_dataframe' not in st.session_state:
    st.session_state['uploaded_dataframe'] = None

if uploaded_file is not None:
    # Lendo o arquivo
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    
    # Salva o DataFrame na sessão, se ainda não estiver carregado
    if st.session_state['uploaded_dataframe'] is None:
        st.session_state['uploaded_dataframe'] = df

    st.markdown("---")  # Esta linha cria uma divisão horizontal

# Criação de abas
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise Detalhada", "Rendimento Relativo (%)"])

with tab1:
    st.header("Visão Geral")
    
    # Verifica se o DataFrame está definido e não vazio
    if st.session_state['uploaded_dataframe'] is not None and not st.session_state['uploaded_dataframe'].empty:
        df = st.session_state['uploaded_dataframe']

        num_macros = df['MACRO'].nunique()
        num_recs = df['REC'].nunique()
        num_micros = df['MICRO'].nunique()
        num_locais = df['LOCAL'].nunique()

        # Usando HTML para adicionar o efeito de sombra nas métricas
        metrics_html = f"""
        <style>
        .metric {{
            border-radius: 10px;
            background: #fff;
            padding: 10px 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
            width: 230px;
        }}
        </style>
        <div class="metric">
            <h4 style='text-align:center; margin:0;'>MACRO</h4>
            <p style='text-align:center; font-size:30px; margin:10px 0;'>{num_macros}</p>
        </div>
        <div class="metric">
            <h4 style='text-align:center; margin:0;'>REC</h4>
            <p style='text-align:center; font-size:30px; margin:10px 0;'>{num_recs}</p>
        </div>
        <div class="metric">
            <h4 style='text-align:center; margin:0;'>MICRO</h4>
            <p style='text-align:center; font-size:30px; margin:10px 0;'>{num_micros}</p>
        </div>
        <div class="metric">
            <h4 style='text-align:center; margin:0;'>LOCAL</h4>
            <p style='text-align:center; font-size:30px; margin:10px 0;'>{num_locais}</p>
        </div>
        """

        st.markdown(metrics_html, unsafe_allow_html=True)

        st.divider()

        # Verifica se o DataFrame está carregado na sessão e contém as colunas necessárias
        if st.session_state['uploaded_dataframe'] is not None:
            df = st.session_state['uploaded_dataframe']
            if all(col in df.columns for col in ['MACRO', 'REC', 'MICRO', 'LOCAL']):
                # Filtra o DataFrame para conter apenas as colunas especificadas
                df_filtered = df[['MACRO', 'REC', 'MICRO', 'LOCAL']]
                
                # Remove linhas duplicadas
                df_filtered_no_duplicates = df_filtered.drop_duplicates()
                
                # Define 'MACRO' como índice do DataFrame
                df_filtered_no_duplicates.set_index('MACRO', inplace=True)
                
                # Como 'MACRO' agora é o índice, o DataFrame já está ordenado por 'MACRO' após definir o índice
                # Exibe o DataFrame com 'MACRO' como índice e sem duplicatas
                st.dataframe(df_filtered_no_duplicates)
            else:
                st.warning("Algumas das colunas especificadas não estão presentes no DataFrame.")
        else:
            st.error("DataFrame não encontrado. Por favor, carregue o arquivo na página de upload.")




with tab2:
    st.header("Estatística Descritiva e Classificação")

    if st.session_state['uploaded_dataframe'] is not None:
        df = st.session_state['uploaded_dataframe']

        if not df.empty:
            # Realizar a análise descritiva da variável 'PROD_sc_ha_corr' agrupada por 'LOCAL'
            analise_descritiva = df.groupby('LOCAL')['PROD_sc_ha_corr'].describe()

            # Calcular o coeficiente de variação para cada local e adicionar como uma nova coluna
            cv = df.groupby('LOCAL')['PROD_sc_ha_corr'].std() / df.groupby('LOCAL')['PROD_sc_ha_corr'].mean() * 100
            analise_descritiva['CV (%)'] = cv

            # Adicionar uma coluna "Ambiente" com base na média
            analise_descritiva['Ambiente'] = np.where(analise_descritiva['mean'] >= 50, 'Favorável', 'Desfavorável')

            # Preparando um DataFrame com 'LOCAL', 'MACRO', 'REC', 'MICRO' para o merge
            df_merge = df[['LOCAL', 'MACRO', 'REC', 'MICRO']].drop_duplicates()

            # Merge (ou join) no analise_descritiva com df_merge baseado em 'LOCAL'
            analise_descritiva_merged = analise_descritiva.reset_index().merge(df_merge, on='LOCAL', how='left')

            # Reordenando as colunas para que 'MACRO', 'REC', 'MICRO' venham antes de 'LOCAL'
            colunas_prioritarias = ['MACRO', 'REC', 'MICRO', 'LOCAL']
            colunas_finais = colunas_prioritarias + [col for col in analise_descritiva_merged.columns if col not in colunas_prioritarias]
            analise_descritiva_reordenada = analise_descritiva_merged[colunas_finais]

            # Define 'MACRO' como índice do DataFrame
            analise_descritiva_final = analise_descritiva_reordenada.set_index('MACRO')

             # Converter colunas para números inteiros antes de aplicar a formatação
            analise_descritiva_final[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'CV (%)']] = analise_descritiva_final[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'CV (%)']].astype(int)

            # Exibir a tabela de análise descritiva com o coeficiente de variação e a classificação do ambiente
            st.dataframe(analise_descritiva_final)
        else:
            st.write("Nenhum dado disponível para análise.")

        


with tab3:
    st.header("Heatmap de Rendimento Relativo por Local e Genótipo")
    if st.session_state['uploaded_dataframe'] is not None:
        df = st.session_state['uploaded_dataframe']

        if df is not None and not df.empty:  # Verifica se o DataFrame não está vazio

            micros_disponiveis = df['MICRO'].unique()
            micros_selecionados = st.multiselect('Selecione a Micro Região', micros_disponiveis)
            
            df_filtrado = df[df['MICRO'].isin(micros_selecionados)]

            if not df_filtrado.empty:  # Verifica se há dados após a filtragem

                # Encontrar o maior valor de PROD_sc_ha_corr para cada LOCAL
                max_values_por_local = df_filtrado.groupby('LOCAL')['PROD_sc_ha_corr'].transform('max')
                
                # Calcular a porcentagem relativa para cada linha em cada local
                df_filtrado['Relative_Yield'] = (df_filtrado['PROD_sc_ha_corr'] / max_values_por_local) * 100

                # Filtro de genótipo
                genotipos_disponiveis = df['LINE'].unique()
                genotipos_selecionados = st.multiselect('Selecione o Genótipo', genotipos_disponiveis, default=genotipos_disponiveis)

                # Filtrar o DataFrame pelos genótipos selecionados
                df_filtrado_genotipo = df_filtrado[df_filtrado['LINE'].isin(genotipos_selecionados)]

                pivot_table_relative_yield = pd.pivot_table(df_filtrado_genotipo, values='Relative_Yield', index='LOCAL', columns='LINE', aggfunc='mean')

                # Criar o gráfico
                fig = px.imshow(
                    pivot_table_relative_yield,
                    labels=dict(x="Linha", y="Local", color="Rendimento Relativo (%)"),
                    x=pivot_table_relative_yield.columns,
                    y=pivot_table_relative_yield.index,
                    color_continuous_scale=[
                        (0.00, "lightcoral"),    # Menor que 50 - rosa claro
                        (0.50, "lightyellow"),    # Entre 50 e 89 - amarelo claro
                        (0.70, "green"),    # Entre 50 e 89 - verde claro
                        (1.00, "darkgreen")      # 90 ou maior - verde escuro
                    ]
                )

                # Configurações do layout
                fig.update_layout(
                    title_text='Rendimento Relativo por Local e Genótipo (%)',
                    xaxis_nticks=36,
                    coloraxis_colorbar=dict(
                        title="Rendimento Relativo (%)",
                        tickvals=[0, 25, 50, 75, 100],
                        ticktext=["0", "25", "50", "75", "100"]
                    ),
                    xaxis=dict(tickfont=dict(color='black')),  # Rótulos do eixo x em preto
                    yaxis=dict(tickfont=dict(color='black'))   # Rótulos do eixo y em preto
                )
                fig.update_xaxes(side="bottom")

                # Adicionar valores diretamente no heatmap com rótulos em preto
                for i in range(len(pivot_table_relative_yield.index)):
                    for j in range(len(pivot_table_relative_yield.columns)):
                        value = pivot_table_relative_yield.values[i, j]
                        if not np.isnan(value):  # Verificar se o valor não é NaN
                            fig.add_annotation(x=pivot_table_relative_yield.columns[j], y=pivot_table_relative_yield.index[i],
                                            text=str(int(value)) + "%",
                                            showarrow=False, font=dict(color="black", size=12))

                # Exibir o gráfico
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.warning("Não há dados disponíveis após a filtragem.")
        else:
            st.warning("O DataFrame está vazio ou não foi carregado.")




