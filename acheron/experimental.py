#!usr/bin/env python
import subprocess

# micromamba activate ach.0.8
# cd acheron

# imports
'''
def main():
    cmd1 = 'esearch -db genome -query brucella'.split()
    step1 = subprocess.run(cmd1, shell = False, check= False, stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    print(step1.stdout)
    cmd2 = 'efilter -mindate 2010 -organism mouse'.split()
    step2 = subprocess.run(cmd2, shell = False, check = False, input = step1.stdout ,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(step2.stdout)
    cmd3 = 'efetch -format fasta'.split()
    step3 = subprocess.run(cmd3, shell = False, check = False, input = step2.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)

'''

def main():
    cmd1 = 'esearch -db assembly -query Brucella microti'.split()
    step1 = subprocess.run(cmd1, shell = False, check= False, stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    print(step1.stdout)
    cmd2 = 'efetch -format docsum'.split()
    step2 = subprocess.run(cmd2, shell = False, check = False, input = step1.stdout ,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # print(step2.stdout)
    cmd3 = 'xtract -pattern DocumentSummary -element FtpPath_RefSeq'.split()
    step3 = subprocess.run(cmd3, shell = False, check = False, input = step2.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # print(step3.stdout)
    cmd4 = 'awk -F"/" {print $0"/"$NF"_genomic.fna.gz"}  > testfile.txt'.split()
    step4 = subprocess.run(cmd4, shell = False, check = False, input = step3.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    cmd5 = 'wget -i testfile.txt'.split()
    step5 = subprocess.run(cmd5, shell = False, check = False, input = step4.stdout,
                      stdout = subprocess.PIPE, stderr = subprocess.PIPE)




if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))



# python acheron/experimental.py
# esearch -db  -query "lycopene cyclase" | elink -related | elink -target protein | efilter -organism mouse -source refseq -mindate 2001 -maxdate 2010| efetch -format fasta
#
# esearch -db assembly -query "brucella" | efetch -format fasta > testfile.fa
# -db genome: completely closed genomes; ref samples

# esearch -db assembly -query "brucella" | efetch -format fasta

'''
esearch -db assembly -query "Brucella microti" | efilter -mindate 2000 | efetch -format docsum | xtract -pattern DocumentSummary -element FtpPath_RefSeq | awk -F"/" '{print $0"/"$NF"_genomic.fna.gz"}' > testfile.txt
nano testfile.txt
wget -i testfile.txt
'''


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
pecoris: 3
...
section total: 223
'''


