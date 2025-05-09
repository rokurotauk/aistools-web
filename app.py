import streamlit as st
from decoder_tab import render_decoder_tab
from visualisation_tab import render_visualisation_tab

st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["🧭 Decode AIS Messages", "🗺️ Visualise AIS Data"])

with tab1:
    render_decoder_tab()

with tab2:
    render_visualisation_tab()
