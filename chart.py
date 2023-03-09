import streamlit as st
import plotly.express as px
from wordcloud import WordCloud

def pie_chart(dataset):
    mean_negative = dataset["negative"].mean()
    mean_positive = dataset["positive"].mean()
    mean_neutral = dataset["neutral"].mean()

    means = [mean_negative, mean_positive, mean_neutral]
    names = ['negative', 'positive', 'neutral']
    fig = px.pie(values=means, names=names) # need to add colours to chart 

    st.caption('Overall Sentiment')
    st.plotly_chart(fig)



def word_cloud(dataset):
    # Generating word cloud
    text = dataset['word'].values
    string_text = ' '.join(text)

    wc = WordCloud().generate(string_text)

    st.caption('Most common words')
    st.image(wc.to_array(), width=650)
