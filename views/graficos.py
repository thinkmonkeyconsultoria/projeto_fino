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

  base = pd.read_csv(file_path)

  return base

df = carregar_csv()

df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])  # Converter datas para formato datetime

# Título da Aplicação
st.title("Dashboard de Fundos de Investimento")

with graph_1:
  selected_funds = st.selectbox("Selecione o fundo",
                                      df['nome_do_fundo'].unique())

  # Aplicar Filtros
  filtered_df = df.loc[(df['nome_do_fundo'] == selected_funds)]

  filtered_df = filtered_df.drop_duplicates(subset='DT_COMPTC')
  # Group by DT_COMPTC and sum VL_QUOTA
  grouped_df = filtered_df.groupby('DT_COMPTC', as_index=False)['VL_QUOTA'].sum()

  graph_1, graph_2 = st.columns(2)
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

with graph_1:

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
    "Select Funds",
    options=df['nome_do_fundo'].unique(),
    default=df['nome_do_fundo'].unique()
)

  # Filter DataFrame based on selection
  filtered_df = df[df['nome_do_fundo'].isin(selected_funds)]

  # Prepare data for candlestick graph
  if not filtered_df.empty:
      fig = go.Figure()

      for fund in selected_funds:
          fund_data = filtered_df[filtered_df['nome_do_fundo'] == fund]

          # Create candlestick for each fund
          fig.add_trace(
              go.Candlestick(
                  x=fund_data['DT_COMPTC'],
                  open=fund_data['VL_QUOTA'],  # Example: Use VL_QUOTA for all candlestick properties
                  high=fund_data['VL_QUOTA'] + 0.5,  # Mock high value
                  low=fund_data['VL_QUOTA'] - 0.5,  # Mock low value
                  close=fund_data['VL_QUOTA'],  # Example close value
                  name=fund
              )
          )

      # Update layout
      fig.update_layout(
          title="Candlestick Graph by Fund",
          xaxis_title="Date",
          yaxis_title="Quota Value",
          xaxis_rangeslider_visible=False
      )

      # Display the chart
      st.plotly_chart(fig)
  else:
      st.warning("No data available for the selected funds.")
