#!/usr/bin/env python

import pandas as pd
import sys

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
    infile["Species"] = infile["Organism Name"].apply(lambda x: " ".join(x.split()[:2]))
    infile.to_csv("~/brucella_species_metadata.csv")


def main():
    '''

    :return:
    '''
    metadata_file = sys.argv[1]
    format_metadata(metadata_file)




if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))

