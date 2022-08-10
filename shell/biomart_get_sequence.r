library(biomaRt)
args = commandArgs(trailingOnly=TRUE)
genes <- read.table(args[1],head=FALSE)


ensembl_fungi <- useMart(host="https://fungi.ensembl.org",
                         biomart="fungi_mart",
                         dataset = "afumigatusa1163_eg_gene")
  
seq <- getBM(attributes = c('ensembl_gene_id','cdna'),
            filters = 'ensembl_gene_id',
            values = genes, 
            mart = ensembl_fungi)
seq

nrow(seq)
seq[,c(2,1)]


print(args[2])
exportFASTA(seq[,c(2,1)],file=paste(args[2],"/referencegene.fasta",sep = ''))
