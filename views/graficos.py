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
  file_path = "bases/inf_diario_fi_202501.csv"

  base = pd.read_csv(file_path,delimiter=";")

  return base

df = carregar_csv()

df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'])  # Converter datas para formato datetime

# Título da Aplicação
st.title("Dashboard de Fundos de Investimento")

# Filtros na página
st.subheader("Filtros")
col1, col2 = st.columns(2)

with col1:
    selected_funds = st.multiselect("Selecione Classes de Fundos", 
                                    df['TP_FUNDO_CLASSE'].unique(), 
                                    default=df['TP_FUNDO_CLASSE'].unique())

with col2:
    date_range = st.date_input("Selecione o Intervalo de Datas", 
                               [df['DT_COMPTC'].min(), df['DT_COMPTC'].max()])

# Aplicar Filtros
filtered_df = df[(df['TP_FUNDO_CLASSE'].isin(selected_funds)) & 
                 (df['DT_COMPTC'] >= pd.to_datetime(date_range[0])) &
                 (df['DT_COMPTC'] <= pd.to_datetime(date_range[1]))]

# Métricas Resumidas
st.header("Métricas Resumidas")
col1, col2, col3 = st.columns(3)
col1.metric("Patrimônio Total", f"R$ {filtered_df['VL_PATRIM_LIQ'].sum():,.2f}")
col2.metric("Captação Total", f"R$ {filtered_df['CAPTC_DIA'].sum():,.2f}")
col3.metric("Resgate Total", f"R$ {filtered_df['RESG_DIA'].sum():,.2f}")

# Gráfico 1: Patrimônio ao longo do tempo
st.header("Patrimônio ao Longo do Tempo")
fig1 = px.line(filtered_df, x="DT_COMPTC", y="VL_PATRIM_LIQ", color="TP_FUNDO_CLASSE", title="Patrimônio ao Longo do Tempo")
st.plotly_chart(fig1)

# Gráfico 2: Captação vs Resgate Diário
st.header("Captação vs Resgate Diário")
fig2 = px.bar(filtered_df, x="DT_COMPTC", y=["CAPTC_DIA", "RESG_DIA"], 
              color_discrete_map={"CAPTC_DIA": "green", "RESG_DIA": "red"},
              barmode="group", title="Captação vs Resgate Diário")
st.plotly_chart(fig2)

# Gráfico 3: Quota Total por Classe de Fundo
st.header("Quota Total por Classe de Fundo")
fig3 = px.pie(filtered_df, values="VL_TOTAL", names="TP_FUNDO_CLASSE", title="Quota Total por Classe de Fundo")
st.plotly_chart(fig3)

# Exibir DataFrame Filtrado
st.header("Dados Filtrados")
st.dataframe(filtered_df, hide_index=True)
