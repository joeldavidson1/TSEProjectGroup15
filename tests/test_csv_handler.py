from csv_handler import write_to_csv, get_length_of_csv, pd_dataframe_to_csv, remove_long_strings, remove_na
import pandas as pd


def test_write_to_csv() -> None:
    """
    Tests the write csv function

    """
    test = {
        'col1': [1, 2, 3],
        'col2': [5, 6, 7]
    }
    dataframe = pd.DataFrame(test)
    write_to_csv(dataframe, 'test_write.csv')
    same = pd.read_csv('dataset/test_write.csv').equals(dataframe)
    assert same


def test_get_length_of_csv() -> None:
    """
    Tests the get length of csv function

    """
    test = {
        'col1': [1, 2, 3],
        'col2': [5, 6, 7]
    }
    dataframe = pd.DataFrame(test)
    write_to_csv(dataframe, 'test_write.csv')
    length = get_length_of_csv('dataset/test_write.csv')
    assert length == dataframe.shape[0]


def test_remove_long_strings() -> None:
    """
    Tests the remove long strings function

    """
    test = {
        'message': ['Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et',
                    'Lorem ipsum dolor sit amet. Sed enim voluptatem et modi debitis sit voluptatum voluptatem est eius cumque non quis doloribus eum itaque recusandae et ullam repellendus. Qui tenetur praesentium ut dolorem aliquam qui quae totam aut neque officiis est blanditiis quam. Ut galisum consequatur ea ipsa laborum eos incidunt voluptate non veritatis eligendi. 33 esse ipsam ut quia consequatur aut maxime deleniti? Est officiis velit quo ipsam quam et perspiciatis earum vel quis corrupti ab minus libero et molestiae necessitatibus.'
                    ]
    }
    dataframe = pd.DataFrame(test)
    max_string_length = 512  # roberta max string length
    removed_long = remove_long_strings(dataframe, max_string_length)
    assert removed_long.shape[0] == 1


def test_remove_na() -> None:
    """
    Tests the remove na function

    """
    test = {
        'message': ['Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et',
                    None,
                    ]
    }
    dataframe = pd.DataFrame(test)
    removed_na = remove_na(dataframe)
    assert removed_na.shape[0] == 1


def test_pd_dataframe_to_csv() -> None:
    """
    Tests the pd dataframe to csv function

    """
    test = {
        'col1': [1, 2, 3],
        'col2': [5, 6, 7]
    }
    dataframe = pd.DataFrame(test)
    csv_file = pd_dataframe_to_csv(dataframe)
    assert isinstance(csv_file, (bytes))
