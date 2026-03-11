import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: #e6e6e6;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            color: #00e5ff;
        }
        .stButton>button {
            background-color: #00e5ff;
            color: black;
            border-radius: 8px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
