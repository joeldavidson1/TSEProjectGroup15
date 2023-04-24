import streamlit as st
from wordcloud import WordCloud
from analyser import Analyser
import pandas as pd
import chart
import csv_handler


def analyse_text_UI():
    st.title("Analyse your own text here")
    st.sidebar.write("""
    ## About
    Enter in text into the box and click submit to receive the sentimental analysis results.
    """)
    user_text_input = st.text_input(label='Text Input', value='Replace me :)')
    if user_text_input:
        # create dataset in correct format
        user_dict = {
            'message': [user_text_input]
        }
        dataset = pd.DataFrame(user_dict)
        na = Analyser(dataset)

        st.title('Facebook Sentiment Analysis')
        st.write("""
                ### Select an NLP model
                Choose between the two different sentiment analysis models
                """)
        st.sidebar.write("""
        ## About
        This is a statistical analysis of several thousand Facebook comments from the dataset: https://github.com/jbencina/facebook-news. The analysis aims to show the polarizing nature of facebook comments.
        """)

        model = st.selectbox("Select a model", [
            "Natural Language Toolkit (NLTK)", "Hugging Face RoBERTa"])

        # overall sentiment

        if model == "Natural Language Toolkit (NLTK)":
            st.write("## Natural Language Toolkit (NLTK)")
        else:
            st.write("## Hugging Face RoBERTa")

        st.subheader('Overall')
        col1, col2 = st.columns(2)
        nltk_analysis = na.analyse_comment(True, user_text_input)
        roberta_analysis = na.analyse_comment(False, user_text_input)

        with col1:
            st.caption('The dataset:')
            if model == "Natural Language Toolkit (NLTK)":
                st.dataframe(nltk_analysis.style.applymap(
                    na.colour_sentiment, subset=['compound']))

                user_csv = csv_handler.pd_dataframe_to_csv(nltk_analysis)
                st.download_button("Download raw data", user_csv,
                                   file_name="nltk_your_text_analysis_results.csv")
            else:
                st.dataframe(roberta_analysis)

                user_csv = csv_handler.pd_dataframe_to_csv(roberta_analysis)
                st.download_button("Download raw data", user_csv,
                                   file_name="roberta_your_text_analysis_results.csv")

        with col2:
            if model == "Natural Language Toolkit (NLTK)":
                counts = na.count_sentiments(nltk_analysis)
            else:
                counts = na.count_sentiments(roberta_analysis)
            chart.pie_chart(counts)

        st.subheader('Word Frequencies')
        col1, col2 = st.columns(2)
        with col1:
            st.caption('These are the most common words:')
            st.dataframe(na.create_word_frequency_dataframe())
        with col2:
            chart.word_cloud(na.create_word_frequency_dataframe(),
                             'Word Cloud of the most common words:')
