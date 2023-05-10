import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud


def pie_chart(dataset, title='Overall Sentiment Makeup:'):
    """
    Create a streamlit pie chart using the totals within the dataset

    Parameters
    ----------
    dataset : Panda Dataframe
        The data to display

    title : String
        The title of the chart

    """

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
    """
    Create a streamlit wordlcloud using the frequencies within the dataset

    Parameters
    ----------
    dataset : Panda Dataframe
        The data to display

    title : String
        The title of the chart
        
    """

    text = dataset['word'].values
    string_text = ' '.join(text)

    wc = WordCloud(background_color="rgba(255, 255, 255, 0)", mode="RGBA").generate(string_text)
    st.caption(title)
    st.image(wc.to_array(), width=550)


def bar_chart(dataset, title = 'Sentiment Count:'):   
    """
    Create a streamlit bar chart using the totals within the dataset

    Parameters
    ----------
    dataset : Panda Dataframe
        The data to display

    title : String
        The title of the chart
        
    """
    
    formatted_dataset = {
        'Sentiment':["negative", "neutral", "positive"],
        'Number of Comments': [dataset['negative'][0], dataset['neutral'][0], dataset['positive'][0]]          
                         }
    bar_chart = px.bar(
        data_frame=formatted_dataset,
        x = 'Sentiment',
        y = 'Number of Comments',
        orientation="v"
    ).update_layout(xaxis_title="Sentiment", yaxis_title="Number of Comments")
    bar_chart.update_xaxes(type = 'category')
    bar_chart.update_traces(marker_color = ["red", "#FFD700", "green"])
    st.caption(title)
    st.plotly_chart(bar_chart)
