from csv_handler import write_to_csv, get_length_of_csv, pd_dataframe_to_csv
import pandas as pd
import os

def test_write_to_csv() -> None:
    test = {
        'col1': [1,2,3],
        'col2': [5,6,7]
    }
    dataframe = pd.DataFrame(test)
    write_to_csv(dataframe, 'test_write.csv')
    same = pd.read_csv('dataset/test_write.csv').equals(dataframe)
    assert same
    

def test_get_length_of_csv() -> None:
    test = {
        'col1': [1,2,3],
        'col2': [5,6,7]
    }
    dataframe = pd.DataFrame(test)
    write_to_csv(dataframe, 'test_write.csv')
    length = get_length_of_csv('dataset/test_write.csv')
    assert length == dataframe.shape[0]
