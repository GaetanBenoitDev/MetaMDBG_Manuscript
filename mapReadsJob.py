

import os, sys, argparse


def main(argv):
    
    parser = argparse.ArgumentParser()

    #parser.add_argument("read", help="short read file")
    #parser.add_argument("paf", help="input align file")
    parser.add_argument("reads", help="output dir")
    parser.add_argument("contigs", help="contigs fasta filename")
    parser.add_argument("outputFilename", help="")
    parser.add_argument("nbCores", help="")
    
    args = parser.parse_args()

    nbCores = int(args.nbCores)

    jobDoneFilename = args.outputFilename + ".done"
    if os.path.exists(jobDoneFilename): os.remove(jobDoneFilename)

    #execute_mapping(args.reads, args.contigs, args.outputFilename, jobDoneFilename)

    # execute_mapping(readFilename, contigFilename, outputFilename, jobDoneFilename):

    #command = "minimap2 -t 1 -ax sr " + contigFilename + " " + shortreads_1 + " " + shortreads_2 + " | samtools sort -o " + outputFilename
    command = "minimap2 -t " + str(nbCores) + " -ak19 -w10 -I10G -g5k -r2k --lj-min-ratio 0.5 -A2 -B5 -O5,56 -E4,1 -z400,50 " + args.contigs + " " + args.reads + " | samtools sort -@ " + str(nbCores) + " -o " + args.outputFilename
    
    print(command)
    os.system(command)
    
    f = open(jobDoneFilename, "w")
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])  
