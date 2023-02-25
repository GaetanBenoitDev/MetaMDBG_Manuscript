



import os, sys, argparse, shutil, glob, gzip
from Bio.SeqIO.FastaIO import SimpleFastaParser


BIN_INDEX = 0
CIRCULAR_BIN_INDEX = 0

def main(argv):

    parser = argparse.ArgumentParser()

    #/mnt/gpfs/gaetan/run/experiments/rust-mdbg/AD_origin/binning/bin*.fa
    parser.add_argument("binDir", help="")
    parser.add_argument("outputDir", help="")
    parser.add_argument("assemblyFilename", help="contig file")
    parser.add_argument("assembler", help="mdbg, hifiasm, metaflye")
    parser.add_argument("minContigLength", help="min contig length")
    
    args = parser.parse_args()

    binDir = args.binDir
    outputDir = args.outputDir + "/__binsCircular"

    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)

    os.makedirs(outputDir)

    circularContigs = collectCircularContigs(args.assembler, args.assemblyFilename, int(args.minContigLength))

    for filename in glob.glob(binDir + "/*.fa"):
        processBin(outputDir, filename, circularContigs)


def processBin(outputDir, filename, circularContigs):

    global BIN_INDEX
    global CIRCULAR_BIN_INDEX

    binFile = None #open(outputDir + "/bin." + str(BIN_INDEX) + ".fa", "w")

    for header, seq in SimpleFastaParser(open(filename)):

        if " " in header:
            header = header.split(" ")[0]

        if header in circularContigs:

            binFileCirc = open(outputDir + "/bin.circ." + str(CIRCULAR_BIN_INDEX) + ".fa", "w")

            binFileCirc.write(">" + header + "\n")
            binFileCirc.write(seq + "\n")

            binFileCirc.close()
            CIRCULAR_BIN_INDEX += 1

        else:

            if binFile is None:
                binFile = open(outputDir + "/bin." + str(BIN_INDEX) + ".fa", "w")

            binFile.write(">" + header + "\n")
            binFile.write(seq + "\n")


    if not (binFile is None):
        binFile.close()
        BIN_INDEX += 1



def collectCircularContigs(assembler, inputFilename, minContigLength):

    circularContigs = {}

    if assembler == "mdbg":
        circularContigs = collectCircularContigs_hifiasm(inputFilename, minContigLength)
    elif assembler == "hifiasm":
        circularContigs = collectCircularContigs_hifiasm(inputFilename, minContigLength)
    elif assembler == "metaflye":
        circularContigs = collectCircularContigs_metaflye(inputFilename, minContigLength)
    elif assembler == "hicanu":
        circularContigs = countHicanu(inputFilename, minContigLength)

    return circularContigs

def collectCircularContigs_hifiasm(inputFilename, minContigLength):

    circularContigs = {}
    fileHandle = None

    if(".gz" in inputFilename):
        fileHandle = gzip.open(inputFilename, "rt")
    else:
        fileHandle = open(inputFilename)

    for header, seq in SimpleFastaParser(fileHandle):
        if header.endswith("c"):
            print(header, len(seq))
        if len(seq) < minContigLength: continue

        if header.endswith("c"):
            circularContigs[header] = True

    return circularContigs

#seq_name	length	cov.	circ.	repeat	mult.	alt_group	graph_path
#contig_5192	6127306	23	N	N	1	*	5192
def collectCircularContigs_metaflye(inputFilename, minContigLength):

    circularContigs = {}
    
    fileHandle = open(inputFilename)
    fileHandle.readline() #skip header

    for line in fileHandle:
        line = line.rstrip()
        fields = line.split("\t")

        header = fields[0]
        contigLength = int(fields[1])
        if contigLength < minContigLength: continue

        isCircular = fields[3] == "Y"
        if isCircular:
            circularContigs[header] = True

    return circularContigs

#>tig00000004 len=37192 reads=21 class=contig suggestRepeat=no suggestBubble=yes suggestCircular=no trim=0-37192
def countHicanu(inputFilename, minContigLength):

    circularContigs = {}

    nbCircularContigs = 0
    fileHandle = None

    if(".gz" in inputFilename):
        fileHandle = gzip.open(inputFilename, "rt")
    else:
        fileHandle = open(inputFilename)

    for header, seq in SimpleFastaParser(fileHandle):
        if len(seq) < minContigLength: continue

        headerShorten = header.split(" ")[0]

        fields = header.split(" ")
        for field in fields:
            if "suggestCircular" in field:
                yesOrNo = field.split("=")[1]
                if yesOrNo == "yes":
                    nbCircularContigs += 1
                    circularContigs[headerShorten] = True

    return circularContigs

if __name__ == "__main__":
    main(sys.argv[1:])  
