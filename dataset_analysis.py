import streamlit as st
from wordcloud import WordCloud
from analyser import Analyser
import chart


def dataset_analysis_UI():
    na = analyser()
    st.title('Facebook Sentiment Analysis')
    st.write("""
            ### Select an NLP model
            Choose between the two different sentiment analysis models
            """)
    st.sidebar.write("""
    ## About
    This is a statistical analysis of several thousand Facebook comments from...
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

    st.subheader('Sentiment by Post')
    if model == "Natural Language Toolkit (NLTK)":
        chart.display_post_sentiment(na, True)
    else:
        chart.display_post_sentiment(na, False)

    st.subheader('Word Frequencies')
    col1, col2 = st.columns(2)
    with col1:
        st.caption('These are the top most 50 common words:')
        st.dataframe(na.frequency_results)
    with col2:
        chart.word_cloud(na.frequency_results,
                         'Word Cloud of the most common words:')


def analyser():
    # -----------Analysis-----------------
    # analyzing the input csv file
    na = Analyser()
    na.get_all_comments()
    na.create_word_frequency_dataframe()

    return na
