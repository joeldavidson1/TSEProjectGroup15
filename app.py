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

st.caption('This is the NLTK results of the Facebook comments')
st.dataframe(na.sia_results)

st.caption('These are the top most 50 common words')
st.dataframe(na.frequency_results)

st.caption('Word Cloud showing highest frequency words in the whole dataset')
chart.word_cloud(na.frequency_results)

st.caption('The overall sentiment of the dataset')
chart.pie_chart(na.sia_results)

st.caption('The sentiment by post name')
chart.display_filtered_pie_chart(na)
