import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np


class Sentiment_Analyser:
    """
    A class which handles the analysis of a Panda Dataframe

    Parameters
    ----------
    path=None, rows=1
    path : String, optional
        The path to a csv formatted dataset
        If None then an empty Dataframe is created

    rows : Int, optional
        Only required if a path is given.
        The number of comments within the csv to be read in as a Dataframe.

    Attributes
    ---------- 
    dataframe : Panda Dataframe
        Overall dataset
    sia : Sentiment Intensity Analyzer
        NLTK Sentiment analyzer 
    """
    def __init__(self, path=None, rows=1):
        nltk.download('popular')
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()
        self.dataframe = pd.DataFrame()
        if path:
            self.dataframe = pd.read_csv(path, nrows=rows, encoding='utf8')
        else:
            self.dataframe = pd.DataFrame()

        # allows pandas to use the full comment instead of shortening it
        pd.set_option('display.max_colwidth', None)

    
    def calc_nltk_sentiment(self):
        """
        Calc NLTK sentiment of dataframe

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the analysed sentiment of the original dataframe
    
        """

        nltk_analysis_results = []
        for index, row in (self.dataframe.iterrows()):
            # append the sentiment analysis results to a dictionary
            # retain key info such as comment and post id
            sia_sentiment_dict = {
                'comment': row['message'],
                'compound': calc_compound(self.sia.polarity_scores(row['message'])['neg'],
                                          self.sia.polarity_scores(row['message'])['pos']),
                'negative': self.sia.polarity_scores(row['message'])['neg'],
                'neutral': self.sia.polarity_scores(row['message'])['neu'],
                'positive': self.sia.polarity_scores(row['message'])['pos'],
                'from_post_id': str(row['from_post_id']).split("_", 1)[1]
            }
            print(f'NLTK Compute: {index + 1} / {self.dataframe.shape[0]}')
            # append the dictionaries to the list of dicts
            nltk_analysis_results.append(sia_sentiment_dict)
        return pd.DataFrame(nltk_analysis_results)

    def calc_roberta_sentiment(self):
        """
        Calc Roberta sentiment of dataframe

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the analysed sentiment of the original dataframe
    
        """
        roberta_analysis_results = []

        # obtain pre-trained model - https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
        MODEL, tokenizer, model = self.load_roberta_model()

        for index, row in (self.dataframe.iterrows()):
            # append the sentiment analysis results to a dictionary
            # retain key info such as comment and post id
            sentiment_scores = self.roberta_sentiment(
                row['message'], MODEL, tokenizer, model)
            roberta_sentiment_dict = {
                'comment': row['message'],
                'compound': calc_compound(sentiment_scores[0], sentiment_scores[2]),
                'negative': sentiment_scores[0],
                'neutral': sentiment_scores[1],
                'positive': sentiment_scores[2],
                'from_post_id': row['from_post_id'].split("_", 1)[1]
            }
            print(f'Roberta Compute: {index + 1} / {self.dataframe.shape[0]}')
            # append the dictionaries to the list of dicts
            roberta_analysis_results.append(roberta_sentiment_dict)
        return pd.DataFrame(roberta_analysis_results)


    def load_roberta_model(self):
        """
        Load in the roberta model

        Returns
        ----------
        String
            model used
        AutoTokenizer
            tokenizer to parse strings
        AutoModelForSequenceClassification
            pre-trained roberta model
    
        """
        print("Roberta: Loading Model")
        MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

        print("Roberta: Creating Tokenizer")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL, model_max_length=512)  # max length for roberta = 512

        print("Roberta: Classifying Model")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        return MODEL, tokenizer, model

    def roberta_sentiment(self, text_sample, MODEL, tokenizer, model):
        """
        Calc NLTK sentiment of text

        Returns
        ----------
        List of Ints
            A list of the NLTK results (negative, neutral, positive, compound)
    
        """
        # tokenizer encodes text to binary for the model to analyse
        encoded_text = tokenizer(
            text_sample, return_tensors='pt', truncation=True)

        # output as numbers the results of the analysis
        output = model(**encoded_text)

        # calculate mean S
        scores = output[0][0].detach().numpy()

        # softmax ensures the scores of the results all sum up to 1 as probabilties, other e.g. negative could = 3, positive 2 etc.
        # See - https://deepai.org/machine-learning-glossary-and-terms/softmax-layer
        scores = softmax(scores)
        return scores

    def calc_nltk_sentiment_text(self, text_sample):
        """
        Calc NLTK sentiment of text

        Returns
        ----------
        Panda Dataframe
            The NLTK results (comment, negative, neutral, positive, compound)
    
        """
        sia_results = []
        sentiment_scores = self.sia.polarity_scores(text_sample)
        sia_sentiment_dict = {
            'comment': text_sample,
            'compound': calc_compound(sentiment_scores['neg'], sentiment_scores['pos']),
            'negative': sentiment_scores['neg'],
            'positive': sentiment_scores['pos'],
            'neutral': sentiment_scores['neu']
        }

        sia_results.append(sia_sentiment_dict)
        return pd.DataFrame(sia_results)

    def calc_nltk_roberta_text(self, text_sample):
        """
        Calc Roberta sentiment of text

        Returns
        ----------
        Panda Dataframe
            The Roberta results (comment, negative, neutral, positive, compound)
    
        """
        roberta_results = []
        # obtain pre-trained model - https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
        MODEL, tokenizer, model = self.load_roberta_model()
        sentiment_scores = self.roberta_sentiment(
            text_sample, MODEL, tokenizer, model)
        roberta_sentiment_dict = {
            'comment': text_sample,
            'compound': calc_compound(sentiment_scores[0], sentiment_scores[2]),
            'negative': sentiment_scores[0],
            'positive': sentiment_scores[2],
            'neutral': sentiment_scores[1]
        }

        roberta_results.append(roberta_sentiment_dict)
        return pd.DataFrame(roberta_results)

# finds the bias between positive and negative sentiment
# 1 - 0 = 1 so positive sentiment


def calc_compound(negative, positive):
    """
        Calculate compound sentiment through the difference between positive and negative components

        Parameters
        ----------
        negative : int
            The negative sentiment
        positive : int
            The postive sentiment

        Returns
        ----------
        Int
            The difference between positive and negative (compound)
    
        """
    return positive - negative
