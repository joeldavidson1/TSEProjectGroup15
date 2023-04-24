import pandas as pd

def write_to_csv(dataframe: pd.DataFrame, filename: str):
    dataframe.to_csv(f'dataset/{filename}', index=False)


def get_length_of_csv(filename: str):
    # get the length of the csv if exists else return -1
    try:
        return pd.read_csv(
            filename, encoding='utf8').shape[0]
    except FileNotFoundError:
        print(f"File not found at: {filename}")
        return -1


def pd_dataframe_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv(index=False).encode('utf-8')
