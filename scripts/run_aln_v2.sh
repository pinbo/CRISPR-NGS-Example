#!/bin/bash

ref=$1
input_r1=$2
input_r2=$3
output=$4
#adapters=$2

## steps

# 0. trim adapters
#java -jar ../trimmomatic-0.39.jar PE $input_r1  $input_r2  ${input_r1/.fastq/_trimmed.fastq} ${input_r1/.fastq/_trimmed_unparied.fastq} ${input_r2/.fastq/_trimmed.fastq} ${input_r2/.fastq/_trimmed_unparied.fastq} ILLUMINACLIP:$adapters:2:30:10:2:keepBothReads LEADING:3 TRAILING:3 MINLEN:36 SLIDINGWINDOW:4:20


# 1.  build index for the reference
#bwa index $ref

# 2. align reads to reference
#bwa mem $ref  ${input_r1/.fastq/_trimmed.fastq}  ${input_r2/.fastq/_trimmed.fastq} |samtools view -Sb - >${output}.bam
bwa mem $ref $input_r1  $input_r2 |samtools view -Sb - >${output}.bam

# 3. sort bam file
samtools sort ${output}.bam -o ${output}.sorted.bam
rm ${output}.bam

# 4. index sorted bam file
samtools index ${output}.sorted.bam

# 5. view bam file using tview
# samtools tview -p PLATZ-6A-Kronos ${output}.sorted.bam GW2_reference.fas

# check coverage
# samtools depth ILLSINHA13.bam.sorted.bam | less -S
echo $output >> log.txt
samtools depth ${output}.sorted.bam | awk '$3>10' | cut -f1 | sort | uniq >> log.txt
