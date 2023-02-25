# MetaMDBG_Manuscript

A collection of scripts and workflows to assess HiFi metagenomics assembly quality.

# Dependencies
- biopython
- metabat2
- checkm

# Circular contigs
Compute the number of circular contigs in an assembly, and their quality with checkM.
```
MetaMDBG:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz mdbg nbCores

Hifiasm_meta:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz hifiasm nbCores

Metaflye:
python3 ./run_singleContigs.py outputDir contigs.fasta.gz assembly_info.txt metaflye nbCores
```

The file outputDir/results.txt contains the results with the following format:
```
Assembly size: 1066556910
N50: 138014
Circular contigs: 18
Single contigs non-circular MAGs: 24 18 16    1 (near-complete, high-quality, medium-quality, contaminated)
Single contigs circular MAGs: 16 2 0    0 (near-complete, high-quality, medium-quality, contaminated)
```

# Non-circular MAGs (binning)
