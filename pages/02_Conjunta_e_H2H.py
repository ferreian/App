import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página para o modo wide
st.set_page_config(layout="wide")

# Cabeçalho e descrição na página principal
st.title("Análise Genótipos")


# Verifica se o DataFrame foi carregado na sessão
if 'uploaded_dataframe' in st.session_state:
    df = st.session_state['uploaded_dataframe']
    # Exibe um aviso com o número de linhas e colunas
    st.info(f"DataFrame carregado com sucesso. Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}")
else:
    # Caso o DataFrame não esteja carregado, exibe um aviso
    st.warning("Nenhum DataFrame foi carregado. Por favor, carregue os dados para prosseguir com a análise.")
    # Cria um DataFrame vazio
    df = pd.DataFrame()

# Criação das abas
tab1, tab2 = st.tabs(["Ranking", "Head to Head"])

# Obter valores únicos da coluna 'MACRO' e classificá-los em ordem decrescente
macros_unique_sorted = sorted(df['MACRO'].unique(), reverse=True)

# Tab1
with st.sidebar:
    st.title('Filtros')
    
    # Multiselect para filtrar por Linhas (LINE)
    selected_lines = st.sidebar.multiselect("Filtrar por Genótipo:", options=df['LINE'].unique())

    # Filtro multisseleção para Macro
    selected_macros = st.multiselect("Filtrar por Macro Região:", options=macros_unique_sorted)

    # Filtro multisseleção para Micro
    selected_micros = st.multiselect("Filtrar por Micro Região:", options=df['MICRO'].unique())
    
    # Filtro de botão de rádio para RM
    rm_filter_options = ["Todos", "RM até 74", "RM de 75 a 80", "RM maiores que 81"]
    rm_group = st.radio("Filtrar por RM:", options=rm_filter_options)

    # Filtro de botão de rádio para POP
    pop_filter_options = ["Todos", "POP [ - ]", "POP [ + ]"]
    pop_filter = st.radio("Filtrar por POP:", options=pop_filter_options)

    # Adicionando o filtro de botão de rádio para Ambiente
    ambiente_filter_options = ["Todos", "Favorável", "Desfavorável"]
    ambiente_filter = st.radio("Filtrar por Ambiente:", options=ambiente_filter_options)

# Cálculo da média de PROD_sc_ha_corr por LOCAL
avg_prod_by_local = df.groupby('LOCAL')['PROD_sc_ha_corr'].mean().reset_index()
favorable_locals = avg_prod_by_local[avg_prod_by_local['PROD_sc_ha_corr'] >= 50]['LOCAL']
unfavorable_locals = avg_prod_by_local[avg_prod_by_local['PROD_sc_ha_corr'] < 50]['LOCAL']

# Filtragem dinâmica com base nas seleções do usuário
filtered_df = df.copy()

# Filtrar o DataFrame com base nas Linhas selecionadas
if selected_lines:
    filtered_df = filtered_df[filtered_df['LINE'].isin(selected_lines)]

# Filtrar o DataFrame com base nas Macros selecionadas
if selected_macros:
    filtered_df = filtered_df[filtered_df['MACRO'].isin(selected_macros)]

# Filtrar o DataFrame com base nas Micros selecionadas
if selected_micros:
    filtered_df = filtered_df[filtered_df['MICRO'].isin(selected_micros)]

# Filtrar o DataFrame com base no grupo de RM selecionado
if rm_group != "Todos":
    if rm_group == "RM até 74":
        filtered_df = filtered_df[filtered_df['RM'] <= 74]
    elif rm_group == "RM de 75 a 80":
        filtered_df = filtered_df[(filtered_df['RM'] >= 75) & (filtered_df['RM'] <= 80)]
    else:  # "RM maiores que 81"
        filtered_df = filtered_df[filtered_df['RM'] > 81]

# Filtrar o DataFrame com base no filtro POP selecionado
if pop_filter != "Todos":
    filtered_df = filtered_df[filtered_df['POP'] == (1 if pop_filter == "POP [ - ]" else 2)]

