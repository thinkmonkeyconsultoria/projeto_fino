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

if selecionar_ativo == "Fundos":
  coluna_de_data = "Data Operação"
else:
  coluna_de_data = "Data"

seletor_1,seletor_2 = st.columns(2)

with seletor_1:

  today = datetime.now()
  last_week = today - timedelta(days=7)

  data_seletor = st.date_input(
        "Selecione a data",
        (last_week, today),
        format="DD/MM/YYYY",
    )

if data_seletor[1]:
  start_date, end_date = data_seletor
else:
  start_date = data_seletor[0]
  end_date = start_date
  
filtered_df = base_selecionada[(base_selecionada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_selecionada[coluna_de_data] <= pd.Timestamp(end_date))]

with seletor_2:

  carteiras = sorted(filtered_df["Carteira"].unique())

  selecionar_carteira = st.selectbox("Selecione a carteira",carteiras)
  filtered_df = filtered_df.loc[filtered_df["Carteira"] == selecionar_carteira]


st.dataframe(filtered_df,hide_index=True,use_container_width=True)
