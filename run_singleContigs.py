

import os, sys, argparse, shutil, subprocess

exeDirName = os.path.dirname(os.path.realpath(__file__))
os.chdir(exeDirName)

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument("outputDir", help="")
    parser.add_argument("contigFilename", help="contig file")
    parser.add_argument("circFile", help="assembly file containing circular information")
    parser.add_argument("assembler", help="mdbg | hifiasm | metaflye")
    #parser.add_argument("minContigLength", help="min contig length")
    parser.add_argument("nbCores", help="")
    
    args = parser.parse_args()

    outputDir = args.outputDir
    contigFilename = args.contigFilename
    circFile = args.circFile
    assembler = args.assembler
    nbCores = int(args.nbCores)
    minContigLength = 1000000

    outputFilename = outputDir + "/results.txt"
    outputDir += "/__results/"

    if os.path.exists(outputDir):
        #os.makedirs(outputDir)
        shutil.rmtree(outputDir)

    os.makedirs(outputDir)

    command = "python3 ./computeAssemblySize.py " + contigFilename
    ret = runCommand(command)
    assemblySize = int(ret)
    print("Assembly size:", assemblySize)
    
    command = "python3 ./computeAssemblyN50.py " + contigFilename
    ret = runCommand(command)
    n50 = int(ret)
    print("N50:", n50)

    command = "python3 ./countCircularContigs.py " + circFile + " " + assembler + " " + str(minContigLength) 
    ret = runCommand(command)
    nbCircularContigs = int(ret)
    print("Circular contigs: ", nbCircularContigs)
    
    command = "python3 ./computeMAG_singleContigs.py " + outputDir + "/mag_singleContigs " + contigFilename + " " + circFile + " " + assembler + " " + str(minContigLength) + " " + str(nbCores) 
    ret = runCommand(command)
    f = open(outputDir + "/mag_singleContigs/__checkmCircularContigs/checkm/__checkm/binScore.csv")
    singleContigs_results = f.readline()
    f.close()
    print("Single contigs MAGs: ", singleContigs_results)

    command = "python3 ./computeMAG_singleContigs.py " + outputDir + "/mag_singleCircularContigs " + contigFilename + " " + circFile + " " + assembler + " " + str(minContigLength) + " " + str(nbCores) + " --circ"
    ret = runCommand(command)
    f = open(outputDir + "/mag_singleCircularContigs/__checkmCircularContigs/checkm/__checkm/binScore.csv")
    singleCircularContigs_results = f.readline()
    f.close()
    print("Single contigs circular MAGs: ", singleCircularContigs_results)

    
    
    outputFile = open(outputFilename, "w")
    
    outputFile.write("Assembly size: " + str(assemblySize) + "\n")
    outputFile.write("N50: " + str(n50) + "\n")
    outputFile.write("Circular contigs: " +  str(nbCircularContigs) + "\n")
    outputFile.write("Single contigs MAGs: " + singleContigs_results + "\n")
    outputFile.write("Single contigs circular MAGs: " + singleCircularContigs_results + "\n")
    outputFile.close()


    print("\n")
    for line in open(outputFilename):
        line = line.rstrip()
        print(line)

def runCommand(command):
    print(command)
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if sp.returncode is not None:
        print("Error")
        sys.exit(1)
    subprocess_return = sp.stdout.read()
    return subprocess_return

if __name__ == "__main__":
    main(sys.argv[1:])  
