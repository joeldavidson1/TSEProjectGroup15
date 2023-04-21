import pandas as pd


def write_to_csv(dataframe: pd.DataFrame, filename: str):
    dataframe.to_csv(f'dataset/{filename}', index=False)


def get_length_of_csv(filename: str):
    # get the size of the csv if exists else return -1
    try:
        return pd.read_csv(
            filename, encoding='utf8').size
    except FileNotFoundError:
        print(f"File not found at: {filename}")
        return -1


def pd_dataframe_to_csv(datframe: pd.DataFrame):
    return datframe.to_csv(index=False).encode('utf-8')


# def get_csv(filename) -> pd.DataFrame:
#     dataframe = pd.read_csv(filename, nrows=1000, encoding='utf8')

#     return dataframe
