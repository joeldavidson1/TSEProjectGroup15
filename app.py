import streamlit as st
from analyzer import Analyzer
from wordcloud import WordCloud
import chart

#-----------Analysis-----------------
# analyzing the input csv file
na = Analyzer('dataset/fb_news_comments_20K_hashed.csv')
na.calc_sentiment()
na.calc_word_frequency()

#-----------Webpage setout-----------
st.set_page_config(page_title='Facebook Sentimental Analysis',
                   layout='wide'
                   )

st.title('Facebook Sentiment Analysis')

# display the results on the webpage 
st.caption('This is the NLTK results of the Facebook comments')
st.dataframe(na.sia_results)

st.caption('These are the top most 50 common words')
st.dataframe(na.frequency_results)

chart.word_cloud(na.frequency_results)

chart.pie_chart(na.sia_results)


def display_filtered_pie_chart():
    # Get unique post_ids
    unique_post_ids = na.dataframe["post_name"].unique()
    selected_post_id = st.selectbox("Select a post:", unique_post_ids)

    # Filter data and calculate sentiment
    filtered_data = na.filter_by_post(selected_post_id).copy()
    filtered_sia_results = na.calc_sentiment_filtered(filtered_data)

    # Display pie chart
    chart.pie_chart(filtered_sia_results, title=f'Sentiment for post {selected_post_id}')



display_filtered_pie_chart()
