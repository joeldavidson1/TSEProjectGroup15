import streamlit as st
import analyse_text
import dataset_analysis


# -----------Webpage setout-----------
st.set_page_config(page_title='Facebook Sentimental Analysis',
                   layout='wide',
                   initial_sidebar_state="expanded"
                   )

st.sidebar.title("Facebook Sentimental Analysis")

PAGES = ["Dataset Analysis", "Analyse Text"]
page = st.sidebar.radio("Navigation", PAGES)

if page == "Dataset Analysis":
    dataset_analysis.dataset_analysis_UI()
elif page == "Analyse Text":
    analyse_text.analyse_text_UI()
