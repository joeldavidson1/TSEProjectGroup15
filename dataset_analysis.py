import streamlit as st
from wordcloud import WordCloud
from analyser import Analyser
import chart


def dataset_analysis_UI():
    na = Analyser()
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

    st.subheader(
        "Bar chart showing the number of reviews of each sentiment (only works for NLTK, needs RoBERTa adding)")
    chart.bar_chart(na.count_reviews(na.sia_results))

    st.subheader('Word frequencies of the whole comment dataset')
    col1, col2 = st.columns(2)
    with col1:
        st.caption('These are the top most 50 common words:')
        st.dataframe(na.create_word_frequency_dataframe())
    with col2:
        chart.word_cloud(na.create_word_frequency_dataframe(),
                         'Word Cloud of the most common words:')

    st.subheader('Sentiment by post')
    if model == "Natural Language Toolkit (NLTK)":
        post_analysis_UI(na, True, "Natural Language Toolkit (NLTK)")
    else:
        post_analysis_UI(na, False, "other")


def post_analysis_UI(analyser: Analyser, nltk_analyser: bool, model: str):
    #  Get unique post_ids
    # need to change to post name on drop down
    selected_post_id = select_post(analyser)

    # Filter data and calculate sentiment
    filtered_data = analyser.filter_by_post(
        selected_post_id, nltk_analyser).copy()

    # Display post
    st.write("#### Post message: ")
    the_post = analyser.posts_dataframe[analyser.posts_dataframe['post_id'].str.contains(
        str(selected_post_id))]
    st.write(the_post['message'].to_string(index=False))
    st.write(the_post['link'].to_string(index=False))

    col1, col2 = st.columns(2)

    # Display comments
    with col1:
        st.caption('Post comments:')
        comments = filtered_data['comment']
        st.dataframe(comments)

    with col2:
        # Display pie chart
        chart.pie_chart(
            filtered_data, title='Mean Sentiment for Post Comments:')

    st.subheader("Sentiment by comment")
    comment = st.selectbox("Select a comment from the post", comments)
    analyser.dataframe = comment
    st.write("#### Comment:")
    st.write(comment)

    if model == "Natural Language Toolkit (NLTK)":
        nltk_result = analyser.analyse_comment(True, comment)
        chart.pie_chart(nltk_result)
    else:
        roberta_result = analyser.analyse_comment(False, comment)
        chart.pie_chart(roberta_result)


def select_post(analyser: Analyser):
    # get unique posts
    unique_post_ids = analyser.sia_results["from_post_id"].unique()
    # create select box with all unique values
    return st.selectbox("Select a post by post ID:", unique_post_ids)
