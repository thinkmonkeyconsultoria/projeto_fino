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
  file_path = "/content/projeto_fino/bases/inf_diario_fi_202501.csv"

  base = pd.read_csv(file_path,delimiter=";")

  return base

df = carregar_csv()

# Filters
st.sidebar.header("Filters")
selected_funds = st.sidebar.multiselect("Select Fund Classes", df['TP_FUNDO_CLASSE'].unique(), default=df['TP_FUNDO_CLASSE'].unique())
date_range = st.sidebar.date_input("Select Date Range", [df['DT_COMPTC'].min(), df['DT_COMPTC'].max()])

# Apply Filters
filtered_df = df[(df['TP_FUNDO_CLASSE'].isin(selected_funds)) & 
                 (df['DT_COMPTC'] >= pd.to_datetime(date_range[0])) &
                 (df['DT_COMPTC'] <= pd.to_datetime(date_range[1]))]

# Summary Metrics
st.header("Summary Metrics")
st.metric("Total Patrimony", f"R$ {filtered_df['VL_PATRIM_LIQ'].sum():,.2f}")
st.metric("Total Capture", f"R$ {filtered_df['CAPTC_DIA'].sum():,.2f}")
st.metric("Total Redemption", f"R$ {filtered_df['RESG_DIA'].sum():,.2f}")

# Plot 1: Patrimony Over Time
st.header("Patrimony Over Time")
fig1 = px.line(filtered_df, x="DT_COMPTC", y="VL_PATRIM_LIQ", color="TP_FUNDO_CLASSE", title="Patrimony Over Time")
st.plotly_chart(fig1)

# Plot 2: Daily Capture vs Redemption
st.header("Daily Capture vs Redemption")
fig2 = px.bar(filtered_df, x="DT_COMPTC", y=["CAPTC_DIA", "RESG_DIA"], 
              color_discrete_map={"CAPTC_DIA": "green", "RESG_DIA": "red"},
              barmode="group", title="Daily Capture vs Redemption")
st.plotly_chart(fig2)

# Plot 3: Total Quota by Fund Class
st.header("Total Quota by Fund Class")
fig3 = px.pie(filtered_df, values="VL_TOTAL", names="TP_FUNDO_CLASSE", title="Total Quota by Fund Class")
st.plotly_chart(fig3)

# Display Filtered DataFrame
st.header("Filtered Data")
st.dataframe(filtered_df, hide_index=True)
