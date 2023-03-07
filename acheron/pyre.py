#!/usr/bin/env python

import pandas as pd
import sys
import gzip
import os
import glob

# import torch
# from torch import nn
# from torch.utils.data import DataLoader

# Create a DF of 1000bp fragments randomly from genomes based on metadata
# Number of samples should be controllable
# Output as a parquet file for easy IO
# Use this to train a Long-Short Term Memory classifier
# Perhaps update to BERT and compare, or compare to the PNAS BERT paper

def format_metadata(meta_file):
    '''
    Get the metadata from datasets / dataformat NCBI tool into DF format
    :return:
    '''
    infile = pd.read_csv(meta_file, delimiter='\t')
    print (infile.head())
    infile["Species"] = infile["Organism Name"].str.split(' ').str[:2].str.join(' ')
    return infile
    # infile.to_csv("~/brucella_species_metadata.csv")

def create_fragments(metadata, genome_directory):
    '''

    :param metadata: pandas DF
    :return:
    '''

    print(metadata.head())
    f_name = metadata.iloc[1 , 0]
    print(f_name)
    full_name = ''.join([os.path.join(genome_directory, f_name), '*.genomic.fna.gz'])
    print(full_name)
    f_name = glob.glob(full_name)

    gzip.open(os.path.join(genome_directory, f_name[0]))


def main():
    '''

    :return:
    '''
    metadata_file = sys.argv[1]
    genome_directory = sys.argv[2]

    metadata = format_metadata(metadata_file)
    create_fragments(metadata, genome_directory)



if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))

