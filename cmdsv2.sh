# looks like they already put R1 and R2 into one file
# but fastp needs two separate files, so I have to seprate R1 and R2
#awk '{if(/1:N:0:1/) {print;n=4;next}; if (n > 1){print; n--}  }' BC001_Plate1_3_322011w_NB1.fastq | gzip > BC001_R1_001.fastq.gz
#awk '{if(/2:N:0:1/) {print;n=4;next}; if (n > 1){print; n--}  }' BC001_Plate1_3_322011w_NB1.fastq | gzip > BC001_R2_001.fastq.gz
#./fastp -i BC001_R1_001.fastq.gz -I BC001_R2_001.fastq.gz -o out-BC001-fail2merge_R1_001.fastq.gz -O out-BC001-fail2merge_R2_001.fastq.gz -m --merged_out out_BC001-merged_R1_001.fastq.gz

## first make a folder to save demultiplexed files
mkdir R1R2
mkdir demultiplexed
cd demultiplexed
time ../scripts/demultiplexv3.py ../sample_barcodes.txt ../qj_id1_crispr_322355w_AB1.fastq
wc -l *
# gzip all the fastq files to save space
gzip *.fastq
mkdir badsamples
mv unassigned* badsamples # and other samples you found
## bwa mapping
cd ..
bwa index references.fasta
mkdir bwa-mem
cd bwa-mem
time ../scripts/run_all_files_v2.sh ../demultiplexed/ ../scripts/run_aln_v2.sh ../references.fasta
# if file names starting with numbers
# ../run_all_files.sh 1 10 ../demultiplexed/ ../run_aln_v2.sh ../references.fasta


# now you can view the bam files with IGV





########### Method 2: use CRISgo
# download CRISgov5: https://github.com/pinbo/CRISgo/
# check CRISgo-cmds.sh
# Now you can also use a webapp:
# https://github.com/pinbo/CRISjs

## merge reads if there are overlap between R1 and R2
# donwload the program fastp first: https://github.com/OpenGene/fastp
mkdir junli-merged
cd junli-merged
../scripts/run_fastpv2.sh 1 32 ../demultiplexed

mkdir junli-merged2
cd junli-merged2

../scripts/run_fastpv3.sh ../demult2

## count lines
for i in *R1_*.gz; do echo $i >> count.txt; zcat $i | wc -l >> count.txt; done







