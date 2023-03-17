#!usr/bin/env python

import subprocess
import urllib.request
import sys

def etools_path(species, output_file):
    """
    Perform etools function by esearch and efetch via subprocess, to save ftp path of
    all genomes of interest from a given species in assembly database(could be changed)
     in NCBI into output_file for later download
    :param species: name of species of interest, in string format as typed in the
    NCBI's search bar
    :param output_file: the text file location for the paths to be saved
    :return: Success
    """
    # search in NCBI database assembly for matched results of the given species,
    # could check output via print(step.stdout), and step1.stdout will return the
    # information of search, such as number of matched results
    # species in format like 'brucella_suis'
    cmd1 = ('esearch -db assembly -query ' + species).split()
    step1 = subprocess.run(cmd1, shell = False, check= False, stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    # fetch document summary
    cmd2 = 'efetch -format docsum'.split()
    step2 = subprocess.run(cmd2, shell = False, check = False, input = step1.stdout ,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # extract reference sequence ftp path from document summary
    cmd3 = 'xtract -pattern DocumentSummary -element FtpPath_RefSeq'.split()
    step3 = subprocess.run(cmd3, shell = False, check = False, input = step2.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    link = (step3.stdout.decode("utf-8"))
    # create the file in directory, and write the path into the file
    file = open(output_file, "w")
    file.write(link)
    file.close()

def get_file(output_file):
    """
    download corresponding files from paths in output_file using urlretrieve, and save the files under data/
    :param output_file: the file containing all the path of our target genomes, the one from etools_path
    :return: Success
    """
    file1 = open(output_file, "r")
    urls = file1.readlines()

    # i[:-1] removes the /n at the end of link, and i[55:] is the RefSeq assembly accession
    # note: 'data/' could be changed to any directory name for files to be saved at
    for i in urls:
        i = (i[:-1])
        download_link = i +'/' + i[55:] +'_genomic.fna.gz'
        # print(download_link)
        name = 'data/' + str(i[55:]) +'.genomic.fna.gz'
        # print(name)
        urllib.request.urlretrieve(download_link, name)


def main():
    """
    Program to:
    1. search and fetch all the related results of our target species on NCBI,
    and save their RefSeq path to output_file
    2. download the files according the saved paths
    :return: Success
    """
    #  Ensure both arguments are specified
    if len(sys.argv) > 2:
        species = sys.argv[1]
        output_file = sys.argv[2]
    else:
        print("Program requires two arguments: etools.py <species> <output_file.txt>")
        sys.exit(1)

    etools_path(species, output_file)
    print("path saved, start downloading seq files")
    get_file(output_file)
    print("download complete")

if __name__ == '__main__':
    """
    Ensures program only executes as a script.
    """
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))













