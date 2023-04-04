import streamlit as st
from analyzer import Analyzer
from wordcloud import WordCloud
import chart

# -----------Analysis-----------------
# analyzing the input csv file
na = Analyzer('dataset/fb_news_comments_20K_hashed.csv')
na.get_all_comments()
na.calc_sentiment()
na.create_word_frequency_dataframe()

# -----------Webpage setout-----------
st.set_page_config(page_title='Facebook Sentimental Analysis',
                   layout='wide'
                   )

st.title('Facebook Sentiment Analysis')

# display the results on the webpage

# overall sentiment
st.subheader('Overall')
col1, col2 = st.columns(2)
with col1:
    st.caption('The dataset:')
    st.dataframe(na.sia_results.style.applymap(na.colour_sentiment, subset=['compound']))

with col2:
    chart.pie_chart(na.sia_results)

st.subheader('Word Frequencies')
col1, col2 = st.columns(2)
with col1:
    st.caption('These are the top most 50 common words:')
    st.dataframe(na.frequency_results)
with col2:
    chart.word_cloud(na.frequency_results, 'Word Cloud of the most common words:')

st.subheader('Sentiment by Post')
chart.display_post_sentiment(na)
