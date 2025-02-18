import streamlit as st

# --- PAGE SETUP ---
movimentacao_page = st.Page(
    "views/movimentacao.py",
    title="Controle de Movimentação",
    icon=":material/savings:",
    default=True
)

graficos_page = st.Page(
    "views/graficos.py",
    title="Gráficos",
    icon=":material/savings:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Páginas": [movimentacao_page,graficos_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")

# --- RUN NAVIGATION ---
pg.run()
