import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para o modo wide
st.set_page_config(layout="wide")

# Cabeçalho e descrição na página principal
st.title("Análise de Genótipos")

# Carregamento e leitura do arquivo Excel
if 'uploaded_dataframe' not in st.session_state:
    uploaded_file = st.file_uploader("Carregue seu arquivo Excel", type=['xlsx'])
    if uploaded_file is not None:
        # Carregar o DataFrame na sessão
        data = pd.read_excel(uploaded_file)
        st.session_state['uploaded_dataframe'] = data
        st.success("DataFrame carregado com sucesso!")

# Verifica se o DataFrame foi carregado na sessão
if 'uploaded_dataframe' in st.session_state:
    df = st.session_state['uploaded_dataframe']
    st.info(f"DataFrame carregado com sucesso. Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}")

    # Filtro multiselect para as linhas na sidebar
    selected_lines = st.sidebar.multiselect("Escolha as linhas (LINE):", options=df['LINE'].unique(), key='line_filter')

    # Filtro multiselect para as micro-regiões na sidebar
    selected_micro = st.sidebar.multiselect("Escolha as micro-regiões (MICRO):", options=df['MICRO'].unique(), key='micro_filter')

    # Filtra o DataFrame com base nas linhas e micro-regiões selecionadas
    df_filtered = df[df['LINE'].isin(selected_lines) & df['MICRO'].isin(selected_micro)]

    # Criação das abas
    tab1, tab2 = st.tabs(["Maturação x Rendimento", "População x Rendimento"])
    
    with tab1:
        st.header("Análise de Maturação x Rendimento")
        if not df_filtered.empty:
            fig1 = px.scatter(df_filtered, x='MAT', y='PROD_sc_ha_corr', color='LINE',
                              labels={'MAT': 'Maturidade', 'PROD_sc_ha_corr': 'Produção corrigida (sc/ha)'},
                              title="Relação entre Maturidade e Produção",
                              height=600, width=800)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.error("Não há dados para mostrar com os filtros aplicados. Por favor, ajuste sua seleção.")

    with tab2:
        st.header("Análise de População x Rendimento")
        if not df_filtered.empty:
            correlation = df_filtered['NP'].corr(df_filtered['PROD_sc_ha_corr'])
            title = f"Relação entre Número de Plantas e Produção - Correlação: {correlation:.2f}"
            fig2 = px.scatter(df_filtered, x='NP', y='PROD_sc_ha_corr', color='LINE',
                              labels={'NP': 'Número de Plantas', 'PROD_sc_ha_corr': 'Produção corrigida (sc/ha)'},
                              title=title,
                              height=600, width=800,
                              trendline="ols")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.error("Não há dados para mostrar com os filtros aplicados. Por favor, ajuste sua seleção.")
