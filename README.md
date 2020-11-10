# CRISPR-NGS-Example
Example of CRISPR Sequencing analysis

## Scenario

We are using the CRISPR sequencing service at [MGH DNA Core](https://dnacore.mgh.harvard.edu/new-cgi-bin/site/pages/crispr_sequencing_main.jsp). We usually add our own barcodes to pool multiple samples as one sample for submission. Over there, they will add the sequencing adapters and barcodes for Illumina NGS. The returned data is an interleaved fastq file (R1 and R2 are in the same file). Therefore, we need to demultiplex it before checking mutations.

## Steps
1. Demultiplex the interleaved fastq file;
2. Map the fastq files to references to create bam files with `bwa mem`
3. Check bam files in [IGV](http://software.broadinstitute.org/software/igv/).
4. Optional but recommended: using [CRISgo](https://github.com/pinbo/CRISgo) or [CRISjs](https://github.com/pinbo/CRISjs) to check indels in bath mode.
## Requirement
1. [bwa](http://bio-bwa.sourceforge.net/bwa.shtml)
2. [IGV](http://software.broadinstitute.org/software/igv/)
3. [CRISgo](https://github.com/pinbo/CRISgo) or [CRISjs](https://github.com/pinbo/CRISjs)