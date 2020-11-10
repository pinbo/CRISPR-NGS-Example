#!/bin/bash
# two argument with start sample name and end sample name
#start=207
#end=224

# https://github.com/OpenGene/fastp
# fastp -i ../raw/140_S140_L001_R1_001.fastq.gz -I ../raw/140_S140_L001_R2_001.fastq.gz -o out_140-fail2merge_R1_001.fastq.gz -O out_140-fail2merge_R2_001.fastq.gz -m --merged_out out_140-merged_R1_001.fastq.gz
# v2: add folder: run_fastpv2.sh 1 30../demultiplexed 

BASEDIR=$(dirname "$0")

for (( c=$1; c<=$2; c++ ))
do  
   fq1=$3/${c}_*R1_001.fastq.gz
   fq2=$3/${c}_*R2_001.fastq.gz
   $BASEDIR/fastp -i $fq1 -I $fq2 -o out_$c-fail2merge_R1_001.fastq.gz -O out_$c-fail2merge_R2_001.fastq.gz -m --merged_out out_$c-merged_R1_001.fastq.gz -h out_$c-fastp.html

done
