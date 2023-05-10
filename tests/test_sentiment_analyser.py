from sentiment_analyser import Sentiment_Analyser, calc_compound
import pandas as pd
import numpy
import nltk


def test_cacl_compound() -> None:
    compound_sum = calc_compound(-0.55, 0.45)
    assert compound_sum == 1


def test_calc_nltk_sentiment_text() -> None:
    sia = Sentiment_Analyser()
    text_sample = 'This is good sample text'
    test = {
        'comment': text_sample,
        'compound': 0.420000,
        'negative': 0.000000,
        'positive': 0.420000,
        'neutral': 0.580000
    }
    calculated_sample_results = sia.calc_nltk_sentiment_text(text_sample)
    assert calculated_sample_results['comment'].iloc[0] == text_sample
    assert calculated_sample_results['compound'].iloc[0] == 0.420000
    assert calculated_sample_results['negative'].iloc[0] == 0.000000
    assert calculated_sample_results['positive'].iloc[0] == 0.420000
    assert calculated_sample_results['neutral'].iloc[0] == 0.580000


def test_calc_robert_sentiment_text() -> None:
    sia = Sentiment_Analyser()
    text_sample = 'This is good sample text'
    test = {
        'comment': text_sample,
        'compound': 0.9368450045585632,
        'negative': 0.004708835389465094,
        'positive': 0.9415538311004639,
        'neutral': 0.0537373423576355
    }

    calculated_sample_results = sia.calc_nltk_roberta_text(text_sample)
    assert calculated_sample_results['comment'].iloc[0] == text_sample
    assert calculated_sample_results['compound'].iloc[0] == 0.9368450045585632
    assert calculated_sample_results['negative'].iloc[0] == 0.004708835389465094
    assert calculated_sample_results['positive'].iloc[0] == 0.9415538311004639
    assert calculated_sample_results['neutral'].iloc[0] == 0.0537373423576355


def test_calc_nltk_sentiment() -> None:
    sia = Sentiment_Analyser()
    sia_data = {'message': 'This is good sample text',
                'from_post_id': '012_111'
                }
    sia_df = pd.DataFrame(sia_data, index=[0])
    sia.dataframe = sia_df
    calculated_sentiment = sia.calc_nltk_sentiment()

    data = {'comment': 'This is good sample text',
            'compound': 0.420000,
            'negative': 0.000000,
            'neutral': 0.580000,
            'positive': 0.420000,
            'from_post_id': '111'
            }
    df = pd.DataFrame(data, index=[0])
    pd.testing.assert_frame_equal(calculated_sentiment, df)


def test_calc_roberta_sentiment() -> None:
    sia = Sentiment_Analyser()
    sia_data = {'message': 'This is good sample text',
                'from_post_id': '012_111'
                }
    sia_df = pd.DataFrame(sia_data, index=[0])
    sia.dataframe = sia_df
    calculated_sentiment = sia.calc_roberta_sentiment()

    data = {'comment': 'This is good sample text',
            'compound': numpy.float32(0.9368450045585632),
            'negative': numpy.float32(0.004708835389465094),
            'neutral': numpy.float32(0.0537373423576355),
            'positive': numpy.float32(0.9415538311004639),
            'from_post_id': '111'
            }
    df = pd.DataFrame(data, index=[0])
    pd.testing.assert_frame_equal(calculated_sentiment, df)
