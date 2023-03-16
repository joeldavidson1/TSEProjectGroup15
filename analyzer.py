import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('popular')
nltk.download('vader_lexicon')

class Analyzer:
    analysis_results = []
    all_comments = ""
    word_frequency = []
    sia_results = pd.DataFrame()
    frequency_results = pd.DataFrame()

    def __init__(self, path=None):
        if path:
            self.dataframe = pd.read_csv(path, nrows=50, encoding='utf8')
            # allows pandas to use the full comment instead of shortening it
            pd.set_option('display.max_colwidth', None)
        else:
            self.dataframe = pd.DataFrame()
     

    def calc_sentiment(self):        
        sia = SentimentIntensityAnalyzer()      
        for index, row in (self.dataframe.iterrows()):
            # convert all the comments from the csv into one string
            self.all_comments += row['message']

            # append the sentiment analysis results to a dictionary
            sentiment_dict = {
                'negative': sia.polarity_scores(row['message'])['neg'],
                'neutral': sia.polarity_scores(row['message'])['neu'],
                'positive': sia.polarity_scores(row['message'])['pos'],
                'compound': sia.polarity_scores(row['message'])['compound'],
                'message': row['message']
            }
            self.analysis_results.append(sentiment_dict)
            self.sia_results = pd.DataFrame(self.analysis_results)

    def calc_word_frequency(self):
        # tokenize the whole string
        tokenized = nltk.word_tokenize(self.all_comments)

        # remove any tokens which aren't words
        all_words = [w for w in tokenized if w.isalpha()]

        # remove stop words e.g. "to", "an", "a"
        stop_words = nltk.corpus.stopwords.words("english")
        all_words = [w for w in all_words if w.lower() not in stop_words]

        # Top (n) most common words and their frequency in a list of dictionaries
        freq = nltk.FreqDist(all_words)
        most_common_words = freq.most_common(50)        
        for i in most_common_words:
            dict_freq = {
                'word': i[0],
                'frequency': i[1]
            }
            self.word_frequency.append(dict_freq)        
        self.frequency_results = pd.DataFrame(self.word_frequency)

    def filter_by_post(self, post_id):
        filtered_data = self.dataframe[self.dataframe['post_name'] == post_id]
        return filtered_data

    def calc_sentiment_filtered(self, dataframe):
        sia = SentimentIntensityAnalyzer()
        analysis_results_filtered = []

        for index, row in (dataframe.iterrows()):
            sentiment_dict = {
                'negative': sia.polarity_scores(row['message'])['neg'],
                'neutral': sia.polarity_scores(row['message'])['neu'],
                'positive': sia.polarity_scores(row['message'])['pos'],
                'compound': sia.polarity_scores(row['message'])['compound'],
                'message': row['message']
            }
            analysis_results_filtered.append(sentiment_dict)

        sia_results_filtered = pd.DataFrame(analysis_results_filtered)
        return sia_results_filtered
