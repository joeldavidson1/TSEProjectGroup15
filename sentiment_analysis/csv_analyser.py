# Run pip install -r requirements.txt in terminal of this directory before running the script

import nltk
import csv
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('popular', 'vader_lexicon')

with open('fb_news_comments_20K_hashed.csv', 'r', encoding='utf8') as csv_file:
    # Read in first (n) lines of the csv_file
    head = [next(csv_file) for x in range(500)]
    csv_reader = csv.DictReader(head)

    # pretrained sentiment analyzer called VADER (Valence Aware Dictionary and sEntiment Reasoner).
    sia = SentimentIntensityAnalyzer()

    results = []
    all_messages = ""
    for row in csv_reader:
        # convert all the messages from the csv into one string
        all_messages += row['message']

        # add results to dictionarycd
        sentiment_dict = {
            'negative': sia.polarity_scores(row['message'])['neg'],
            'neutral': sia.polarity_scores(row['message'])['neu'],
            'positive': sia.polarity_scores(row['message'])['pos'],
            'compound': sia.polarity_scores(row['message'])['compound'],
            'message': row['message']
        }
        results.append(sentiment_dict)

    # tokenize the whole string
    tokenized = nltk.word_tokenize(all_messages)

    # remove any tokens which aren't words
    all_words = [w for w in tokenized if w.isalpha()]

    # remove stop words e.g. "to", "an", "a"
    stop_words = nltk.corpus.stopwords.words("english")
    all_words = [w for w in all_words if w.lower() not in stop_words]

    # Top (n) most common words and their frequency in a list of dictionaries
    freq = nltk.FreqDist(all_words)
    most_common_words = freq.most_common(25)
    word_frequency = []
    for i in most_common_words:
        dict_freq = {
            'word': i[0],
            'frequency': i[1]
        }
        word_frequency.append(dict_freq)

    # write to a csv file the sentiment analysis scores and the corresponding message
    with open('sentiment_analysis.csv', 'w', encoding='utf8') as new_file:
        fieldnames = ['negative', 'neutral', 'positive', 'compound', 'message']
        csv_writer = csv.DictWriter(
            new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()

        for entry in results:
            csv_writer.writerow(entry)

    # write to a csv file the most common words and their frequency
    with open('word_frequency.csv', 'w', encoding='utf8') as new_file:
        fieldnames = ['word', 'frequency']
        csv_writer = csv.DictWriter(
            new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()

        for entry in word_frequency:
            csv_writer.writerow(entry)

csv_file.close()
print('Created Files...')
