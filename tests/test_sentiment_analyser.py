from sentiment_analyser import Sentiment_Analyser, calc_compound
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
