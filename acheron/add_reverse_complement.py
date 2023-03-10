import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
best_kmers = open("data/best_kmers_canonical.jf", encoding = "utf-8")
contents = best_kmers.readlines()
good_kmers = []
for i,c in enumerate(contents):
    if i % 2 != 0:
        good_kmers.append(c[:-1])



#Generates the reverse complement of a given kmer
def reverse_complement(kmer):
    return ''.join([complement[base] for base in kmer[::-1]])

diction = {}
for i in good_kmers:
    diction[i] = reverse_complement(i)

df = pd.DataFrame(diction.items())
table = pa.Table.from_pandas(df)
pq.write_table(table, 'add_reverse_complement.parquet')