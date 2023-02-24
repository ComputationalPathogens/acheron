#!usr/bin/env python
''' my user guide
micromamba activate ach.0.8
cd acheron      cd data        cd -        cd ~      rm -r data     mkdir data
        python experimental.py
etools command: esearch -db assembly -query "Brucella_microti" | efetch -format docsum | xtract -pattern DocumentSummary -element FtpPath_RefSeq | awk -F"/" '{print $0"/"$NF"_genomic.fna.gz"}' > testfile.txt | wget -i testfile.txt
count number files downloaded in current directory: ls -1 | wc -l
example filename: GCF_000022745.1_ASM2274v1.genomic.fna
command line unzipping file: gzip -dk GCF_000022745.1_ASM2274v1.genomic.fna.gz
move file up: cp GCF_947242805.1_B6.fna.gz ../
cmd: git push instead of ide method, see docs file
'''

import subprocess
import urllib.request
import gzip
from Bio import SeqIO



def main():
    cmd1 = 'esearch -db assembly -query Brucella'.split()
    step1 = subprocess.run(cmd1, shell = False, check= False, stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    # print(step1.stdout)
    cmd2 = 'efetch -format docsum'.split()
    step2 = subprocess.run(cmd2, shell = False, check = False, input = step1.stdout ,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # print(step2.stdout)
    cmd3 = 'xtract -pattern DocumentSummary -element FtpPath_RefSeq'.split()
    step3 = subprocess.run(cmd3, shell = False, check = False, input = step2.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    link = (step3.stdout.decode("utf-8"))
    file = open("testfile.txt", "w")
    file.write(link)
    file.close()
    file1 = open("testfile.txt", "r")
    urls = file1.readlines()
    # print(urls)        # print all the links together
    # print(len(urls))   # check the number matches search result with number downloaded
    for i in urls:
        i = (i[:-1])
        print(i)
        download_link = i +'/' + i[55:] +'_genomic.fna.gz'
        print(download_link)
        name = 'data/' + str(i[55:]) +'.genomic.fna.gz'
        print(name)
        urllib.request.urlretrieve(download_link, name)

        






''' for analysis
def main():
    with gzip.open("data/GCF_000022745.1_ASM2274v1.genomic.fna.gz", "rt") as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            identifier = record.id
            description = record.description
            sequence = record.seq
            print(sequence)
            print('Processing the record {}:'.format(identifier))
            print('Its description is: \n{}'.format(description))
            amount_of_nucleotides = len(sequence)
            print('Its sequence contains {} nucleotides.'.format(amount_of_nucleotides))
'''




if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))





# species counts
''' total results:1241
brucella suis: 86
abortus: 334
melitensis: 527
canis: 30
ovis: 17
microti:2
pinnipedalis: 
ceti: 11
inopinata: 4
neotomae: 7
section total: 1018

pseudintermedia: 3
pecoris: 3
haematophila: 2
anthropi: 53
rhizosphaerae: 2
gallinifaecis: 2


anomalous: 42
...
section total: 223

total: 1241
downloaded: 1007
'''


