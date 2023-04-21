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


def word_cloud(dataset, title):
    # Generating word cloud
    text = dataset['word'].values
    string_text = ' '.join(text)

    wc = WordCloud().generate(string_text)

    st.caption(title)
    st.image(wc.to_array(), width=550)


def bar_chart(dataset):
    bar_chart = px.bar(
        data_frame=dataset,
        x=["negative", "neutral", "positive"],
        y="value",
        orientation="v"
    ).update_layout(xaxis_title="Sentiment", yaxis_title="Number of comments")
    bar_chart.update_xaxes(tickvals=(1, 2, 3), ticktext=[
                           "negative", "neutral", "positive"])

    st.plotly_chart(bar_chart)
