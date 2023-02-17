import nltk
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('popular')
nltk.download('vader_lexicon')

st.set_page_config(page_title='Facebook Sentimental Analysis',
                   layout='wide'
                   )

st.title('Facebook Sentiment Analysis')

##### could separate the following into functions so streamlit portion only here in this file... ######
dataframe = pd.read_csv('fb_news_comments_20K_hashed.csv',
                        nrows=50, encoding='utf8')

# allows pandas to use the full comment instead of shortening it
pd.set_option('display.max_colwidth', None)


sia = SentimentIntensityAnalyzer()

analysis_results = []
all_comments = ""

for index, row in (dataframe.iterrows()):
    # convert all the comments from the csv into one string
    all_comments += row['message']

    # append the sentiment analysis results to a dictionary
    sentiment_dict = {
        'negative': sia.polarity_scores(row['message'])['neg'],
        'neutral': sia.polarity_scores(row['message'])['neu'],
        'positive': sia.polarity_scores(row['message'])['pos'],
        'compound': sia.polarity_scores(row['message'])['compound'],
        'message': row['message']
    }
    analysis_results.append(sentiment_dict)

# tokenize the whole string
tokenized = nltk.word_tokenize(all_comments)

# remove any tokens which aren't words
all_words = [w for w in tokenized if w.isalpha()]

# remove stop words e.g. "to", "an", "a"
stop_words = nltk.corpus.stopwords.words("english")
all_words = [w for w in all_words if w.lower() not in stop_words]

# Top (n) most common words and their frequency in a list of dictionaries
freq = nltk.FreqDist(all_words)
most_common_words = freq.most_common(50)
word_frequency = []
for i in most_common_words:
    dict_freq = {
        'word': i[0],
        'frequency': i[1]
    }
    word_frequency.append(dict_freq)


sia_results = pd.DataFrame(analysis_results)
frequency_results = pd.DataFrame(word_frequency)

st.caption('This is the NLTK results of the Facebook comments')
st.dataframe(sia_results)

st.caption('These are the top most 50 common words')
st.dataframe(frequency_results)

# Generating word cloud
text = frequency_results['word'].values
string_text = ' '.join(text)
wc = WordCloud().generate(string_text)

st.caption('Most common words')
st.image(wc.to_array(), width=650)