# Aplicar o filtro de Ambiente
if ambiente_filter != "Todos":
    if ambiente_filter == "Favorável":
        filtered_df = filtered_df[filtered_df['LOCAL'].isin(favorable_locals)]
    elif ambiente_filter == "Desfavorável":
        filtered_df = filtered_df[filtered_df['LOCAL'].isin(unfavorable_locals)]

# Adicionando a coluna 'Ambiente' ao filtered_df
filtered_df['Ambiente'] = np.where(filtered_df['LOCAL'].isin(favorable_locals), "Favorável", "Desfavorável")

# Tab1
with tab1:
    st.header("Visão Geral")
    st.write("Ranking de Rendimento")

    if not filtered_df.empty:
        # Calcula a média de PROD_sc_ha_corr para cada LINE no DataFrame filtrado
        avg_prod_by_line = filtered_df.groupby('LINE')['PROD_sc_ha_corr'].mean().reset_index()
        
        # Ordena o DataFrame pela coluna PROD_sc_ha_corr em ordem decrescente
        avg_prod_by_line_sorted = avg_prod_by_line.sort_values('PROD_sc_ha_corr', ascending=False)

        # Calcula a média geral de produção no DataFrame filtrado
        overall_avg_prod = filtered_df['PROD_sc_ha_corr'].mean()


        # Mapeia as linhas para suas respectivas cores
        line_colors = {
            "73i75": "red",
            "20NCE10008-F-306606-5": "purple",
            "20NKE10024-F-302332-8": "purple",
            "20NKE10182-F-308227-3": "purple",
            "TORMENTA": "red",
            "19NAM15685-F-317265-5": "purple",
            "19NAM15705-F-318697-1": "purple",
            "20NKE10105-F-304478-4": "purple",
            "76EA72": "green",
            "19NAM15705-F-318697-2": "purple",
            "20NKE10182-F-308219": "purple",
            "20NKE10139-F-310518-1": "purple",
            "77EA40": "green",
            "20NKE10139-F-307951-4": "purple",
            "18NA410052-F-215639-01-3": "purple",
            "20NKE10182-F-308268-2": "purple",
            "78KA42": "purple",
            "20NKE10182-F-308282": "purple",
            "79KA72": "purple",
            "19NAM15657-F-315360-6": "purple",
            "NEO 790": "red",
            "80KA72": "purple",
            "BÔNUS": "red",
            "OLIMPO": "red",
            "20NKE10139-F-307951-5": "purple",
            "20NKE10139-F-310552-8": "purple",
            "19MAM10001-F-166999-06": "green",
            "18MAM10024-F-164747-02": "green",
            "84KA92": "purple",
            "18NY420054-F-215367-07-2": "purple",
            "ZEUS": "red",
            "18NC412028-F-216899-08": "purple",
            "19NAM15705-F-21202318-6": "purple",
            "19NAM15669-F-21201876-3": "purple",
            "DM 56I59": "red",
            "19NAM15669-F-21201876-7": "purple",
            "19NAM15635-F-21201129-4": "purple",
            "18NY420055-F-211233-10": "purple",
            "VÊNUS": "red",
            "19NAM15705-F-21202318-5": "purple",
            "18NC412028-F-216899": "purple",
            "18NY420054-F-210173-05": "purple",
            "DM 57I52": "red",
            "18NY420054-F-210173-07": "purple",
            "15MA41030-27-03": "green",
            "18NY420054-F-210177-05": "purple",
            "NEO 580": "red",
            "15MA41097-07-03": "green",
            "19NN420035-F-123829": "green",
            "18NY430049-F-121513-01": "green",
            "LANÇA": "red",
            "19NAM10012-F-21100230-1": "green",
            "18NA410037-F-130204-03": "green",
            "DM 60IX64": "red",
            "19NAM15658-F-21101712-2": "green",
            "19NAM15651-F-21101643-2": "green",
            "FIBRA": "red",
            "19NAM15649-F-21101609-6": "green",
            "18NA410034-E-053": "purple",
            "DM 66I68": "red"
        }

        
       # Contar o número de linhas únicas na coluna 'LOCAL' do dataframe
        num_linhas_dataframe = len(filtered_df['LOCAL'].unique())

        # Título do gráfico com o número de linhas
        titulo_grafico = f'Produção Média por Linha- {num_linhas_dataframe} locais - Pop: {pop_filter}'

        # Cria o gráfico de barras com cores personalizadas
        fig = px.bar(avg_prod_by_line_sorted, x='LINE', y='PROD_sc_ha_corr', 
                    title=titulo_grafico,
                    color='LINE',
                    color_discrete_map=line_colors)

        # Atualiza o layout do gráfico para remover a legenda
        fig.update_layout(showlegend=False)

        # Adiciona uma linha horizontal contínua na média geral de produção
        fig.add_hline(y=overall_avg_prod, line_dash="solid", line_color="red", 
                    annotation_text="Média Geral", annotation_position="top right")

        # Altera a cor e coloca em negrito os rótulos nos eixos x e y
        fig.update_xaxes(tickfont=dict(color='black', size=14))
        fig.update_yaxes(tickfont=dict(color='black', size=14))

        # Exibe o gráfico
        st.plotly_chart(fig)

        st.divider()
        # Calcular o coeficiente de variação agrupado pelo LOCAL
        cv_by_local = filtered_df.groupby('LOCAL')['PROD_sc_ha_corr'].apply(lambda x: np.std(x) / np.mean(x) * 100)

        # Adicionar os valores calculados como uma nova coluna ao DataFrame
        filtered_df['CV(%)'] = filtered_df['LOCAL'].map(cv_by_local)

        # Renomear a coluna 'PROD_sc_ha_corr' para 'PROD sc/ha'
        filtered_df.rename(columns={'PROD_sc_ha_corr': 'PROD sc/ha'}, inplace=True)

        # Definir as colunas a serem exibidas na tabela
        columns_to_display = ['MACRO', 'REC', 'MICRO', 'LOCAL', 'LINE', 'PROD sc/ha', 'MAT', 'U', 'NP', 'NV', 'AIV', 'ALT', 'AC', 'Ambiente', 'CV(%)']

        # Criar a tabela com as colunas especificadas
        table_to_display = filtered_df[columns_to_display].reset_index(drop=True)

        # Calcula as médias das colunas desejadas por linha (LINE)
        mean_values_by_line = filtered_df.groupby('LINE').agg({
            'PROD sc/ha': 'mean',
            'MAT': 'mean',
            'U': 'mean',
            'NP': 'mean',
            'NV': 'mean',
            'AIV': 'mean',
            'ALT': 'mean',
            'AC': 'mean',
            'CV(%)': 'mean'
        }).reset_index()

        # Renomeia as colunas para indicar que são médias
        mean_values_by_line.columns = [col + '_mean' if col != 'LINE' else col for col in mean_values_by_line.columns]

        # Definir a coluna 'LINE' como o índice
        mean_values_by_line.set_index('LINE', inplace=True)

        # Ordena o DataFrame das médias por linha
        mean_values_by_line_sorted = mean_values_by_line.sort_values('PROD sc/ha_mean', ascending=False)

        # Converter apenas as colunas numéricas para números inteiros
        numeric_columns = mean_values_by_line_sorted.select_dtypes(include=['int', 'float']).columns
        mean_values_by_line_sorted[numeric_columns] = mean_values_by_line_sorted[numeric_columns].astype(int)

        # Formatar as outras colunas para uma casa decimal
        non_numeric_columns = mean_values_by_line_sorted.select_dtypes(exclude=['int', 'float']).columns
        mean_values_by_line_sorted[non_numeric_columns] = mean_values_by_line_sorted[non_numeric_columns].round(1)

        # Exibe o DataFrame com as médias calculadas por linha, ordenado
        st.write("Tabela com dados médios")
        st.dataframe(mean_values_by_line_sorted)

        st.divider()

        # Exibir a tabela
        st.write("Tabela Completa")
        st.dataframe(table_to_display)


