import streamlit as st
from wordcloud import WordCloud
from analyser import Analyser
import pandas as pd
import chart

def analyse_text_UI():
    st.title("Analyse your own text here")
    st.sidebar.write("""
    ## About
    Enter in text into the box and click submit to receive the sentimental analysis results.
    """)
    user_text_input = st.text_input(label ='Text Input', value = 'Replace me :)')
    if user_text_input:
    # create dataset in correct format 
        user_dict = {
                'from_post_id': [0],
                'message': [user_text_input]
        }
        dataset = pd.DataFrame(user_dict)

        na = analyser(dataset)
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
            st.write("""
                    ### Natural Language Toolkit (NLTK)
                    NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
                    """)
        else:
            st.write("""
                    ### Hugging Face RoBERTa
                    The RoBERTa model was proposed in RoBERTa: A Robustly Optimized BERT Pretraining Approach by Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, Veselin Stoyanov. It is based on Google’s BERT model released in 2018.

                    It builds on BERT and modifies key hyperparameters, removing the next-sentence pretraining objective and training with much larger mini-batches and learning rates.

                    This particular RoBERTa-base model has been trained on ~58M tweets and finetuned for sentiment analysis with the TweetEval benchmark. This model is suitable for English.
                    """)

        st.subheader('Overall')
        col1, col2 = st.columns(2)
        with col1:
            st.caption('The dataset:')
            if model == "Natural Language Toolkit (NLTK)":
                st.dataframe(na.sia_results.style.applymap(
                    na.colour_sentiment, subset=['compound']))

                with open('dataset/nltk_analysis_results.csv', 'rb') as f:
                    st.download_button('Download raw data', f,
                                    file_name='nltk_analysis_results.csv')
            else:
                st.dataframe(na.roberta_results)
                with open('dataset/roberta_analysis_results.csv', 'rb') as f:
                    st.download_button('Download raw data', f,
                                    file_name='roberta_analysis_results.csv')

        with col2:
            if model == "Natural Language Toolkit (NLTK)":
                chart.pie_chart(na.sia_results)
            else:
                chart.pie_chart(na.roberta_results)

        st.subheader('Word Frequencies')
        col1, col2 = st.columns(2)
        with col1:
            st.caption('These are the most common words:')
            st.dataframe(na.frequency_results)
        with col2:
            chart.word_cloud(na.frequency_results,
                            'Word Cloud of the most common words:')

def analyser(dataset):
    # -----------Analysis-----------------
    # analysing the input csv file
    na = Analyser(dataset)
    na.get_all_comments()
    na.create_word_frequency_dataframe()

    return na