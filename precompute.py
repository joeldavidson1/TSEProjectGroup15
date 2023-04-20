import csv_handler
from sentiment_analyser import Sentiment_Analyser


class Precompute:

    def __init__(self):
        pass

    def precompute_analysis(self, path, number_of_rows):
        # only compute if an existing csv file isn't found or has a different number of rows
        if (csv_handler.get_length_of_csv('dataset/nltk_analysis_results.csv') == number_of_rows and 
            csv_handler.get_length_of_csv('dataset/nltk_analysis_results.csv')  == number_of_rows):
            return 
        else:    
            # size of csv's are different so compute new
            analyser = Sentiment_Analyser(path, number_of_rows)
            # Get analysis results
            nltk_analysis_results = analyser.calc_nltk_sentiment()
            roberta_analysis_results = analyser.calc_roberta_sentiment()

            # write the results to csv files
            csv_handler.write_to_csv(
                nltk_analysis_results, 'nltk_analysis_results.csv')
            csv_handler.write_to_csv(
                roberta_analysis_results, 'roberta_analysis_results.csv')
