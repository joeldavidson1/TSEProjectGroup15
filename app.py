import streamlit as st
import analyse_text
import dataset_analysis
from precompute import Precompute


@st.cache
# allows heavy computation to run only once
def pre_compute_analysis():
    p = Precompute()
    p.precompute_analysis('dataset/fb_news_comments_20K_hashed.csv', 5)


if __name__ == '__main__':
    # -----------Webpage setout-----------
    st.set_page_config(page_title='Facebook Sentimental Analysis',
                       layout='wide',
                       initial_sidebar_state="expanded"
                       )

    pre_compute_analysis()

    st.sidebar.title("Facebook Sentimental Analysis")

    PAGES = ["Dataset Analysis", "Analyse Text"]
    page = st.sidebar.radio("Navigation", PAGES)

    if page == "Dataset Analysis":
        dataset_analysis.dataset_analysis_UI()
    elif page == "Analyse Text":
        analyse_text.analyse_text_UI()

    # Hiding the Streamlit style
    hide_st_style = """
                <style>
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
