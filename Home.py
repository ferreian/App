import streamlit as st
import pandas as pd


# Título da página
st.title("Bem Vindo!")

# Descrição da aplicação
st.write("""
Esta aplicação permite analisar dados relacionados aos testes de faixa realizados pelo time DTC, fornecendo uma visão geral das métricas, estatísticas descritivas e visualizações interativas.
""")

st.write("""


Nesta aplicação, você pode carregar seus dados e realizar diversas análises sobre eles. Aqui está um resumo do que você pode encontrar:

- **Visão Geral:** Veja estatísticas básicas sobre os dados carregados, como número de registros, colunas, etc.
- **Estatística Descritiva e Classificação:** Analise a estatística descritiva de suas variáveis e classifique os ambientes com base nos resultados.
- **Rendimento Relativo (%):** Visualize um heatmap mostrando o rendimento relativo por local e genótipo.
- **Ranking:** Visualize a análise conjunta do genótipos.
- **Análise HEAD TO HEAD:** Realize uma comparação direta entre dois genótipos e visualize a diferença de rendimento por local
Divirta-se explorando as funcionalidades da aplicação!
""")