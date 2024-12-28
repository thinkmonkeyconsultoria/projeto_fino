import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

st.title("Controle de Movimentação")

@st.cache_data
def carregar_dados():
  file_path = "bases/Planilha de Movimentação.xlsx"

  fundos_df = pd.read_excel(file_path, sheet_name="Fundos")
  acoes_df = pd.read_excel(file_path, sheet_name="Ações")
  renda_fixa_df = pd.read_excel(file_path, sheet_name="Renda Fixa")

  dados_dic = {
      "Fundos":fundos_df,
      "Ações":acoes_df,
      "Renda Fixa":renda_fixa_df
  }

  return dados_dic

bases = carregar_dados()

selecionar_ativo = st.pills(
    "Selecione o Ativo",
    options=["Fundos","Ações","Renda Fixa"],
    selection_mode="single",
)

base_selecionada = bases[selecionar_ativo]

if base_selecionada == "Fundos":
  coluna_de_data = "Data Operação"
else:
  coluna_de_data = "Data"

today = datetime.now()
last_week = today - timedelta(days=7)

data_seletor = st.date_input(
      "Selecione a data",
      (last_week, today),
      format="DD/MM/YYYY",
  )

start_date, end_date = data_seletor
filtered_df = base_selecionada[(base_selecionada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_selecionada[coluna_de_data] <= pd.Timestamp(end_date))]

st.dataframe(filtered_df,hide_index=True,use_container_width=True)
