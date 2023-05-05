from analyser import Analyser, tokenize_words, remove_non_words, remove_stop_words, parse_messages_for_analysis
import nltk


def test_tokenize_words() -> None:
    tokenized = tokenize_words("This is a unit test.")
    assert tokenized == ['This', 'is', 'a', 'unit', 'test', '.']


def test_remove_non_words() -> None:
    removed_non_words = remove_non_words("Unit test 2, testing!...")
    assert removed_non_words == ['U', 'n', 'i', 't', 't',
                                 'e', 's', 't', 't', 'e', 's', 't', 'i', 'n', 'g']


def test_remove_stop_words() -> None:
    removed_stop_words = remove_stop_words(
        "This is a unit test. Testing for a pass.")
    assert removed_stop_words == ['h', ' ', ' ', ' ', 'u', 'n', ' ',
                                  'e', '.', ' ', 'e', 'n', 'g', ' ', 'f', 'r', ' ', ' ', 'p', '.']


def test_parse_message_for_analysis() -> None:
    parsed_words = parse_messages_for_analysis(
        "Unit testing 99. HopefullyThis! passes a test...")
    assert parsed_words == ['Unit', 'testing',
                            'HopefullyThis', 'passes', 'test']


def test_calc_word_frequency() -> None:
    analyser = Analyser()
    analyser.all_comments = "four, four, four, four, three, three, three, two, two, one"
    common_words = analyser.calc_word_frequency()
    assert common_words == [('four', 4), ('three', 3), ('two', 2), ('one', 1)]
