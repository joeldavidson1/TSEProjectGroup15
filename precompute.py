import csv_handler
from sentiment_analyser import Sentiment_Analyser


class Precompute:
    """
    A class which handles the pre-computation of the dataset

    """

    def __init__(self):
        pass

    def precompute_analysis(self, path, number_of_rows):
        """
        Read in precomputed values (csv files) if available else create them 

        Parameters
        ----------
        path : String
            The path to the dataset

        number_of_rows: int
            The number of rows to analyse

        """
        # only compute if an existing csv file isn't found or has a different number of rows
        if (csv_handler.get_length_of_csv('dataset/nltk_analysis_results.csv') >= number_of_rows and
                csv_handler.get_length_of_csv('dataset/nltk_analysis_results.csv') >= number_of_rows):
            print('precompute already done.')
        else:
            print('calculating values.')
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
     

if __name__ == '__main__':
   number_of_comments = 10000
   p = Precompute()
   p.precompute_analysis('dataset/fb_news_comments_20K_hashed.csv', number_of_comments)
