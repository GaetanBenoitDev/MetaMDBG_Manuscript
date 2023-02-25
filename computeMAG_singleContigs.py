



import os, sys, argparse, shutil, glob, gzip
from Bio.SeqIO.FastaIO import SimpleFastaParser


BIN_INDEX = 0

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument("outputDir", help="")
    parser.add_argument("assemblyFilename", help="contig file")
    parser.add_argument("circFile", help="assembly file containing circular information")
    parser.add_argument("assembler", help="mdbg | hifiasm | metaflye")
    parser.add_argument("minContigLength", help="min contig length")
    parser.add_argument("nbCores", help="")
    parser.add_argument("--circ", help="circular contig only", action='store_true')
    
    args = parser.parse_args()

    outputDir = args.outputDir + "/__checkmCircularContigs/"
    nbCores = int(args.nbCores)

    circularContigOnly = False
    if args.circ:
        circularContigOnly = True

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        #shutil.rmtree(outputDir)

    #os.makedirs(outputDir)

    binDir = outputDir + "/bins/"
    if not os.path.exists(binDir):
        os.makedirs(binDir)
    
    circularContigs = collectContigs(args.assembler, args.circFile, int(args.minContigLength), circularContigOnly)
    processContigs(binDir, args.assemblyFilename, circularContigs)

    command = "python3 ./checkm.py " + binDir + " " + outputDir + "/checkm" + " " + str(nbCores)
    print(command)
    ret = os.system(command)
    if(ret != 0): sys.exit(1)

    shutil.rmtree(binDir)

    #f = open(outputDir + "/checkm/__checkm/binScore.csv")
    #print(f.readlines())
    #f.close()

def processContigs(binDir, contigFilename, circularContigs):

    global BIN_INDEX

    fileHandle = None
    if(".gz" in contigFilename):
        fileHandle = gzip.open(contigFilename, "rt")
    else:
        fileHandle = open(contigFilename)

    for header, seq in SimpleFastaParser(fileHandle):

        if " " in header:
            header = header.split(" ")[0]

        if header in circularContigs:

            binFileCirc = open(binDir + "/bin.circ." + str(BIN_INDEX) + ".fa", "w")

            binFileCirc.write(">" + header + "\n")
            binFileCirc.write(seq + "\n")

            binFileCirc.close()
            BIN_INDEX += 1



def collectContigs(assembler, inputFilename, minContigLength, circularContigOnly):

    circularContigs = {}

    if assembler == "mdbg":
        circularContigs = collectCircularContigs_hifiasm(inputFilename, minContigLength, circularContigOnly)
    elif assembler == "hifiasm":
        circularContigs = collectCircularContigs_hifiasm(inputFilename, minContigLength, circularContigOnly)
    elif assembler == "metaflye":
        circularContigs = collectCircularContigs_metaflye(inputFilename, minContigLength, circularContigOnly)
    elif assembler == "hicanu":
        circularContigs = countHicanu(inputFilename, minContigLength, circularContigOnly)

    return circularContigs

def collectCircularContigs_hifiasm(inputFilename, minContigLength, circularContigOnly):

    circularContigs = {}
    fileHandle = None

    if(".gz" in inputFilename):
        fileHandle = gzip.open(inputFilename, "rt")
    else:
        fileHandle = open(inputFilename)

    for header, seq in SimpleFastaParser(fileHandle):
        if len(seq) < minContigLength: continue

        if circularContigOnly:
            if header.endswith("c"):
                circularContigs[header] = True
        else:
            circularContigs[header] = True


    return circularContigs

#seq_name	length	cov.	circ.	repeat	mult.	alt_group	graph_path
#contig_5192	6127306	23	N	N	1	*	5192
def collectCircularContigs_metaflye(inputFilename, minContigLength, circularContigOnly):

    circularContigs = {}
    
    fileHandle = open(inputFilename)
    fileHandle.readline() #skip header

    for line in fileHandle:
        line = line.rstrip()
        fields = line.split("\t")

        header = fields[0]
        contigLength = int(fields[1])
        if contigLength < minContigLength: continue


        if circularContigOnly:
            isCircular = fields[3] == "Y"
            if isCircular:
                circularContigs[header] = True
        else:
            circularContigs[header] = True

    return circularContigs

#>tig00000004 len=37192 reads=21 class=contig suggestRepeat=no suggestBubble=yes suggestCircular=no trim=0-37192
def countHicanu(inputFilename, minContigLength, circularContigOnly):

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

        if circularContigOnly:
            fields = header.split(" ")
            for field in fields:
                if "suggestCircular" in field:
                    yesOrNo = field.split("=")[1]
                    if yesOrNo == "yes":
                        nbCircularContigs += 1
                        circularContigs[headerShorten] = True
        else:
            circularContigs[headerShorten] = True

    return circularContigs

if __name__ == "__main__":
    main(sys.argv[1:])  
