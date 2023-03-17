#!/usr/bin/env python

import pandas as pd
import sys
import ahocorasick
import pathlib
import gzip
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np


def get_df_from_parquet(kmer_parquet_file):
    """
    For simplicity, this will just return a small dataframe
    :param kmer_parquet_file: ourput parquet file having column 0 as revcomp and column 1 as canonical kmers
    could be the output from add_reverse_complement
    :return:
    """
    df = pd.read_parquet(kmer_parquet_file)
    # sys.exit("done reading parquet")
    # We want to have the index be the revcomp kmer, so we can easily look up the canonical
    df = df.set_index(0)
    return df


def find_all_kmers(aho, genome_directory, kmer_df):
    """

    :param aho: ahocorasick automaton of all kmers
    :param genome_directory: the directory containing genome files that end with .gz
    :param kmer_df: dataframe from parquet file with 2 columns: reverse complements and canonical kmers
    :return: The final dataframe with rows as kmers, columns as genomes
    """

    # Create the final dataframe, removing duplicates by creating a set and then
    # converting the set into a list
    final_df = pd.DataFrame(index=[*set(kmer_df[1])], dtype=np.int8)
    files = []

    for gz_file in pathlib.Path(genome_directory).glob('*.gz'):
        print("Reading {}".format(gz_file))
        files.append(gz_file)

        with gzip.open(gz_file, 'rt') as fasta:
            # New genome column, currently names as file name
            # Default every kmer to 0 for each genome
            final_df[gz_file] = np.int8(0)
            alldata = str(fasta.readlines())

            # key is location of the kmer, and v is the kmer itself
            # we only care if it is present or not
            for _, v in aho.iter(alldata):
                # We need to look up the canonical kmer in the original kmer df
                # 'v' is the index which could be canonical or revcomp
                # The column '1' contains the canonical kmer
                # .at[] works on single values and is faster than loc[]
                final_df.at[kmer_df.at[v, 1], gz_file] = np.int8(1)
            # final_df[gz_file] = final_df[gz_file].astype('int8') ###############
        # fasta.close() #################
        if len(files) == 3:
            break

    return final_df


def create_aho_automaton(kmer_df):
    """
    Create the ahocorasick automaton
    :param kmer_df: dataframe from parquet file with 2 columns: reverse complements and canonical kmers
    :return: aho automaton
    """
    aho = ahocorasick.Automaton()

    # The index contains both canonical and revcomp kmers
    # kmer_df[1] contains only canonical kmers

    kmer_df.index.map(lambda x: aho.add_word(x,x))
    aho.make_automaton()
    return aho

def save_parquet1(final_df, output_file):
    """
    Take the final df and save it into a parquet file for later use.
    :param final_df: The final dataframe with rows as kmers, columns as genomes
    :param output_file: the parquet file location for the dataframe from dictionary to be saved.
    :return: Success
    """
    # df = pd.DataFrame(final_df.items())
    table = pa.Table.from_pandas(final_df)
    pq.write_table(table, output_file)

def main():
    """
    Program to:
    1. Read in {kmers} = {revcomp} parquet file and convert to pandas dataframe
    2. Search all kmers in all genomes
    3. Save output table as kmers (rows), genomes (columns), using only canonical kmers
    :return: Success
    """
    #  Ensure both arguments are specified
    if len(sys.argv) > 3:
        kmer_parquet_file = sys.argv[1]
        directory_of_genomes = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print("Program requires three arguments: needle_in_the_hay.py <kmer_parquet file> <directory_of_genomes> <output_file.parquet>")
        sys.exit(1)

    kmer_df = get_df_from_parquet(kmer_parquet_file)
    print("DF read")
    aho = create_aho_automaton(kmer_df)
    print("aho created")
    final_df = find_all_kmers(aho, directory_of_genomes, kmer_df)
    print("final df made")
    print(final_df.info(memory_usage="deep"))
    # Still need to create a function to save the output table ...
    save_parquet1(final_df, output_file)



if __name__ == '__main__':
    """
    Ensures program only executes as a script.
    """
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))
