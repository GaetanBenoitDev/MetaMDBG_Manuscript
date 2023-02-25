# MetaMDBG_Manuscript

A collection of scripts and workflows to assess HiFi metagenomics assembly quality.

# Dependencies
- biopython
- metabat2
- checkm

# Circurlar contigs
Compute the number of circular contigs in an assembly, and their quality with checkM.
'''
MetaMDBG:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz mdbg nbCores

Hifiasm_meta:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz hifiasm nbCores

Metaflye:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz assembly_info.txt metaflye nbCores
'''
