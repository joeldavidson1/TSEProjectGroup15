import pandas as pd
import streamlit as st


def write_to_csv(dataframe: pd.DataFrame, filename: str):
    """
    Save a dataframe to a csv file within the 'dataset' folder

    Parameters
    ----------
    dataframe : Panda Dataframe
        The data to save

    filename: String
        The filename of the csv file

    """
    dataframe.to_csv(f'dataset/{filename}', index=False)


def get_length_of_csv(filename: str):
    """
    Get the length of a given csv file

    Parameters
    ----------
    filename : string
        The filename of the file to read

    Returns
    ----------
    Int
        The length of the csv if found, else -1

    """
    # get the length of the csv if exists else return -1
    try:
        return pd.read_csv(
            filename, encoding='utf8').shape[0]
    except FileNotFoundError:
        print(f"File not found at: {filename}")
        return -1


@st.cache_data(persist="disk")  # @st.cache # - for joel
def pd_dataframe_to_csv(dataframe: pd.DataFrame):
    """
    Convert a dataframe to csv format

    Parameters
    ----------
    dataframe : Panda Dataframe
        The dataset to convert

    Returns
    ----------
    String
        The csv formatted dataframe

    """
    return dataframe.to_csv(index=False).encode('utf-8')

# remove any invalid rows from dataset


def remove_na(dataframe):
    """
    removes any rows which messages are null

    Parameters
    ----------
    dataframe : Panda Dataframe
        The dataset to parse

    Returns
    ----------
    Panda Dataframe
        A parsed copy of the dataset

    """
    return dataframe[dataframe['message'].notna()]


def remove_long_strings(dataframe, max_string_length):
    """
    removes any rows which messages are too long to analyse

    Parameters
    ----------
    dataframe : Panda Dataframe
        The dataset to parse

    Returns
    ----------
    Panda Dataframe
        A parsed copy of the dataset

    """
    return dataframe[dataframe['message'].str.len() < max_string_length]


# purge csv file for any invalid strings
if __name__ == '__main__':
    max_string_length = 512  # roberta max string length
    raw = pd.read_csv(
        'dataset/RAW_fb_news_comments_20K_hashed.csv', encoding='utf8')
    formatted = remove_na(raw)
    print(f"pre purge: {raw.size}")
    print(f"after purge: {formatted.size}")
    formatted = remove_long_strings(formatted, max_string_length)
    print(f"after purge string lengths: {formatted.size}")
    write_to_csv(formatted, "fb_news_comments_20K_hashed.csv")
