import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

import chart
import csv_handler
from sentiment_analyser import Sentiment_Analyser

# nltk.download('popular')
# nltk.download('vader_lexicon')


class Analyser:

    def __init__(self, input_dataframe=None):
        self.analyser = Sentiment_Analyser()

        if input_dataframe is None:
            # load in precomputed sentiments
            self.sia_results = pd.read_csv(
                'dataset/nltk_analysis_results.csv', encoding='utf8')
            self.roberta_results = pd.read_csv(
                'dataset/roberta_analysis_results.csv', encoding='utf8')
            # read in the same data from the dataset
            rows = len(self.sia_results)
            self.dataframe = pd.read_csv(
                'dataset/fb_news_comments_20K_hashed.csv', nrows=rows, encoding='utf8')
            self.posts_dataframe = pd.read_csv(
                'dataset/fb_news_posts_20K.csv', nrows=rows, encoding='utf8')
        else:
            # analyse user input
            self.dataframe = input_dataframe
            # self.sia_text_results = self.analyser.calc_nltk_sentiment_text(
            # input_dataframe)
            # self.roberta_text_results = self.analyser.calc_nltk_roberta_text(
            # input_dataframe)

        # allows pandas to use the full comment instead of shortening it
        pd.set_option('display.max_colwidth', None)

        # use precomputed info
        self.all_comments = self.get_all_comments()
        self.word_frequency = []

    def analyse_comment(self, nltk_analysis: bool, comment: str):
        analysed_comment = pd.DataFrame()

        if nltk_analysis:
            analysed_comment = self.analyser.calc_nltk_sentiment_text(comment)
        else:
            analysed_comment = self.analyser.calc_nltk_roberta_text(comment)

        return analysed_comment

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
        return pd.DataFrame(self.word_frequency)

    # return comments matching post_id
    def filter_by_post(self, post_id, nltk_option: bool):
        if nltk_option:
            filtered_data = self.sia_results[self.sia_results['from_post_id'] == post_id]
        else:
            filtered_data = self.roberta_results[self.roberta_results['from_post_id'] == post_id]

        return filtered_data

    # convert all the comments from the csv into one string
    def get_all_comments(self):
        if isinstance(self.dataframe, pd.DataFrame):
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

    def count_reviews(self, dataset: pd.DataFrame):
        # makes a separate dataframe for the number of sentiments out of all the comments
        negative = dataset.loc[dataset['compound'] < -0.2]
        positive = dataset.loc[dataset['compound'] > 0.2]
        neutral = dataset.loc[(dataset['compound'] < 0.2)
                              & (dataset['compound'] > -0.2)]

        new_dataframe = pd.DataFrame(columns=["negative", "neutral", "positive", "total"], data=[
                                     [negative.shape[0], neutral.shape[0], positive.shape[0], dataset.shape[0]]])

        return new_dataframe


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
