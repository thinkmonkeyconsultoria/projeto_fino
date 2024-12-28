import streamlit as st
import pandas as pd

st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

st.title("Controle de Movimentação")

file_path = "bases/Planilha de Movimentação.xlsx"

fundos_df = pd.read_excel(file_path, sheet_name="Fundos")
acoes_df = pd.read_excel(file_path, sheet_name="Ações")
renda_fixa_df = pd.read_excel(file_path, sheet_name="Renda Fixa")

selecionar_ativo = st.pills(
    "Selecione o Ativo",
    options=["Fundos","Ações","Renda Fixa"],
    selection_mode="single",
)
