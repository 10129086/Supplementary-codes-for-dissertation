# Supplementary-codes-for-dissertation
## Usage
1. Place all the multiple sequence fasta files to be analysed into a folder named "pancentroids", store the list of Ensembl IDs of the genes that you want to analysis in a txt file , then move them into the “shell” folder.
2. Terminal enter into “shell” folder path.
```cd ./shell```
3. Running Shell script, the parameter is the txt file of the gene list.
```sh program.sh genelist.txt```
## Notice
1. Make sure that the R, BiomaRt in R, Blast, and SNP-sites are all installed and their environment are configured before running the shell.
2. The MUSCLE program (version 3.8) and stable.py are downloaded from [http://www.drive5.com/muscle/muscle_userguide3.8.html]
3. This study uses the fungus - Aspergillus fumigatus A1163 as a reference strain, if your study uses another species or other reference template please change the corresponding parameters in "biomart_get_sequence.r".
4. Given the differences between versions of Python and BLAST, you may need to slightly modify the corresponding commands in the shell to suit your computer. 
