import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa
from csv import writer

'''
def read_and_swap(file_directory):
    """
    reads the parquet file into pandas dataframe and transpose it using df.swapaxes
    :param file_directory: directory of parquet file
    :return: a transposed pandas dataframe
    """
    df = pd.read_parquet(file_directory)
    df = df.swapaxes("index", "columns")
    return df
'''

# Set path to input parquet file
input_path = 'final_df_final.parquet'
output_path = 'no_species.csv'
# Set chunk size for writing to output file
chunk_size = 1000

# Load parquet file into pandas dataframe
df = pd.read_parquet(input_path)

# Transpose dataframe
df_transposed = df.transpose()

# Open output file for writing
with open(output_path, 'w') as f:
    # Write header row to output file
    f.write(",".join(df_transposed.columns) + "\n")
    # Loop over rows of transposed dataframe
    for i in range(0, df_transposed.shape[0], chunk_size):
        # Write chunk of rows to output file
        f.write(df_transposed.iloc[i:i+chunk_size].to_csv(header=False))
print("success!")