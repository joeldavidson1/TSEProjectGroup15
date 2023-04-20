import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud

# show average sentiment of dataset in a pie chart


def pie_chart(dataset, title='Overall Sentiment:'):
    # mean each sentiment type
    mean_negative = dataset["negative"].mean()
    mean_positive = dataset["positive"].mean()
    mean_neutral = dataset["neutral"].mean()

    # create a pie chart using the means
    means = [mean_negative, mean_positive, mean_neutral]
    names = ['negative', 'positive', 'neutral']
    fig = px.pie(values=means, names=names)

    st.caption(title)
    st.plotly_chart(fig)


def select_post(analyzer):
    # get unique posts
    unique_post_ids = analyzer.dataframe["from_post_id"].unique()
    # create select box with all unique values
    return st.selectbox("Select a post:", unique_post_ids)


# show the average sentiment of a specific post
def display_post_sentiment(analyzer, nltk_analyser: bool):
    # Get unique post_ids
    # need to change to post name on drop down
    selected_post_id = select_post(analyzer)

    # Filter data and calculate sentiment
    filtered_data = analyzer.filter_by_post(
        selected_post_id, nltk_analyser).copy()

    # Display post
    st.caption('Post')
    # add post content so there is context for sentiment
    st.caption('post contents here..........')

    col1, col2 = st.columns(2)

    # Display comments
    with col1:
        st.caption('Post Comments:')
        comments = filtered_data['comment']
        st.dataframe(comments)

    with col2:
        # Display pie chart
        pie_chart(filtered_data, title='Sentiment for Post Comments:')


def word_cloud(dataset, title):
    # Generating word cloud
    text = dataset['word'].values
    string_text = ' '.join(text)

    wc = WordCloud().generate(string_text)

    st.caption(title)
    st.image(wc.to_array(), width=550)
