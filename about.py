import streamlit as st
import csv_handler
import pandas as pd
from analyser import Analyser


def about_UI():
    """
    Create the about section of the website

    """
    st.title("About")

    st.write("""
            This website contains a statistical analysis of several thousand Facebook comments taken from various publicly available pages in 2017.
            It features two different sentimental analysis models which are explained in more detail below.
            """)
    st.write("""
            ### Natural Language Toolkit (NLTK)
            NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
            
            Source: https://www.nltk.org
            """)

    st.write("""
            ### Hugging Face RoBERTa
            The RoBERTa model was proposed in RoBERTa: A Robustly Optimized BERT Pretraining Approach by Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, Veselin Stoyanov. It is based on Google’s BERT model released in 2018.

            It builds on BERT and modifies key hyperparameters, removing the next-sentence pretraining objective and training with much larger mini-batches and learning rates.

            This particular RoBERTa-base model has been trained on ~58M tweets and finetuned for sentiment analysis with the TweetEval benchmark. This model is suitable for English.
            
            Source: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
            """)
