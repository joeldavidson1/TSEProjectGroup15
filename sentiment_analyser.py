import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# nltk.download('popular')
# nltk.download('vader_lexicon')


class Sentiment_Analyser:

    def __init__(self, path=None, rows=1):
        self.sia = SentimentIntensityAnalyzer()
        self.dataframe = pd.DataFrame()
        if path:
            self.dataframe = pd.read_csv(path, nrows=rows, encoding='utf8')
        else:
            self.dataframe = pd.DataFrame()

        # allows pandas to use the full comment instead of shortening it
        pd.set_option('display.max_colwidth', None)

    # calc nltk sentiment
    def calc_nltk_sentiment(self):
        nltk_analysis_results = []
        for index, row in (self.dataframe.iterrows()):
            # append the sentiment analysis results to a dictionary
            # retain key info such as comment and post id
            sia_sentiment_dict = {
                'negative': self.sia.polarity_scores(row['message'])['neg'],
                'neutral': self.sia.polarity_scores(row['message'])['neu'],
                'positive': self.sia.polarity_scores(row['message'])['pos'],
                'compound': self.sia.polarity_scores(row['message'])['compound'],
                'comment': row['message'],
                'from_post_id': str(row['from_post_id']).split("_", 1)[1]
            }
            # append the dictionaries to the list of dicts
            nltk_analysis_results.append(sia_sentiment_dict)
        return pd.DataFrame(nltk_analysis_results)

    def calc_roberta_sentiment(self):
        roberta_analysis_results = []
        for index, row in (self.dataframe.iterrows()):
            # append the sentiment analysis results to a dictionary
            # retain key info such as comment and post id
            sentiment_scores = self.roberta_sentiment(row['message'])
            roberta_sentiment_dict = {
                'negative': sentiment_scores[0],
                'neutral': sentiment_scores[1],
                'positive': sentiment_scores[2],
                'comment': row['message'],
                'from_post_id': row['from_post_id'].split("_", 1)[1]
            }

            # append the dictionaries to the list of dicts
            roberta_analysis_results.append(roberta_sentiment_dict)
        return pd.DataFrame(roberta_analysis_results)

    def roberta_sentiment(self, text_sample):
        # obtain pre-trained model - https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
        MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)

        # tokenizer encodes text to binary for the model to analyse
        encoded_text = tokenizer(text_sample, return_tensors='pt')

        # output as numbers the results of the analysis
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()

        # softmax ensures the scores of the results all sum up to 1 as probabilties, other e.g. negative could = 3, positive 2 etc.
        # See - https://deepai.org/machine-learning-glossary-and-terms/softmax-layer
        scores = softmax(scores)
        return scores

    def calc_nltk_sentiment_text(self, text_sample):
        sia_results = []
        polarity_scores = self.sia.polarity_scores(text_sample)
        sia_sentiment_dict = {
            'negative': polarity_scores['neg'],
            'neutral': polarity_scores['neu'],
            'positive': polarity_scores['pos'],
            'compound': polarity_scores['compound'],
            'message': text_sample
        }

        sia_results.append(sia_sentiment_dict)
        return pd.DataFrame(sia_results)

    def calc_nltk_roberta_text(self, text_sample):
        roberta_results = []
        sentiment_scores = self.roberta_sentiment(text_sample)
        roberta_sentiment_dict = {
            'negative': sentiment_scores[0],
            'neutral': sentiment_scores[1],
            'positive': sentiment_scores[2],
            'message': text_sample
        }

        roberta_results.append(roberta_sentiment_dict)
        return pd.DataFrame(roberta_results)
