import streamlit as st
import plotly.express as px
from wordcloud import WordCloud

# show average sentiment of dataset in a pie chart
def pie_chart(dataset, title='Overall Sentiment'):
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

# show the average sentiment of a specific post
def display_filtered_pie_chart(analyzer):
    # Get unique post_ids
    unique_post_ids = analyzer.dataframe["post_name"].unique()
    selected_post_id = st.selectbox("Select a post:", unique_post_ids)

    # Filter data and calculate sentiment
    filtered_data = analyzer.filter_by_post(selected_post_id).copy() #need to change to post name on drop down
    filtered_sia_results = analyzer.calc_sentiment_filtered(filtered_data)

    # Display pie chart
    pie_chart(filtered_sia_results, title=f'Sentiment for post {selected_post_id}')

def word_cloud(dataset):
    # Generating word cloud
    text = dataset['word'].values
    string_text = ' '.join(text)

    wc = WordCloud().generate(string_text)

    st.caption('Most common words')
    st.image(wc.to_array(), width=650)