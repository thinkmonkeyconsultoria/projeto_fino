import streamlit as st
import pandas as pd

st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

st.title("Controle de Movimentação")

file_path = "bases/Planilha de Movimentação.xlsx"

fundos_df = pd.read_excel(file_path, sheet_name="Fundos")
acoes_df = pd.read_excel(file_path, sheet_name="Ações")
renda_fixa_df = pd.read_excel(file_path, sheet_name="Renda Fixa")

st.dataframe(fundos_df)
st.dataframe(acoes_df)
st.dataframe(renda_fixa_df)
