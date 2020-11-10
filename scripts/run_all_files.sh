#!/bin/bash
# 4 arguments: sample number, end sample number, fastq.gz folder, run_aln_v2.sh path, and fasta reference (bwa indexed)
#start=207
#end=224

# for example: ../run_all_files.sh 1 2 ../R1R2/ ../run_aln_v2.sh ../BC_references.fasta


for (( c=$1; c<=$2; c++ ))
do  
   fq1=`echo $3${c}_*R1_001.fastq.gz`
   fq2=`echo $3${c}_*R2_001.fastq.gz`
   # v2 use 'bwa mem'
   sh $4 $5 $fq1 $fq2 out_$c
done
