import streamlit as st
#from wordcloud import WordCloud
from analyzer import Analyzer

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

chart.word_cloud(na.frequency_results) # needs fixing as word cloud pip doesn't work

chart.pie_chart(na.sia_results)


