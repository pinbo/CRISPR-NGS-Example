#!/bin/bash
# 4 arguments: sample number, end sample number, fastq.gz folder, run_aln_v2.sh path, and fasta reference (bwa indexed)
#start=207
#end=224

# for example: ../run_all_files.sh 1 2 ../R1R2/ ../run_aln_v2.sh ../BC_references.fasta

# v2: run all the gz files in a folder, because the names are not numbers
#../run_all_files_v2.sh ../R1R2/ ../run_aln_v2.sh ../BC_references.fasta

samples=$(ls -1 $1/*.gz | cut -d"_" -f1|sort|uniq)

for i in $samples
do  
   #echo $i
   fq1=${i}_R1_001.fastq.gz
   fq2=${i}_R2_001.fastq.gz
   # v2 use 'bwa mem'
   sh $2 $3 $fq1 $fq2 out_$(basename $i)
done
