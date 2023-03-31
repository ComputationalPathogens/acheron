import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from xgboost import XGBClassifier

def get_df(input_file1, input_file2):
    """

    :param input_file1: parquet file containing best_kmers and counts and column as genome file names
    :param input_file2: parquet file containing a row of all species with column being genome file names
    :return: a transposed df for analysis
    """
    df1 = pd.read_parquet(input_file1)
    df1 = df1.astype(np.int8)
    df2 = pd.read_parquet(input_file2)
    df = pd.concat([df1, df2])
    return df


def transpose(df):
    df = df.T
    return df







def main():
    """
    Program to:
    1. Read in {kmers} = {revcomp} parquet file and convert to pandas dataframe
    2. Search all kmers in all genomes
    3. Save output table as kmers (rows), genomes (columns), using only canonical kmers
    :return: Success
    """
    data = get_df('final_df_final.parquet','final_df_species.parquet')
    # df = data.swapaxes("index", "columns")
    # print(np.shape(df))
    # print(df.head(10).info(memory_usage = 'deep'))




if __name__ == '__main__':
    """
    Ensures program only executes as a script.
    """
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))