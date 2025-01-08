import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Streamlit Page Config
st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

header_1, header_2 = st.columns([1,3])
with header_1:

  st.image("Imagens/logo.png")

with header_2:

  st.title("Controle de Movimentação")

@st.cache_data
def carregar_bases():

  # Carregar excel
  file_path = "bases/Planilha de Movimentação.xlsx"

  fundos_df = pd.read_excel(file_path, sheet_name="Fundos")
  acoes_df = pd.read_excel(file_path, sheet_name="Ações")
  renda_fixa_df = pd.read_excel(file_path, sheet_name="Renda Fixa")

  bases_dict = {
      "Fundos":fundos_df,
      "Ações": acoes_df,
      "Renda Fixa":renda_fixa_df
  }

  return bases_dict


bases_df = carregar_bases()

colunas_1,colunas_2,coluna_3 = st.columns(3)

with colunas_1:

  seletor_de_abas = st.pills("Selecione o Ativo",options=["Fundos","Ações","Renda Fixa"],selection_mode="single",default="Fundos")

with colunas_2:

  base_selecionado_df = bases_df[seletor_de_abas]
  carteiras_unicas = base_selecionado_df["Carteira"].unique()
  selecionar_carteira = st.multiselect("Selecione a carteira",carteiras_unicas)

with coluna_3:

  today = datetime.now()
  la_atras = today - timedelta(days=1800)

  data_seletor = st.date_input(
        "Selecione a data",
        (la_atras, today),
        format="DD/MM/YYYY",
    )


if len(selecionar_carteira) == 0:
  base_filtrada = base_selecionado_df
else:
  base_filtrada = base_selecionado_df.loc[base_selecionado_df["Carteira"].isin(selecionar_carteira)]

if len(data_seletor) == 0:
  pass
else:
  if len(data_seletor) == 2:
    start_date, end_date = data_seletor
  else:
    start_date = data_seletor[0]
    end_date = start_date

  if seletor_de_abas == "Fundos":
    coluna_de_data = "Data Operação"
  else:
    coluna_de_data = "Data"

  base_filtrada = base_filtrada.loc[(base_filtrada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_filtrada[coluna_de_data] <= pd.Timestamp(end_date))]


total_financeiro = base_filtrada["Financeiro"].sum()
st.metric(label="Total Financeiro", value=f"R$ {total_financeiro}")

st.dataframe(base_filtrada,hide_index=True,use_container_width=True)
