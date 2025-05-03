import pandas as pd

def read_file(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df


def merge_files(file1: str, file2: str, column_join: str) -> pd.DataFrame:
    ds1 = read_file(file1)
    ds2 = read_file(file2)
    merged_data = pd.merge(ds1, ds2, on=column_join, how="inner")
    return merged_data

def mean_columns(df: pd.DataFrame, columnaName: str, columns: list) -> pd.DataFrame:
   
   df[columnaName] = df[columns].mean(axis=1)
   return df