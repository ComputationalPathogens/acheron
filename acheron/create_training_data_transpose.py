import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa
from csv import writer
import numpy as np

input_file = 'final_df_final.parquet'


# parquet_file = pq.ParquetFile(input_file)
# metadata = parquet_file.metadata
# schema = parquet_file.schema
# print("this is the schema")
# print(schema.names)
df = pd.read_parquet(input_file)
df = df.swapaxes("index", "columns")
df = df.astype('int8')
# print(df.head(10))

with open('final_df_transposed_test.csv', 'w', newline = '') as f:
    writer_object = writer(f)
    # for row in df.rows():
    writer_object.writerow(df.columns)
    for row in df.itertuples(index = False, name = None):
        writer_object.writerow([np.int8(val) for val in row])

'''
count =0
for i in schema.names:
    count += 1
    # print(table)
    index_name = table.index.values
    df_transposed = table.transpose().set_axis(index_name, axis=1, inplace=False)
    table_transposed = pa.Table.from_pandas(df_transposed)
    print("printing transposed table")
    print(table_transposed)
    pq.write_table(table_transposed, output_file)
    if count >= 5:
        break
result = pd.read_parquet(output_file)
print(result)
# df_transposed = pd.concat(transposed_list)
# print("printing transposed final df")
# print(df_transposed)
# table_transposed = pa.Table.from_pandas(df_transposed)
# pq.write_table(table_transposed, output_file)
'''