with tab2:
    st.header("Análise HEAD TO HEAD")
    
    if 'uploaded_dataframe' in st.session_state:
        df = st.session_state.uploaded_dataframe

        genotipos = df['LINE'].unique().tolist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            genotipo1 = st.selectbox('Selecione o Genótipo 1:', genotipos, index=0, key='genotipo1')
        
        with col2:
            genotipo2 = st.selectbox('Selecione o Genótipo 2:', genotipos, index=1, key='genotipo2')
        
        if st.button('Analisar e Visualizar'):
            # Filtrar o DataFrame com base nos genótipos selecionados
            df_filtered = df[df['LINE'].isin([genotipo1, genotipo2])]
            
            # Aplicar os filtros do sidebar ao DataFrame filtrado
            if selected_lines:
                df_filtered = df_filtered[df_filtered['LINE'].isin(selected_lines)]
            if selected_macros:
                df_filtered = df_filtered[df_filtered['MACRO'].isin(selected_macros)]
            if selected_micros:
                df_filtered = df_filtered[df_filtered['MICRO'].isin(selected_micros)]
            if rm_group != "Todos":
                if rm_group == "RM até 74":
                    df_filtered = df_filtered[df_filtered['RM'] <= 74]
                elif rm_group == "RM de 75 a 80":
                    df_filtered = df_filtered[(df_filtered['RM'] >= 75) & (df_filtered['RM'] <= 80)]
                else:  # "RM maiores que 81"
                    df_filtered = df_filtered[df_filtered['RM'] > 81]
            if pop_filter != "Todos":
                df_filtered = df_filtered[df_filtered['POP'] == (1 if pop_filter == "POP [ - ]" else 2)]
            if ambiente_filter != "Todos":
                if ambiente_filter == "Favorável":
                    df_filtered = df_filtered[df_filtered['LOCAL'].isin(favorable_locals)]
                elif ambiente_filter == "Desfavorável":
                    df_filtered = df_filtered[df_filtered['LOCAL'].isin(unfavorable_locals)]

            df_grouped = df_filtered.groupby(['LOCAL', 'LINE'])['PROD_sc_ha_corr'].mean().unstack()
            
            df_grouped['Diferenca'] = df_grouped[genotipo1] - df_grouped[genotipo2]

            vitorias_genotipo1 = (df_grouped['Diferenca'] > 3).sum()
            derrotas_genotipo1 = (df_grouped['Diferenca'] < -3).sum()
            empates = df_grouped.shape[0] - vitorias_genotipo1 - derrotas_genotipo1
            
            total_locais = df_grouped.shape[0]

            percentual_vitorias_genotipo1 = (vitorias_genotipo1 / total_locais) * 100
            percentual_empates = (empates / total_locais) * 100
            percentual_derrotas_genotipo1 = (derrotas_genotipo1 / total_locais) * 100

            # Supondo que as cores são definidas da seguinte forma:
            cor_vitoria = "lightgreen"
            cor_empate = "lightyellow"
            cor_derrota = "lightpink"

            # Função para criar um "métrica" customizado com markdown
            def metrica_customizada(titulo, valor, subtexto, cor_de_fundo):
                st.markdown(f"""
                <div style="background-color: {cor_de_fundo}; border-radius: 10px; padding: 10px; margin: 10px 0;">
                    <p style="color: #333; margin: 0;">{titulo}</p>
                    <h1 style="color: #000;">{valor}</h1>
                    <p style="color: #666; margin: 0;">{subtexto}</p>
                </div>
                """, unsafe_allow_html=True)

            # Calcular o maior valor nas vitórias e o menor valor nas derrotas
            maior_valor_vitoria = df_grouped['Diferenca'].max()
            menor_valor_derrota = df_grouped['Diferenca'].min()

            # Calcular a diferença média dos valores nas vitórias e nas derrotas
            if vitorias_genotipo1 > 0:
                diferenca_media_vitoria = df_grouped[df_grouped['Diferenca'] > 3]['Diferenca'].mean()
            else:
                diferenca_media_vitoria = 0

            if derrotas_genotipo1 > 0:
                diferenca_media_derrota = df_grouped[df_grouped['Diferenca'] < -3]['Diferenca'].mean()
            else:
                diferenca_media_derrota = 0

            # Usando a função definida acima para criar métricas customizadas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                metrica_customizada("Número de Locais", total_locais, "", "#f0f2f6")  # Cor neutra;
            with col2:
                metrica_customizada(f"Vitórias - Max: {maior_valor_vitoria:.2f} sc/ha", vitorias_genotipo1, f"{percentual_vitorias_genotipo1:.2f}% - Média: {diferenca_media_vitoria:.2f} sc/ha", cor_vitoria)
            with col3:
                metrica_customizada(f"Empates", empates, f"{percentual_empates:.2f}%", cor_empate)
            with col4:
                metrica_customizada(f"Derrotas - Max: {menor_valor_derrota:.2f} sc/ha", derrotas_genotipo1, f"{percentual_derrotas_genotipo1:.2f}% - Média: {diferenca_media_derrota:.2f} sc/ha", cor_derrota)

           
            st.markdown("---")
            
            colors = ['lightgreen' if x > 3 else 'lightpink' if x < -3 else 'lightyellow' for x in df_grouped['Diferenca']]
            data_labels = [f"{x:.2f}" for x in df_grouped['Diferenca']]

            fig = go.Figure(data=[go.Bar(x=df_grouped.index, y=df_grouped['Diferenca'], marker_color=colors, text=data_labels, textposition='outside', 
                            textfont=dict(color='black', size=12, family='Arial, sans-serif'),
                             )])
            
            fig.update_layout(
                title=f"Diferença de Rendimento entre HEAD: {genotipo1} e CHECK: {genotipo2} por Local",
                xaxis_title=None,
                yaxis_title=None,
                xaxis=dict(showticklabels=True, tickfont=dict(color='black', size=12, family='Arial, sans-serif')),
                yaxis=dict(showticklabels=True, tickfont=dict(color='black', size=12, family='Arial, sans-serif')),
                autosize=True,
                margin=dict(l=40, r=40, t=40, b=30)
            )
                
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcular a média de MAT, U, NP, NV, AIV, ALT e AC para cada LINE
            media_caracteristicas_por_line = df_filtered.groupby('LINE').agg({
                'MAT': 'mean',
                'U': 'mean',
                'NP': 'mean',
                'NV': 'mean',
                'AIV': 'mean',
                'ALT': 'mean',
                'AC': 'mean'
            }).reset_index()

            # Calcular a média de MAT, U, NP, NV, AIV, ALT e AC para cada LINE
            media_caracteristicas_por_line = df_filtered.groupby('LINE').agg({
                'MAT': 'mean',
                'U': 'mean',
                'NP': 'mean',
                'NV': 'mean',
                'AIV': 'mean',
                'ALT': 'mean',
                'AC': 'mean'
            }).reset_index()

            # Pivotar a tabela para ter os genótipos como colunas
            media_caracteristicas_pivot = media_caracteristicas_por_line.set_index('LINE').transpose()

            # Formatar os valores para números inteiros
            media_caracteristicas_pivot_int = media_caracteristicas_pivot.astype(int)

             #Criar as três colunas
            col1, col2, col3 = st.columns([1, 3, 1])

            # Centralizar a tabela
            media_caracteristicas_pivot_styled = media_caracteristicas_pivot_int.style.set_properties(**{'text-align': 'center'})

            # Exibir a tabela formatada e centralizada na coluna do meio
            with col2:
                st.write("Médias de Características por Genótipo:")
                st.dataframe(media_caracteristicas_pivot_styled)