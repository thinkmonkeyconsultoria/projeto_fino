import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Streamlit Page Config
st.set_page_config(page_title="Exemplo de Gráficos", page_icon="💰", layout="wide")

@st.cache_data
def carregar_csv():

  # Carregar excel
  file_path = "bases/fundos_sample.csv"

  base = pd.read_csv(file_path)

  return base

df = carregar_csv()

df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])  # Converter datas para formato datetime

# Título da Aplicação
st.title("Dashboard de Fundos de Investimento")

graph_1,graph_2 = st.columns(2)

with graph_1:
  selected_funds = st.selectbox("Selecione o fundo",
                                      df['nome_do_fundo'].unique())

  # Aplicar Filtros
  filtered_df = df.loc[(df['nome_do_fundo'] == selected_funds)]

  filtered_df = filtered_df.drop_duplicates(subset='DT_COMPTC')
  # Group by DT_COMPTC and sum VL_QUOTA
  grouped_df = filtered_df.groupby('DT_COMPTC', as_index=False)['VL_QUOTA'].sum()

  # Plotly Express Line Chart
  fig = px.line(
      grouped_df,
      x="DT_COMPTC",
      y="VL_QUOTA",
      title="VL_QUOTA por Data",
      labels={"DT_COMPTC": "Data", "VL_QUOTA": "Quota"}
  )

  # Display the chart in Streamlit
  st.plotly_chart(fig)

with graph_2:

  selected_funds = st.multiselect(
    "Selecione fundos",
    options=df['nome_do_fundo'].unique(),
    default=df['nome_do_fundo'].unique()[:5]
  )

  filtered_df = df[df['nome_do_fundo'].isin(selected_funds)]

  if not filtered_df.empty:
      # Group by 'nome_do_fundo' and sum 'VL_QUOTA'
      grouped_df = filtered_df.groupby('nome_do_fundo', as_index=False)['VL_QUOTA'].sum()

      # Create a bar graph using Plotly Express
      fig = px.bar(
          grouped_df,
          x='nome_do_fundo',
          y='VL_QUOTA',
          title="Total VL_QUOTA por fundo",
          labels={"nome_do_fundo": "Nome Fundo", "VL_QUOTA": "Total Quota"},
          height=600
      )

      # Display the bar graph
      st.plotly_chart(fig)

  else:
    st.warning("Selecione um fundo")
