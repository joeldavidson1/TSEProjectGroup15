import pandas as pd


def write_to_csv(dataframe, filename):
    dataframe.to_csv(f'dataset/{filename}', index=False)
