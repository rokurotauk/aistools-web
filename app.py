import streamlit as st
from decoder_tab import render_decoder_tab
from visualisation_tab import render_visualisation_tab
from encoder_tab import render_encoder_tab
from checksum_tab import render_checksum_tab
from replay_tab import render_replay_tab
from jump_detector_tab import render_jump_detector_tab
from mmsi_extractor_tab import render_mmsi_extractor_tab

st.set_page_config(layout="wide")

tabs = st.tabs([
    "🧭 Decode AIS Messages",
    "🗺️ Visualise AIS Data",
    "✉️ Encode AIS Messages",
    "✅ AIS Checksum Validator",
    "⏯️ AIS Replay",
    "📈 AIS Jump Detector",
    "🔍 AIS MMSI Extractor"
])

with tabs[0]:
    render_decoder_tab()

with tabs[1]:
    render_visualisation_tab()

with tabs[2]:
    render_encoder_tab()

with tabs[3]:
    render_checksum_tab()

with tabs[4]:
    render_replay_tab()

with tabs[5]:
    render_jump_detector_tab()

with tabs[6]:
    render_mmsi_extractor_tab()