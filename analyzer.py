import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('popular')
nltk.download('vader_lexicon')


class Analyzer:

    def __init__(self, path=None):
        if path:
            self.dataframe = pd.read_csv(path, nrows=50, encoding='utf8')
            # allows pandas to use the full comment instead of shortening it
            pd.set_option('display.max_colwidth', None)
        else:
            self.dataframe = pd.DataFrame()

        self.analysis_results = []
        self.all_comments = ""
        self.word_frequency = []
        self.sia_results = pd.DataFrame()
        self.frequency_results = pd.DataFrame()

    def calc_sentiment(self):
        sia = SentimentIntensityAnalyzer()

        for index, row in (self.dataframe.iterrows()):
            # append the sentiment analysis results to a dictionary
            # retain key info such as comment and post id
            sentiment_dict = {
                'from_post': row['post_name'],
                'negative': sia.polarity_scores(row['message'])['neg'],
                'neutral': sia.polarity_scores(row['message'])['neu'],
                'positive': sia.polarity_scores(row['message'])['pos'],
                'compound': sia.polarity_scores(row['message'])['compound'],
                'comment': row['message']
            }
            self.analysis_results.append(sentiment_dict)
            self.sia_results = pd.DataFrame(self.analysis_results)

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

    def filter_by_post(self, post_id):
        filtered_data = self.sia_results[self.sia_results['from_post'] == post_id]
        return filtered_data

    def get_all_comments(self):
        # convert all the comments from the csv into one string
        self.all_comments = self.dataframe['message'].sum()


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
