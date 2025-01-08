import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

header_1, header_2 = st.columns([1,3])

with header_1:

  st.image("Imagens/logo.png")

with header_2:

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
seletor_1,seletor_2,seletor_3 = st.columns(3)

with seletor_1:
  selecionar_ativo = st.pills(
      "Selecione o Ativo",
      options=["Fundos","Ações","Renda Fixa"],
      selection_mode="single",
      default="Fundos"
  )

base_selecionada = bases[selecionar_ativo]

if selecionar_ativo == "Fundos":
  coluna_de_data = "Data Operação"
else:
  coluna_de_data = "Data"

with seletor_2:

  today = datetime.now()
  last_month = today - timedelta(days=30)

  data_seletor = st.date_input(
        "Selecione a data",
        (last_month, today),
        format="DD/MM/YYYY",
    )
if len(data_seletor) == 0:
  filtered_df = base_selecionada
else:
  if len(data_seletor) > 1:
    start_date, end_date = data_seletor
  else:
    start_date = data_seletor[0]
    end_date = start_date

  filtered_df = base_selecionada.loc[(base_selecionada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_selecionada[coluna_de_data] <= pd.Timestamp(end_date))]

with seletor_3:

  carteiras = sorted(filtered_df["Carteira"].unique())

  selecionar_carteira = st.selectbox("Selecione a carteira",carteiras)
  filtered_df = filtered_df.loc[filtered_df["Carteira"] == selecionar_carteira]


st.dataframe(filtered_df,hide_index=True,use_container_width=True,
    column_config={
        "Financeiro": st.column_config.NumberColumn(
            "Financeiro (R$)"
            format="R$%d",
        )
    })
