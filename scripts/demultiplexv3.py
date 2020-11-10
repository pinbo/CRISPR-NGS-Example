#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2020 Junli Zhang <zhjl86@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

## This script can be used to demultiplex samples user mixed as one sample
## these samples were preapred with two round PCRs
## 1st round:
# 5’-TCCTCTGTCACGGAAGCG-Your-forward-primer -3’
# 5’-TTTAGCCTCCCCACCGAC-Your-reverse-primer -3
## 2nd round: add barcodes (XXXXXXXX and YYYYYYYY are 8bp barcodes)
# 5’-XXXXXXXXTCCTCTGTCACGGAAGCG -3’
# 5’-YYYYYYYYTTTAGCCTCCCCACCGAC -3
## Then mix them and submit as one sample for NGS sequencing
## The sequencing facility then prepare libraries by adding their sequencing adapters and barcodes
## the comeback results have only our PCR products: 
## XXXXXXXXTCCTCTGTCACGGAAGCG... to 150 bp
## YYYYYYYYTTTAGCCTCCCCACCGAC... to 150 bp

## This script separate samples by XXXXXXXX and YYYYYYYY combinations
## v3: trim barcode and adapters

# import sys
import argparse
# classes
class sample(object):
	def __init__(self):
		self.name = ''
		self.R1 = [] # 4 lines of read1
		self.R2 = [] # 4 lines of read2

# function to process barcode file : 3 columns: sample name, left barcode, right barcode
def get_barcode(infile, barcodeLenToCheck): # barcodeLenToCheck: only use the right barcodeLenToCheck bp to check matches
	barcodes = {} # dictionary for alignment
	with open(infile) as file_one:
		for line in file_one:
			line = line.strip()
			if line:
				name, leftbarcode, rightbarcode = line.split()
				barcodes[leftbarcode[-barcodeLenToCheck:] + "-" + rightbarcode[-barcodeLenToCheck:]] = name
	return barcodes

## arguments
#barcodeFile = sys.argv[1] # 3 columns: sample name, left barcode, right barcode
#fastqFile = sys.argv[2] # fastq file: both R1 and R2 are in the same file next to each other
#usage = "USAGE: %prog -b barcode-file.txt -f interleaved.fastq [OPTIONS] [-h or --help]"
# parser = OptionParser(usage=usage)
# parser.add_option("-b", "--barcode", dest="barcodeFile", default=sys.argv[1], help="Barcode file with 3 columns: barcode number, left barcode, right barcode")
# parser.add_option("-f", "--fastq", dest="fastqFile", default=sys.argv[2], help="An interleaved fastq file including pooled samples")
# parser.add_option("--barcodeLen", "-l", dest="barcodeLenToCheck", type = "int", default=8, help="The right 5bp can already differentiate all the barcodes. This can save some reads missing a few bp on the left")
# parser.add_option("--adapterLen", "-a", dest="adapterLenToCheck", type = "int", default=8, help="The LEFT 8bp are unique enough to find the left or right adapter. This can avoid some sequencing errors.")
# (opt, args) = parser.parse_args()

parser = argparse.ArgumentParser(description="Demultiplex user pooled samples from an interleaved fastq file")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 3.0')
parser.add_argument("barcodeFile", help="Barcode file with 3 columns: barcode number, left barcode, right barcode")
parser.add_argument("fastqFile", help="An interleaved fastq file including pooled samples")
parser.add_argument("-l", "--barcodeLen", dest="barcodeLenToCheck", type = int, default=8, help="The right 5bp can already differentiate all the barcodes. This can save some reads missing a few bp on the left")
parser.add_argument("-a", "--adapterLen", dest="adapterLenToCheck", type = int, default=8, help="The LEFT 8bp are unique enough to find the left or right adapter. This can avoid some sequencing errors.")
parser.add_argument('-t', "--trim",  dest="toTrim", help="whether to trim the 5' barcode and adapters", action="store_true")
args = parser.parse_args()

## demultiplex
# I found the sequencing output sometimes has incomplete barcode.
# The right 5 bps are already unique for the random 8-bp barcodes I designed
# so I only use the right 5 bp here
barcodeLenToCheck = args.barcodeLenToCheck # change here to try different length 5-8
dictBarcode = get_barcode(args.barcodeFile, barcodeLenToCheck)

