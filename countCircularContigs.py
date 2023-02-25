

import os, sys, argparse, shutil, gzip
from Bio.SeqIO.FastaIO import SimpleFastaParser

def main(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("inputFilename", help="contig file")
    parser.add_argument("assembler", help="mdbg, hifiasm, metaflye")
    parser.add_argument("minLength", help="min contig length")
    parser.add_argument("--out", help="output fasta filename")
    
    #parser.add_argument("csv", help="output unitig coverage file (.csv)")
    
    args = parser.parse_args()

    inputFilename = args.inputFilename
    assembler = args.assembler
    minContigLength = int(args.minLength)
    
    outputFile = None
    if args.out:
        outputFile = open(args.out, "w")
    
    nbCircularContigs = 0

    if assembler == "mdbg":
        nbCircularContigs = countHifiasm(inputFilename, minContigLength, outputFile)
    elif assembler == "hifiasm":
        nbCircularContigs = countHifiasm(inputFilename, minContigLength, outputFile)
    elif assembler == "metaflye":
        nbCircularContigs = countMetaflye(inputFilename, minContigLength, outputFile)
    elif assembler == "hicanu":
        nbCircularContigs = countHicanu(inputFilename, minContigLength, outputFile)

    if outputFile: outputFile.close()
    print(nbCircularContigs)


def countHifiasm(inputFilename, minContigLength, outputFile):

    nbCircularContigs = 0
    fileHandle = None

    if(".gz" in inputFilename):
        fileHandle = gzip.open(inputFilename, "rt")
    else:
        fileHandle = open(inputFilename)

    for header, seq in SimpleFastaParser(fileHandle):
        if len(seq) < minContigLength: continue

        if header.endswith("c"):
            nbCircularContigs += 1
            if outputFile:
                outputFile.write(">" + header + "\n")
                outputFile.write(seq + "\n")


    return nbCircularContigs

#seq_name	length	cov.	circ.	repeat	mult.	alt_group	graph_path
#contig_5192	6127306	23	N	N	1	*	5192
def countMetaflye(inputFilename, minContigLength, outputFile):

    nbCircularContigs = 0
    
    fileHandle = open(inputFilename)
    fileHandle.readline() #skip header

    for line in fileHandle:
        line = line.rstrip()
        fields = line.split("\t")

        contigLength = int(fields[1])
        if contigLength < minContigLength: continue

        isCircular = fields[3] == "Y"
        if isCircular:
            nbCircularContigs += 1

    return nbCircularContigs

#>tig00000004 len=37192 reads=21 class=contig suggestRepeat=no suggestBubble=yes suggestCircular=no trim=0-37192
def countHicanu(inputFilename, minContigLength, outputFile):

    nbCircularContigs = 0
    fileHandle = None

    if(".gz" in inputFilename):
        fileHandle = gzip.open(inputFilename, "rt")
    else:
        fileHandle = open(inputFilename)

    for header, seq in SimpleFastaParser(fileHandle):
        if len(seq) < minContigLength: continue

        fields = header.split(" ")
        for field in fields:
            if "suggestCircular" in field:
                yesOrNo = field.split("=")[1]
                if yesOrNo == "yes":
                    nbCircularContigs += 1

    return nbCircularContigs

if __name__ == "__main__":
    main(sys.argv[1:])  
