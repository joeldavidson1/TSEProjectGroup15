import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax


import chart
import csv_handler
from sentiment_analyser import Sentiment_Analyser


class Analyser:
    """
    A class which handles the analysis of a Panda Dataframe

    Parameters
    ----------
    input_dataframe : Panda Dataframe, optional
        A Dataframe that needs to be analysed.
        If None then a Dataframe is read in from the default csv

    number_of_comments : Int, optional
        Only required if no Dataframe is given.
        The number of comments within the csv to be read in as a Dataframe.

    Attributes
    ---------- 
    analyser : Analyser
        analyser object 
    dataframe : Panda Dataframe
        overall dataset
    sia_results : Panda Dataframe
        nltk sentiment results
    roberta_results : Panda Dataframe
        roberta sentiment results
    posts_dataframe : Panda Dataframe  
        dataset post references
    all_comments : list of str
        list of all comments
    word_frequency : list of Dict (word and frequency)
        list of all words and their frequencies
    boundary : Int
        boundary used for sentiment categorising
    """
    def __init__(self, input_dataframe=None, number_of_comments=1):
        self.analyser = Sentiment_Analyser()

        if input_dataframe is None:
            # load in precomputed sentiments
            self.sia_results = pd.read_csv(
                'dataset/nltk_analysis_results.csv', encoding='utf8', nrows=number_of_comments)
            self.roberta_results = pd.read_csv(
                'dataset/roberta_analysis_results.csv', encoding='utf8', nrows=number_of_comments)
            # read in the same data from the dataset
            rows = len(self.sia_results)
            self.dataframe = pd.read_csv(
                'dataset/fb_news_comments_20K_hashed.csv', encoding='utf8', nrows=number_of_comments)
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

        # boundary for sentiment compound splitting
        self.boundary = 0.1

    def analyse_comment(self, nltk_analysis: bool, comment: str):
        """
        Analyse an individual comment

        Parameters
        ----------
        nltk_analysis : bool
            whether to use nltk or roberta for the analysis
        comment : string
            The comment to be analysed

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the comment and its analysed sentiment
    
        """
        analysed_comment = pd.DataFrame()

        if nltk_analysis:
            analysed_comment = self.analyser.calc_nltk_sentiment_text(comment)
        else:
            analysed_comment = self.analyser.calc_nltk_roberta_text(comment)

        return analysed_comment

    def calc_word_frequency(self):
        """
        Calculate word frequency

        Returns
        ----------
        2d Array
            An array of words and their frequencies 
    
        """
        all_words = parse_messages_for_analysis(self.all_comments)

        # Top (n) most common words and their frequency in a list of dictionaries
        freq = nltk.FreqDist(all_words)
        most_common_words = freq.most_common(50)

        return most_common_words

    def create_word_frequency_dataframe(self):
        """
        Calculate word frequency

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the words (string) and their frequencies (int)
    
        """
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
        """
        Filter results by post id

        Parameters
        ----------
        post_id : string
            The id of the post to filter by
        nltk_option : bool
            whether to use nltk or roberta for the analysis        

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the filtered comments
    
        """
        if nltk_option:
            filtered_data = self.sia_results[self.sia_results['from_post_id'] == post_id]
        else:
            filtered_data = self.roberta_results[self.roberta_results['from_post_id'] == post_id]

        return filtered_data

    # convert all the comments from the csv into one string
    def get_all_comments(self):
        """
        Concatenate all the comments into one string     

        Returns
        ----------
        Panda Dataframe
            A Dataframe containing the concatenated string
    
        """
        # check dataframe is not empty
        if isinstance(self.dataframe, pd.DataFrame):
            # get comments from column. Column name may vary between comment and message
            if 'comment' in self.dataframe.columns:
                return self.dataframe['comment'].sum()
            elif 'message' in self.dataframe.columns:
                return self.dataframe['message'].sum()
        return pd.DataFrame()

    # colour cell based on value relative to boundaries
    def colour_sentiment(self, val):
        """
        set the colour to red, orange or green of a cell by categorising its value between boundaries

        Parameters
        ----------
        val : int
            The value to categorise

        Returns
        ----------
        String
            A formatted string stating the colour of the cell
    
        """
        if val < -self.boundary:
            colour = 'red'
        elif val < self.boundary:
            colour = 'orange'
        else:
            colour = 'green'
        return f'background-color: {colour}'

    def count_sentiments(self, dataset: pd.DataFrame):
        """
        Count the number of positive, neutral and negative comments in a dataset

        Parameters
        ----------
        dataset : Panda Dataframe
            The dataset to search through 

        Returns
        ----------
        Panda Dataframe
            The total number of each category present in the dataset
    
        """
        # makes a separate dataframe for the number of sentiments out of all the comments
        negative = dataset.loc[dataset['compound'] < -self.boundary]
        positive = dataset.loc[dataset['compound'] > self.boundary]
        neutral = dataset.loc[(dataset['compound'] < self.boundary)
                              & (dataset['compound'] > -self.boundary)]

        new_dataframe = pd.DataFrame(columns=["negative", "neutral", "positive", "total"], data=[
                                     [negative.shape[0], neutral.shape[0], positive.shape[0], dataset.shape[0]]])
        return new_dataframe


def tokenize_words(comments: str):
    """
    Tokenize all comments

    Parameters
    ----------
    comments : String
        The comments to tokenize

    Returns
    ----------
    String
        A tokenize copy of the input comments

    """
    return nltk.word_tokenize(comments)


def remove_non_words(comments: str):
    """
    Remove any tokens which aren't letters

    Parameters
    ----------
    comments : String
        The comments to sort through

    Returns
    ----------
    String
        A copy of the input comments without non alphabet letters (a-z)

    """
    return [w for w in comments if w.isalpha()]


def remove_stop_words(comments: str):
    """
    Remove stop words e.g. "to", "an", "a"

    Parameters
    ----------
    comments : String
        The comments to sort through

    Returns
    ----------
    String
        A copy of the input comments without stop words

    """
    
    stop_words = nltk.corpus.stopwords.words("english")
    return [w for w in comments if w.lower() not in stop_words]


def parse_messages_for_analysis(comments: str):
    """
    Parse the comments for analysis

    Parameters
    ----------
    comments : String
        The comments to parse

    Returns
    ----------
    String
        A copy of the input comments without non-words and stop words

    """
    tokenized = tokenize_words(comments)
    normal_words = remove_non_words(tokenized)
    all_words_without_stop_words = remove_stop_words(normal_words)
    return all_words_without_stop_words
