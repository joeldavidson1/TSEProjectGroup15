import pandas as pd


def write_to_csv(dataframe, filename):
    dataframe.to_csv(f'dataset/{filename}', index=False)

# get the size of the csv if exists else return -1
def get_length_of_csv(filename):
    try:
         return pd.read_csv(
            filename, encoding='utf8').size   
    except FileNotFoundError:
        print(f"File not found at: {filename}")
        return -1
    