import streamlit as st
import pandas as pd

# Streamlit Page Config
st.set_page_config(page_title="Controle de Movimentação", page_icon="💰", layout="wide")

# Carregar excel
file_path = "bases/Planilha de Movimentação.xlsx"
fundos_df = pd.read_excel(file_path, sheet_name="Fundos")

st.dataframe(fundos_df,hide_index=True,use_container_width=True)

# Cache Decorator
# @st.cache_data

# Mostrar dataframe


# Pills
# st.pills("Selecione o Ativo",options=["Fundos","Ações","Renda Fixa"],selection_mode="single",default="Fundos")
