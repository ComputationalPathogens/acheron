import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa
import numpy as np
import dask.dataframe as dd

df = pd.read_csv('final_df_transposed_test.csv')
df.head(10)