dictSample = {} # dictionary of sample reads R1 and R2
n1 = 0
n2 = 1
sample_name = ""
leftAdapter  = "TCCTCTGTCACGGAAGCG"[:args.adapterLenToCheck] # random_adapter_F TCCTCTGTCACGGAAGCG
rightAdapter = "TTTAGCCTCCCCACCGAC"[:args.adapterLenToCheck] # random_adapter_R TTTAGCCTCCCCACCGAC
trimLen = 26 # 8 bp barcode + 18 bp adapter

with open(args.fastqFile) as file_one:
	for line in file_one:
		line = line.strip()
		if line.startswith("@") and " " in line: # I found sometimes quality line (the 4th line) also starts with @, but they have no space
		# example: @M02850:171:000000000-J54GV:1:1101:19874:1325 1:N:0:1
			#print(line + "\n")
			sample_name, read = line.split(" ") # read is R1 or R2, here 1:N:0:1
			n1 = 2 # counter of the 4 lines of each read
			if sample_name in dictSample: # should be R2
				dictSample[sample_name].R2 = [line]
				n2 = 2 # now reads are R2
			else:
				ss = sample()
				ss.R1 = [line]
				dictSample[sample_name] = ss
		elif n2 == 1: # input to R1
			dictSample[sample_name].R1.append(line)
			n1 += 1
		elif n2 == 2 and n1 < 4:
			dictSample[sample_name].R2.append(line)
			n1 += 1
		elif n2 == 2 and n1 == 4: # ready to write
			dictSample[sample_name].R2.append(line)
			n2 = 1 # reset to 1
			leftbarcode = ""
			rightbarcode = ""
			R1First20bp = dictSample[sample_name].R1[1][:30] # the first 30 bp of R1
			R2First20bp = dictSample[sample_name].R2[1][:30] # the first 30 bp of R2
			P1 = R1First20bp.find(leftAdapter) # position of the left adpator in R1
			P2 = R2First20bp.find(leftAdapter)
			P3 = R1First20bp.find(rightAdapter)
			P4 = R2First20bp.find(rightAdapter)
			if P1 >= barcodeLenToCheck and P4 >= barcodeLenToCheck: # if there are still at least 5 bp on the left
				leftbarcode = R1First20bp[(P1 - barcodeLenToCheck):P1]
				rightbarcode = R2First20bp[(P4 - barcodeLenToCheck):P4]
			if P2 >= barcodeLenToCheck and P3 >= barcodeLenToCheck:
				leftbarcode = R2First20bp[(P2 - barcodeLenToCheck):P2]
				rightbarcode = R1First20bp[(P3 - barcodeLenToCheck):P3]
				# switch R1 and R2, so R1 always has the left adapter
				dictSample[sample_name].R1, dictSample[sample_name].R2 = dictSample[sample_name].R2, dictSample[sample_name].R1
			barcode = leftbarcode + "-" + rightbarcode
			if barcode in dictBarcode:
				out1 = dictBarcode[barcode] + "_R1_001.fastq"
				out2 = dictBarcode[barcode] + "_R2_001.fastq"
				if args.toTrim:
					dictSample[sample_name].R1[1] = dictSample[sample_name].R1[1][trimLen:]
					dictSample[sample_name].R1[3] = dictSample[sample_name].R1[3][trimLen:]
					dictSample[sample_name].R2[1] = dictSample[sample_name].R2[1][trimLen:]
					dictSample[sample_name].R2[3] = dictSample[sample_name].R2[3][trimLen:]
				outfile1 = open(out1, 'a')
				outfile2 = open(out2, 'a')
				outfile1.write('\n'.join(dictSample[sample_name].R1) + "\n")
				outfile2.write('\n'.join(dictSample[sample_name].R2) + "\n")
				outfile1.close()
				outfile2.close()
			else:
				out = "unassigned.fastq"
				outfile = open(out, 'a')
				outfile.write('\n'.join(dictSample[sample_name].R1 + dictSample[sample_name].R2) + "\n")
				outfile.close()
			del dictSample[sample_name] # delete this entry to save memory

## write all entries kept in dictSample into unassigned.fastq
out = "unassigned2.fastq"
outfile = open(out, 'a')
for sample_name in dictSample:
	outfile.write('\n'.join(dictSample[sample_name].R1 + dictSample[sample_name].R2) + "\n")

outfile.close()
