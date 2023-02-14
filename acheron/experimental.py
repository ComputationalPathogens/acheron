#!usr/bin/env python
import subprocess
# micromamba activate ach.0.8
# cd acheron

# imports
def main():
    cmd1 = 'esearch -db nucleotide -query brucella'.split()
    step1 = subprocess.run(cmd1, shell = False, check= False, stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    cmd2 = 'efilter -mindate 2010 -maxdate 2011 -organism mouse'.split()
    step2 = subprocess.run(cmd2, shell = False, check = False, input = step1.stdout ,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    cmd3 = 'efetch -format fasta'.split()
    step3 = subprocess.run(cmd3, shell = False, check = False, input = step2.stdout,
                           stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(step3.stdout)

# cmd = 'efetch -db biosample -id SAMN00187850 -format fasta'.split()
# subprocess.run(cmd)


if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))



# python experimental.py
# esearch -db pubmed -query "lycopene cyclase" | elink -related | elink -target protein | efilter -organism mouse -source refseq -mindate 2001 -maxdate 2010| efetch -format fasta
#
# esearch -db nucleotide -query "brucella" | efilter -mindate 2010 -maxdate 2011 -organism mouse| efetch -format fasta


