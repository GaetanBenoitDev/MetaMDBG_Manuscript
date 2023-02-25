

import os, sys, argparse, shutil, gzip
from Bio.SeqIO.FastaIO import SimpleFastaParser

def main(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("contigs", help="contig file")
    
    #parser.add_argument("csv", help="output unitig coverage file (.csv)")
    
    args = parser.parse_args()

    contigFilename = args.contigs

    if(".gz" in contigFilename):
        fileHandle = gzip.open(contigFilename, "rt")
    else:
        fileHandle = open(contigFilename)

    nbBases = 0

    contigLengths = []
    for header, seq in SimpleFastaParser(fileHandle):
        contigLengths.append(len(seq))

    tmp = []
    for contigLength in set(contigLengths):
        tmp += [contigLength] * contigLengths.count(contigLength) * contigLength

    tmp.sort()

    if len(tmp) % 2 == 0:
        median = (tmp[int(len(tmp)/2) - 1] + tmp[int(len(tmp)/2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]

    print(int(median))

if __name__ == "__main__":
    main(sys.argv[1:])  