import csv_writer
from sentiment_analyser import Sentiment_Analyser

class Precompute:

    def __init__(self):
        pass

    def precompute_analysis(self, path, number_of_rows):
        analyser = Sentiment_Analyser(path, number_of_rows)
        # Get analysis results
        nltk_analysis_results = analyser.calc_nltk_sentiment()
        roberta_analysis_results = analyser.calc_roberta_sentiment()

        # write the results to csv files
        csv_writer.write_to_csv(
            nltk_analysis_results, 'nltk_analysis_results.csv')
        csv_writer.write_to_csv(
            roberta_analysis_results, 'roberta_analysis_results.csv')
        

if __name__ == '__main__':
    p = Precompute()
    p.precompute_analysis('dataset/fb_news_comments_20K_hashed.csv', 5)
        
    

        

