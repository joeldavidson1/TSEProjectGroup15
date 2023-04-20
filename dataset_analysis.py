import streamlit as st
from wordcloud import WordCloud
from analyser import Analyser
import chart


def dataset_analysis_UI():
    na = analyser()
    st.title('Facebook Sentiment Analysis')
    st.sidebar.write("""
    ## About
    This is a statistical analysis of several thousand Facebook comments from...
    """)
    # overall sentiment
    st.subheader('Overall')
    col1, col2 = st.columns(2)
    with col1:
        st.caption('The dataset:')
        st.dataframe(na.sia_results.style.applymap(
            na.colour_sentiment, subset=['compound']))

    with col2:
        chart.pie_chart(na.sia_results)

    st.subheader('Word Frequencies')
    col1, col2 = st.columns(2)
    with col1:
        st.caption('These are the top most 50 common words:')
        st.dataframe(na.frequency_results)
    with col2:
        chart.word_cloud(na.frequency_results,
                         'Word Cloud of the most common words:')

    st.subheader('Sentiment by Post')
    chart.display_post_sentiment(na)


def analyser():
    # -----------Analysis-----------------
    # analyzing the input csv file
    na = Analyser()
    na.get_all_comments()
    na.create_word_frequency_dataframe()

    return na
