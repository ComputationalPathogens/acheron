#!/usr/bin/env python

import pandas as pd
import pyarrow.parquet as pq
import sys
import pyarrow as pa

COMPLEMENT = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}


def reverse_complement(kmer):
    """
    Generates the reverse complement of a given kmer using only A,T,C,G
    :param kmer: The kmer to reverse complement
    :return: The reverse complement of kmer
    """
    return ''.join([COMPLEMENT[base] for base in kmer[::-1]])


def revcomp_kmers(input_file):
    """
    Takes the filtered kmers file from Jellyfish and creates a dictionary with both canonical and revcomp kmers, with
    the keys giving both canonical and revcomp, and values the canonical.
    :param input_file: The Jellyfish kmer file filtered for kmers within a given frequency distribution.
    :return: The dictionary with {canonical} = {canonical} and {revcomp} = {canonical}
    """

    diction = {}
    with open(input_file, mode='r') as fh:
        # Use a slice to get every other line of the file, and read it in one by one
        # This is more memory efficient than readlines() which stores the whole thing in memory
        for _ in fh:
            kmer = fh.readline().strip()
            diction[kmer] = kmer
            diction[reverse_complement(kmer)] = kmer

    return diction


def save_parquet(final_dictionary, output_file):
    """
    Take the final dictionary of {kmer} = {kmer} / {revcomp} = {kmer} and save it into a parquet file for later use.
    This requires converting the dictionary into a dataframe.
    :param final_dictionary: {kmer} = {kmer} / {revcomp} = {kmer}
    :param output_file: the parquet file location for the dataframe from dictionary to be saved.
    :return: Success
    """
    df = pd.DataFrame(final_dictionary.items())
    table = pa.Table.from_pandas(df)
    pq.write_table(table, output_file)


def main():
    """
    Program to:
    1. Take in file of pre-filtered kmers
    2. Create a dictionary of {kmer} = {kmer} / {revcomp} = {kmer}
    3. Save this dictionary as a parquet file for fast loading in subsequent programs
    :return: Success
    """
    # best_kmers = 'data/best_kmers_canonical.jf'
    # output_file = 'rev_comp_dictionary.parquet'
    #  Ensure both arguments are specified
    if len(sys.argv) > 2:
        best_kmers = sys.argv[1]
        output_file = sys.argv[2]
    else:
        print("Program requires two arguments: add_reverse_complement <kmer_file> <output_file.parquet>")
        sys.exit(1)

    final_dictionary = revcomp_kmers(best_kmers)
    # final_dictionary = revcomp_kmers('data/best_kmers_canonical.jf')
    # save_parquet(final_dictionary, 'rev_comp_dictionary.parquet')
    save_parquet(final_dictionary, output_file)



if __name__ == '__main__':
    """
    Ensures program only executes as a script.
    """
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))
