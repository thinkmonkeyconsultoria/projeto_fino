import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Streamlit Page Config
st.set_page_config(page_title="Exemplo de Gráficos", page_icon="💰", layout="wide")

@st.cache_data
def carregar_csv():

  # Carregar excel
  file_path = "bases/fundos_sample.csv"

  base = pd.read_csv(file_path,delimiter=";")

  return base

df = carregar_csv()

df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])  # Converter datas para formato datetime

# Título da Aplicação
st.title("Dashboard de Fundos de Investimento")

# Filtros na página
st.subheader("Filtros")

selected_funds = st.selectbox("Selecione o fundo",
                                    df['nome_do_fundo'].unique())

# Aplicar Filtros
filtered_df = df.loc[(df['nome_do_fundo'] == selected_funds)]

# Gráfico 1: Patrimônio ao longo do tempo
st.header("Patrimônio ao Longo do Tempo")
fig1 = px.line(filtered_df, x="DT_COMPTC", y="VL_PATRIM_LIQ", title="Patrimônio ao Longo do Tempo")
st.plotly_chart(fig1)
