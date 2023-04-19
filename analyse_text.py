import streamlit as st


def analyse_text_UI():
    st.title("Analyse your own text here")
    st.sidebar.write("""
    ## About
    Enter in text into the box and click submit to receive the sentimental analysis results.
    """)
    st.write("Text box here...")
