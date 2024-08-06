import streamlit as st
from vis_helpers import vis_utils


def main_page():
    quant_logo = vis_utils.show_quant_logo(width="40%")
    st.markdown(quant_logo, unsafe_allow_html=True)
    

    col, = st.columns(1)
    with col:

        st.markdown("<h1 style='text-align: center; padding:0; margin:0 0 150px 0;'>Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>by</h5>", unsafe_allow_html=True)
    
    optimater_logo = vis_utils.show_logo(width="35%")
    st.markdown(optimater_logo, unsafe_allow_html=True)
