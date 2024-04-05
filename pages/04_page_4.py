import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
import io

# Configuração da página para o modo wide
st.set_page_config(layout="wide")

# Cabeçalho e descrição na página principal
st.title("Análise Genótipos")

# Seção para baixar o modelo de organização de dados
st.subheader("Baixar Modelo de Organização de Dados")
st.write("Baixe o modelo de arquivo CSV abaixo para organizar seus dados para análise. Este modelo contém as colunas recomendadas para o carregamento de dados.")

# Modelo DataFrame com as três colunas especificadas
modelo_df = pd.DataFrame({
    'Local': [],
    'Tratamento': [],
    'Variavel': []
})
csv_modelo = modelo_df.to_csv(index=False)

st.download_button(
    label="Baixar Modelo CSV",
    data=csv_modelo,
    file_name='modelo_organizacao_dados.csv',
    mime='text/csv',
)

# Verifica se o DataFrame foi carregado na sessão
if 'uploaded_dataframe' in st.session_state:
    df = st.session_state['uploaded_dataframe']
    # Exibe um aviso com o número de linhas e colunas
    st.info(f"DataFrame carregado com sucesso. Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}")

    # Criação das abas
    tab1, tab2 = st.tabs(["Seleção e Exportação", "Análise de Dados"])

    with tab1:
        # Define as colunas que queremos pré-selecionar para exportação
        colunas_pre_selecionadas = [
            "ID_LOCAL", "LOCAL", "TRAT", "LINE", "POP", "PROD_sc_ha_corr", "NP", "NG", "De", "NV", "AC", "MAT", "AIV",
            "ALT", "MP", "O", "MAL", "ANT", "MOR", "MAP", "CER", "ANO", "DFC"
        ]
        
        # Filtra apenas as colunas pré-selecionadas que existem no DataFrame
        colunas_validas = [col for col in colunas_pre_selecionadas if col in df.columns]

        # Permita que o usuário selecione as colunas para exportação, com algumas já pré-selecionadas
        colunas_selecionadas = st.multiselect('Selecione as colunas para exportar:', df.columns, default=colunas_validas)

        # Cria um novo DataFrame com as colunas selecionadas
        df_exportar = df[colunas_selecionadas] if colunas_selecionadas else pd.DataFrame()

        if not df_exportar.empty:
            # Converta o DataFrame selecionado para CSV
            csv = df_exportar.to_csv(index=False)

            # Crie um botão para baixar o CSV
            st.download_button(
                label="Baixar dados selecionados como CSV",
                data=csv,
                file_name='dados_selecionados.csv',
                mime='text/csv',
            )
        else:
            st.error("Por favor, selecione pelo menos uma coluna para exportar.")

    with tab2:
        # Adicione aqui o conteúdo da segunda aba referente à "Análise de Dados"
        st.write("Análise de dados será adicionada aqui.")

else:
    # Caso o DataFrame não esteja carregado, exibe um aviso
    st.warning("Nenhum DataFrame foi carregado. Por favor, carregue os dados para prosseguir com a análise.")
    # Cria um DataFrame vazio
    df = pd.DataFrame()

with tab2:
    st.header('Subir arquivo do R')
    
    uploaded_csv_file = st.file_uploader("Faça upload do seu arquivo CSV", type=['csv'])
    
    if uploaded_csv_file is not None:
        # Ler o arquivo CSV
        content = uploaded_csv_file.read().decode("utf-8")
        
        # Criar um DataFrame
        df_r = pd.read_csv(io.StringIO(content), index_col=0)
        
        # Criar o gráfico de barras
        fig = px.bar(df_r, x='treatment', y='adjusted.mean', text='scott_knott', color='scott_knott', title='Agrupamento de Médias - ',
                     labels={'treatment': 'Tratamento', 'adjusted.mean': 'Média Ajustada', 'scott_knott': 'Rótulo dos Dados'})
        
        # Adicionar título e rótulos dos eixos
        fig.update_layout(xaxis_title='Tratamento', yaxis_title='Média Ajustada')
        
        # Exibir o gráfico
        st.plotly_chart(fig)