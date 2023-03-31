import pandas as pd
import sys
import ahocorasick
import pathlib
import gzip
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
from Bio import SeqIO

species_df = pd.read_parquet('final_df_species.parquet')
final_df = pd.read_parquet('final_df_final.parquet')
final_df = final_df.astype('int8')
# col_names = final_df.columns.values.tolist()

# for i in range(len(col_names)):
#     col_names[i] = col_names[i][48:]
# final_df.set_axis(col_names, axis=1, inplace=True)
table = pa.Table.from_pandas(final_df)
pq.write_table(table, 'final_df_final.parquet')
print('we have progress')

training_df = pd.concat([species_df,final_df])
training_df_arr = training_df.to_numpy()
training_df_arr_t = np.transpose(training_df_arr)
print('it works!')
col_in_df = training_df.index.values.tolist()
ind_in_df = training_df.columns.values.tolist()
table_final = pa.Table.from_pandas(pd.DataFrame(training_df_arr_t, index = ind_in_df, columns = col_in_df))
pq.write_table(table_final, 'final_df_training.parquet')
print('omg!')





