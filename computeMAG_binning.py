
import os, sys, argparse, time, glob


exeDirName = os.path.dirname(os.path.realpath(__file__))
os.chdir(exeDirName)

def main(argv):
    
    parser = argparse.ArgumentParser()

    #parser.add_argument("read", help="short read file")
    #parser.add_argument("paf", help="input align file")
    parser.add_argument("outputDir", help="output dir")
    parser.add_argument("contigs", help="contigs fasta filename")
    parser.add_argument("circFile", help="assembly file containing circular information")
    parser.add_argument("assembler", help="mdbg | hifiasm | metaflye")
    parser.add_argument("minContigLength", help="min contig length")
    parser.add_argument("nbCores", help="")
    parser.add_argument("reads", nargs='+', help="Read filename(s) (separated by space)")
    parser.add_argument("--circ", help="put circular contigs in their own bin", action="store_true")
    #parser.add_argument("--circ", help="put circular contigs in their own bin")
    #parser.add_argument("--circFile", help="assembly file containing circular information")
    #parser.add_argument("--circAsm", help="mdbg | hifiasm | metaflye")
    #parser.add_argument("--circMinLength", help="minimum contig length for circular contigs")
    
    args = parser.parse_args()

    outputDir = args.outputDir
    contigFilename = args.contigs
    nbCores = int(args.nbCores)

    readFilenames = []
    for path in args.reads:
        readFilenames.append(path)

    if os.path.exists(outputDir):
        print("output dir exists")
        #exit(1)
    else:
        os.makedirs(outputDir)

    isCircularBinning = args.circ
    #circFile = None
    #circAsm = None
    #circMinLength = None
    #if args.circFile:
    #    circFile = args.circFile
    #    circAsm = args.circAsm
    #    circMinLength = args.circMinLength

    #execute_mapping(outputDir, contigFilename, readFilenames, circFile, circAsm, circMinLength, nbCores)

    #def execute_mapping(outputDir, contigFilename, readFilenames, circFile, circAsm, circMinLength, nbCores):

    allJobFilenames = []
    allBamFilename = []
    nbCoresJob = nbCores #int(max(1, nbCores/len(readFilenames)))
    
    for readFilename in readFilenames:#["/mnt/gpfs/gaetan/data/HiFi/AD2W20/AD2W1.fastq.gz", "/mnt/gpfs/gaetan/data/HiFi/AD2W20/AD2W20.fastq.gz", "/mnt/gpfs/gaetan/data/HiFi/AD2W20/AD2W40.fastq.gz"]:


        filename = os.path.basename(readFilename)
        outputFilename = outputDir + "/" + filename + "_mapping.bam"

        command = "nohup python3 ./mapReadsJob.py " + readFilename + " " + contigFilename + " " + outputFilename + " " + str(nbCoresJob)
        allJobFilenames.append(outputFilename + ".done")
        allBamFilename.append(outputFilename)
        #command = "minimap2 -t 1 -ax sr " + contigFilename + " " + shortreads_1 + " " + shortreads_2 + " | samtools sort -o " + outputFilename + " &"
        print(command)


        if os.path.exists(outputFilename + ".done"): continue

        os.system(command)

        #break

    """
    while(True):

        isDone = True

        for filename in allJobFilenames:
            if not os.path.exists(filename):
                isDone = False
                break

        if isDone: break
        time.sleep(1)
    """
    abundance_filename = outputDir + "/depth.txt" 
    
    command = "jgi_summarize_bam_contig_depths --outputDepth " + abundance_filename + " " + outputDir + "/*.bam"
    print(command)
    os.system(command)

    for filename in allBamFilename:
        os.remove(filename)
    for filename in allJobFilenames:
        os.remove(filename)
    
    binDir = outputDir + "/bins/"
    binDirCirular = binDir + "/circular/"
    command = "metabat2 --seed 42 -i " + contigFilename + " -o " + binDir + "/bin" + " -a " + abundance_filename + " -t " + str(nbCores)
    print(command)
    os.system(command)

    if isCircularBinning:

        command = "python3 ./_computeMAG_binning_extractCircularBin.py " + binDir + " " + binDirCirular + " " + args.circFile + " " + args.assembler + " " + args.minContigLength
        print(command)
        os.system(command)

        binDirCirular += "/__binsCircular/"

        command = "python3 ./checkm.py " + binDirCirular + " " + outputDir + "/checkm" + " " + str(nbCores)
        #command = "python3 /mnt/gpfs/gaetan/scripts/annotation/annotation2/drepStats.py " + "\"" + binDir + "/bin*.fa\"" + " " + outputDir + "/drep/"
        print(command)
        os.system(command)
    else:

        command = "python3 ./checkm.py " + binDir + " " + outputDir + "/checkm" + " " + str(nbCores)
        #command = "python3 /mnt/gpfs/gaetan/scripts/annotation/annotation2/drepStats.py " + "\"" + binDir + "/bin*.fa\"" + " " + outputDir + "/drep/"
        print(command)
        os.system(command)

    for binFilename in glob.glob(binDir + "/bin*.fa"):
        os.remove(binFilename)

    if isCircularBinning: 
        for binFilename in glob.glob(binDirCirular + "/bin*.fa"):
            os.remove(binFilename)

if __name__ == "__main__":
    main(sys.argv[1:])  
