import os
import glob
import numpy as np
from os import listdir
import pandas as pd



complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

best_kmers = open("data/best_kmers_canonical.jf", encoding = "utf-8")
contents = best_kmers.readlines()
len(contents)

#Generates the reverse complement of a given kmer
def reverse_complement(kmer):
    return ''.join([complement[base] for base in kmer[::-1]])

for i,c in enumerate(contents):
    if i % 2 != 0:
        if reverse_complement(c[:-1]) not in contents:
            contents.append(c[:-1])

contents

print(len(good_kmers))

