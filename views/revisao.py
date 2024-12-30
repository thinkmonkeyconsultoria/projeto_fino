import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Streamlit Page Config
st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

seletor_de_abas = st.pills("Selecione o Ativo",options=["Fundos","Ações","Renda Fixa"],selection_mode="single",default="Fundos")

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

st.title("algum título!!")

bases_df = carregar_bases()

base_selecionado_df = bases_df[seletor_de_abas]

carteiras_unicas = base_selecionado_df["Carteira"].unique()

selecionar_carteira = st.selectbox("Selecione a carteira",carteiras_unicas)

base_filtrada = base_selecionado_df.loc[base_selecionado_df["Carteira"] == selecionar_carteira]

today = datetime.now()
la_atras = today - timedelta(days=1800)

data_seletor = st.date_input(
      "Selecione a data",
      (la_atras, today),
      format="DD/MM/YYYY",
  )

st.dataframe(base_filtrada,hide_index=True,use_container_width=True)
