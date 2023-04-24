import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud

# show average sentiment of dataset in a pie chart


def pie_chart(dataset, title='Overall Sentiment:'):
    # create a pie chart using the totals
    counts = [dataset['negative'][0], dataset['positive'][0], dataset['neutral'][0]]
    names = ['negative', 'positive', 'neutral']
    colour_dict = {'negative': 'red',
                   'positive': "green",
                   'neutral': '#FFD700'}
    fig = px.pie(values=counts, names=names,
                 color=names, color_discrete_map=colour_dict, hole=0.35)
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
        orientation="v",
        color_discrete_sequence=["#FFD700", "red", "green"]
    ).update_layout(xaxis_title="Sentiment", yaxis_title="Number of comments")
    bar_chart.update_xaxes(tickvals=(1, 2, 3), ticktext=[
                           "negative", "neutral", "positive"])

    st.plotly_chart(bar_chart)
