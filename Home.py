import streamlit as st
import pandas as pd
import folium

# Título da página
st.title("Bem Vindo!")

# Descrição da aplicação
st.write("""
Esta aplicação permite analisar dados relacionados aos testes de faixa realizados pelo time DTC, fornecendo uma visão geral das métricas, estatísticas descritivas e visualizações interativas.
""")

# Adicionando um uploader na barra lateral para carregar os dados dos locais
with st.sidebar:
    st.header('Carregar Dados')
    uploaded_file = st.file_uploader("Escolha um arquivo Excel ou CSV", type=["xlsx", "csv"])

# Se dados forem carregados, construir o mapa
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)  # Ler o arquivo Excel ou CSV

    # Adicionar um mapa com Folium
    st.write("## Mapa")

    # Criando um mapa com a localização inicial
    mapa = folium.Map(location=[-22.9068, -43.1729], zoom_start=12)

    # Adicionar marcadores para cada local no DataFrame
    for index, row in df.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Local']).add_to(mapa)

    # Exibir o mapa
    st.write(mapa)
