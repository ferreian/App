import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Esquema de cores para genótipos
line_colors = {
    # Seu dicionário completo de mapeamento de cores aqui...
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
    # Adicione todas as outras linhas e suas cores...
}

# Cabeçalho e descrição na página principal
st.title("Análise Genótipos")

if 'uploaded_dataframe' in st.session_state:
    df = st.session_state['uploaded_dataframe']
    st.info(f"DataFrame carregado com sucesso. Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}")

    # Sidebar - Filtros
    genotipos = df['LINE'].unique()
    genotipos_selecionados = st.sidebar.multiselect('Selecione um ou mais Genótipos:', genotipos, key='genotipos_select')

    # Adicionando filtros de RM e POP ao sidebar
    rm_options = ["Todos", "RM até 74", "RM de 75 a 80", "RM maiores que 81"]
    rm_group = st.sidebar.radio('Selecione o grupo de RM:', rm_options, key='rm_select')

    
    # Aplica os filtros de RM e POP
    if rm_group == "Todos":
        filtered_df = df
    elif rm_group == "RM até 74":
        filtered_df = df[df['RM'] <= 74]
    elif rm_group == "RM de 75 a 80":
        filtered_df = df[(df['RM'] >= 75) & (df['RM'] <= 80)]
    elif rm_group == "RM maiores que 81":
        filtered_df = df[df['RM'] > 81]

    
    # Criação das abas
    tab1, tab2 = st.tabs(["Correlação", "Outra Análise"])

    with tab1:
        st.subheader("Correlação Rendimento x População")

        if genotipos_selecionados:
            # Inicializa um gráfico vazio
            fig = go.Figure()

            for genotipo in genotipos_selecionados:
                # Aqui, filtramos o DataFrame já filtrado pelos critérios RM e POP
                df_genotipo_filtrado = filtered_df[filtered_df['LINE'] == genotipo]

                # Garantimos que os dados necessários estão presentes
                if len(df_genotipo_filtrado) > 1 and 'NP' in df_genotipo_filtrado.columns and 'PROD_sc_ha_corr' in df_genotipo_filtrado.columns:
                    # Limpa dados para garantir que não haja NaN ou infinitos
                    df_genotipo_filtrado = df_genotipo_filtrado.dropna(subset=['NP', 'PROD_sc_ha_corr'])
                    df_genotipo_filtrado = df_genotipo_filtrado[np.isfinite(df_genotipo_filtrado['NP']) & np.isfinite(df_genotipo_filtrado['PROD_sc_ha_corr'])]

                    # Calcula a regressão linear
                    slope, intercept, r_value, p_value, std_err = stats.linregress(df_genotipo_filtrado['NP'], df_genotipo_filtrado['PROD_sc_ha_corr'])
                    
                    # Adiciona os pontos de dispersão
                    fig.add_trace(go.Scatter(x=df_genotipo_filtrado['NP'], y=df_genotipo_filtrado['PROD_sc_ha_corr'], mode='markers', name=genotipo,
                                            marker=dict(color=line_colors.get(genotipo, "black"))))
                    
                    # Calcula os valores y da linha de tendência
                    line_y = slope * df_genotipo_filtrado['NP'] + intercept
                    
                    # Adiciona a linha de tendência ao gráfico
                    fig.add_trace(go.Scatter(x=df_genotipo_filtrado['NP'], y=line_y, mode='lines', name=f"Tendência {genotipo}",
                                            line=dict(color=line_colors.get(genotipo, "black"))))

            # Configura o layout do gráfico
            fig.update_layout(title='Relação entre Rendimento e Número de Plantas por Genótipo',
                            xaxis_title='Número de Plantas',
                            yaxis_title='Rendimento por Hectare Corrigido')

            # Exibe o gráfico no Streamlit
            st.plotly_chart(fig)

        else:
            st.warning("Por favor, selecione pelo menos um genótipo.")
with tab2:
    st.subheader("Gráfico de Densidade")

    