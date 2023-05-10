from analyser import Analyser, tokenize_words, remove_non_words, remove_stop_words, parse_messages_for_analysis
import nltk
import pandas as pd


def test_tokenize_words() -> None:
    """
    Tests the tokenize words function

    """
    tokenized = tokenize_words("This is a unit test.")
    assert tokenized == ['This', 'is', 'a', 'unit', 'test', '.']


def test_remove_non_words() -> None:
    """
    Tests the remove non words function

    """
    removed_non_words = remove_non_words("Unit test 2, testing!...")
    assert removed_non_words == ['U', 'n', 'i', 't', 't',
                                 'e', 's', 't', 't', 'e', 's', 't', 'i', 'n', 'g']


def test_remove_stop_words() -> None:
    """
    Tests the remove stop words function

    """
    removed_stop_words = remove_stop_words(
        "This is a unit test. Testing for a pass.")
    assert removed_stop_words == ['h', ' ', ' ', ' ', 'u', 'n', ' ',
                                  'e', '.', ' ', 'e', 'n', 'g', ' ', 'f', 'r', ' ', ' ', 'p', '.']


def test_parse_message_for_analysis() -> None:
    """
    Tests the parse message function

    """
    parsed_words = parse_messages_for_analysis(
        "Unit testing 99. HopefullyThis! passes a test...")
    assert parsed_words == ['Unit', 'testing',
                            'HopefullyThis', 'passes', 'test']


def test_calc_word_frequency() -> None:
    """
    Tests the calc word frequency function

    """
    analyser = Analyser()
    analyser.all_comments = "four, four, four, four, three, three, three, two, two, one"
    common_words = analyser.calc_word_frequency()
    assert common_words == [('four', 4), ('three', 3), ('two', 2), ('one', 1)]


def test_analyse_comment() -> None:
    analyser = Analyser()
    comment = "This is some sample text"
    data = {'comment': [comment],
            'compound': 0.000000,
            'negative': 0.000000,
            'positive': 0.000000,
            'neutral': 1.000000
            }
    df = pd.DataFrame(data, index=[0])
    analysed_comment = analyser.analyse_comment(
        nltk_analysis=True, comment=comment)
    pd.testing.assert_frame_equal(analysed_comment, df)


def test_create_word_frequency_dataframe() -> None:
    analyser = Analyser()
    analyser.all_comments = "four, four, four, four, three, three, three, two, two, one"
    data = {'word': ['four', 'three', 'two', 'one'],
            'frequency': [4, 3, 2, 1]
            }
    df = pd.DataFrame(data)
    common_words_df = analyser.create_word_frequency_dataframe()
    pd.testing.assert_frame_equal(common_words_df, df)


def test_get_all_comments() -> None:
    analyser = Analyser()
    analyser_data = {'comment': ['Sample text', 'testing sample', 'pytest']
                     }
    analyser_df = pd.DataFrame(analyser_data)
    analyser.dataframe = analyser_df
    all_comments = analyser.get_all_comments()
    merged_comments = 'Sample texttesting samplepytest'
    assert all_comments == merged_comments


def test_filter_by_post() -> None:
    analyser = Analyser()
    analyser_data = {'comment': ['sample text', 'sample', 'testing'],
                     'compound': [0.000000, 0.000000, 0.000000],
                     'negative': [0.000000, 0.000000, 0.000000],
                     'neutral': [1.000000, 1.000000, 1.000000],
                     'positive': [0.000000, 0.000000, 0.000000],
                     'from_post_id': [111, 111, 222]
                     }
    analyser_df = pd.DataFrame(analyser_data)
    analyser.sia_results = analyser_df
    filtered_data = analyser.filter_by_post(111, True)

    data = {'comment': ['sample text', 'sample'],
            'compound': [0.000000, 0.000000],
            'negative': [0.000000, 0.000000],
            'neutral': [1.000000, 1.000000],
            'positive': [0.000000, 0.000000],
            'from_post_id': [111, 111]
            }
    df = pd.DataFrame(data)
    print(filtered_data)
    print(df)
    pd.testing.assert_frame_equal(filtered_data, df)


def test_count_sentiments() -> None:
    analyser = Analyser()
    analyser_data = {'compound': [0.4, -0.2, 0.9, -0.6]}
    analyser_df = pd.DataFrame(analyser_data)
    counted_sentiments = analyser.count_sentiments(analyser_df)

    data = {'negative': 2,
            'neutral': 0,
            'positive': 2,
            'total': 4
            }
    df = pd.DataFrame(data, index=[0])

    pd.testing.assert_frame_equal(counted_sentiments, df)


def test_colour_sentiment() -> None:
    analyser = Analyser()
    colour = analyser.colour_sentiment(0.8)

    assert colour == 'background-color: green'
