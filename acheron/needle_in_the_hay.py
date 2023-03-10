#!/usr/bin/env python

import pandas as pd
import sys
import ahocorasick
import pathlib
import gzip


def get_df_from_parquet(kmer_parquet_file):
    """
    For simplicity, this will just return a small dataframe
    :param kmer_parquet_file:
    :return:
    """
    df = pd.read_parquet(kmer_parquet_file)

    # We want to have the index be the revcomp kmer, so we can easily look up the canonical
    df = df.set_index(0)
    return df


def find_all_kmers(aho, genome_directory, kmer_df):
    """

    :param aho: ahocorasick automaton of all kmers
    :param genome_directory:
    :param kmer_df:
    :return: The final dataframe with rows as kmers, columns as genomes
    """
    # Count is only for testing
    count = 0

    # Create the final dataframe, removing duplicates by creating a set and then
    # converting the set into a list
    final_df = pd.DataFrame(index=[*set(kmer_df[1])])

    for gz_file in pathlib.Path(genome_directory).glob('*.gz'):

        # <-This is just for testing to limit the number of genomes and print the df
        count += 1
        if count == 5:
            print(final_df)
            return
        # ->

        with gzip.open(gz_file, 'rt') as fasta:
            # New genome column, currently names as file name
            # Default every kmer to 0 for each genome
            final_df[gz_file] = 0
            alldata = str(fasta.readlines())

            # key is location of the kmer, and v is the kmer itself
            # we only care if it is present or not
            for _, v in aho.iter(alldata):
                # We need to look up the canonical kmer in the original kmer df
                # 'v' is the index which could be canonical or revcomp
                # The column '1' contains the canonical kmer
                final_df.loc[kmer_df.loc[v, 1], gz_file] = 1

    return final_df


def create_aho_automaton(kmer_df):
    """
    Create the ahocorasick automaton
    :param kmer_df:
    :return: aho
    """
    aho = ahocorasick.Automaton()

    # The index is the revcomp kmer
    for i in kmer_df.index:
        # We look up the canonical kmer to add to the automaton
        k2 = kmer_df.loc[i, 1]
        aho.add_word(i, i)
        aho.add_word(k2, k2)
    aho.make_automaton()
    return aho


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
    aho = create_aho_automaton(kmer_df)
    output_table = find_all_kmers(aho, directory_of_genomes, kmer_df)
    print(output_table)
    # Still need to create a function to save the output table ...


if __name__ == '__main__':
    """
    Ensures program only executes as a script.
    """
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))
