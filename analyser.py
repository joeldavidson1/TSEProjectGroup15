import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

import chart
import csv_writer

# nltk.download('popular')
# nltk.download('vader_lexicon')


class Analyser:

    def __init__(self):
            # load in precomputed sentiments
            self.sia_results = pd.read_csv('dataset/nltk_analysis_results.csv', encoding='utf8')
            self.roberta_results = pd.read_csv('dataset/roberta_analysis_results.csv', encoding='utf8')
            # read in the same data from the dataset
            rows = len(self.sia_results)
            self.dataframe = pd.read_csv('dataset/fb_news_comments_20K_hashed.csv', nrows = rows,encoding='utf8')
            # allows pandas to use the full comment instead of shortening it
            pd.set_option('display.max_colwidth', None)

            # use precomputed info
            self.all_comments = self.get_all_comments()
            self.word_frequency = []        


    def calc_word_frequency(self):
        all_words = parse_messages_for_analysis(self.all_comments)

        # Top (n) most common words and their frequency in a list of dictionaries
        freq = nltk.FreqDist(all_words)
        most_common_words = freq.most_common(50)

        return most_common_words

    def create_word_frequency_dataframe(self):
        most_common_words = self.calc_word_frequency()

        for i in most_common_words:
            dict_freq = {
                'word': i[0],
                'frequency': i[1]
            }
            self.word_frequency.append(dict_freq)
        self.frequency_results = pd.DataFrame(self.word_frequency)

    # return comments matching post_id
    def filter_by_post(self, post_id):
        filtered_data = self.sia_results[self.sia_results['from_post_id'] == post_id]
        return filtered_data

    # convert all the comments from the csv into one string
    def get_all_comments(self):
        return self.dataframe['message'].sum()

    # colour cell based on value relative to boundaries
    def colour_sentiment(self, val):
        boundary1 = -0.2
        boundary2 = 0.2
        if val < boundary1:
            colour = 'red'
        elif val < boundary2:
            colour = 'orange'
        else:
            colour = 'green'
        return f'background-color: {colour}'


def tokenize_words(comments: str):
   # tokenize the whole string
    return nltk.word_tokenize(comments)


def remove_non_words(comments: str):
    # remove any tokens which aren't words
    return [w for w in comments if w.isalpha()]


def remove_stop_words(comments: str):
    # remove stop words e.g. "to", "an", "a"
    stop_words = nltk.corpus.stopwords.words("english")
    return [w for w in comments if w.lower() not in stop_words]


def parse_messages_for_analysis(comments: str):
    tokenized = tokenize_words(comments)
    normal_words = remove_non_words(tokenized)
    all_words_without_stop_words = remove_stop_words(normal_words)
    return all_words_without_stop_words
