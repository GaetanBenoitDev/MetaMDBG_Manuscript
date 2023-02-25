



import os, sys, argparse, shutil

def main(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("binDir", help="")
    parser.add_argument("outputDir", help="")
    parser.add_argument("nbCores", help="")
    
    args = parser.parse_args()

    binDir = args.binDir
    outputDir = args.outputDir + "/__checkm/"
    nbCores = args.nbCores


    resultFilename = outputDir + "/result.tsv"

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        #shutil.rmtree(outputDir)

        outputFilename = outputDir + "/checkm_results.txt"

        command = "checkm lineage_wf -x fa " + binDir + " " + outputDir + " -t " + str(nbCores) + " --pplacer_threads " + str(nbCores) + " >  " + outputFilename
        print(command)
        os.system(command)

        command = "checkm qa -o 2 --tab_table -f " + resultFilename + " " + outputDir + "/lineage.ms" + " " + outputDir  
        print(command)
        os.system(command)

        outputBinDir = outputDir + "/bins_/"

        completeDir = outputBinDir + "/complete"
        if os.path.exists(completeDir): shutil.rmtree(completeDir)
        os.makedirs(completeDir)

        highDir = outputBinDir + "/high"
        if os.path.exists(highDir): shutil.rmtree(highDir)
        os.makedirs(highDir)

        medDir = outputBinDir + "/med"
        if os.path.exists(medDir): shutil.rmtree(medDir)
        os.makedirs(medDir)

        shutil.rmtree(outputDir + "/bins/")
        shutil.rmtree(outputDir + "/storage/")
        
    else:
        print("Output dir exists!")





    qualityScores = {
        "high": 0,
        "med": 0,
        "low": 0,
        "contaminated": 0,
    }

    f = open(resultFilename)

    #skip header
    f.readline()
    #f.readline()
    #f.readline()


    for line in f:
        line = line.rstrip()
        if line[0] == "-": continue

        fields = line.split("\t")

        binName = fields[0]
        binFilename = binName + ".fa"
        #binFilename = outputDir + "/dereplicated_genomes/" + binName
        #print(binFilename)
        #score = float(fields[1])
        completeness = float(fields[5])
        contamination = float(fields[6])
        strain = float(fields[7])
        strainContamination = contamination * strain/100
        #contamination -= strainContamination

        #print(line)
        #print(fields)
        #print(completeness, contamination, strain)
        
        score = completeness - 5*contamination
        
        #command = ""

        if contamination > 5:
            #command = "ln -s " + binFilename + " " + contaminatedDir + "/" + binName
            qualityScores["contaminated"] += 1
        
        if completeness >= 90 and contamination <= 5:
            #command = "ln -s " + binFilename + " " + completeDir + "/" + binName
            if os.path.exists(binDir + "/" + binFilename): shutil.copy2(binDir + "/" + binFilename, completeDir + "/" + binFilename)
            qualityScores["high"] += 1
        elif completeness >= 70 and contamination <= 10:
            #command = "ln -s " + binFilename + " " + highDir + "/" + binName
            if os.path.exists(binDir + "/" + binFilename):  shutil.copy2(binDir + "/" + binFilename, highDir + "/" + binFilename)
            qualityScores["med"] += 1
        elif score >= 50 and contamination <= 10:
            #command = "ln -s " + binFilename + " " + medDir + "/" + binName
            if os.path.exists(binDir + "/" + binFilename):  shutil.copy2(binDir + "/" + binFilename, medDir + "/" + binFilename)
            qualityScores["low"] += 1

        #if command != "": os.system(command)

    f.close()

    print(qualityScores["high"], qualityScores["med"], qualityScores["low"], "    ", qualityScores["contaminated"])

    f = open(outputDir + "/binScore.csv", "w")
    f.write(str(qualityScores["high"]) + " " + str(qualityScores["med"]) + " " + str(qualityScores["low"])+ "    " + str(qualityScores["contaminated"]))
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])  
