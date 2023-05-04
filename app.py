import streamlit as st
import about
import analyse_text
import dataset_analysis
from precompute import Precompute

number_of_comments = 2500  # number of comments to analyze

@st.cache_data(persist="disk")  # @st.cache # - for joel
# allows heavy computation to run only once
def pre_compute_analysis():
     p = Precompute()
     p.precompute_analysis('dataset/fb_news_comments_20K_hashed.csv', number_of_comments)

if __name__ == '__main__':
    # -----------Webpage setout-----------
    st.set_page_config(page_title='Facebook Sentimental Analysis',
                       layout='wide',
                       initial_sidebar_state="expanded"
                       )

    pre_compute_analysis()

    st.sidebar.title("Facebook Sentimental Analysis")

    PAGES = ["About", "Dataset Analysis", "Analyse Text"]
    page = st.sidebar.radio("Navigation", PAGES)

    if page == "About":
        about.about_UI()
    elif page == "Dataset Analysis":
        dataset_analysis.dataset_analysis_UI(number_of_comments)
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
