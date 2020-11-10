#!/bin/bash
# two argument with start sample name and end sample name
#start=207
#end=224

# https://github.com/OpenGene/fastp
# fastp -i ../raw/140_S140_L001_R1_001.fastq.gz -I ../raw/140_S140_L001_R2_001.fastq.gz -o out_140-fail2merge_R1_001.fastq.gz -O out_140-fail2merge_R2_001.fastq.gz -m --merged_out out_140-merged_R1_001.fastq.gz
# v2: add folder: run_fastpv2.sh 1 30../demultiplexed 
# v3: merge all files in the folder

BASEDIR=$(dirname "$0")

samples=$(ls -1 $1/*.gz | cut -d"_" -f1|sort|uniq)

for i in $samples
do  
   #echo $i
   fq1=${i}_R1_001.fastq.gz
   fq2=${i}_R2_001.fastq.gz
   c=$(basename $i)
   # run fastp
   $BASEDIR/fastp -i $fq1 -I $fq2 -o out_$c-fail2merge_R1_001.fastq.gz -O out_$c-fail2merge_R2_001.fastq.gz -m --merged_out out_$c-merged_R1_001.fastq.gz -h out_$c-fastp.html
done
