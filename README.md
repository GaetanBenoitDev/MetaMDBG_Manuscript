# MetaMDBG_Manuscript

A collection of scripts and workflows to assess HiFi metagenomics assembly quality.

# Dependencies
- biopython
- metabat2
- checkm
- minimap2 2.24+
- wfmash
- pyani

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

After successful execution, the file outputDir/results.txt contains the results with the following format:
```
Assembly size: 1066556910
N50: 138014
Circular contigs: 18
Single contigs non-circular MAGs: 24 18 16    1 (near-complete, high-quality, medium-quality, contaminated)
Single contigs circular MAGs: 16 2 0    0 (near-complete, high-quality, medium-quality, contaminated)
```

# Non-circular MAGs (binning)
Reconstruct non-circular MAGs using metabat2, and assess their quality with checkM.
```
MetaMDBG:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz contigs.fasta.gz mdbg minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ

Hifiasm_meta:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz contigs.fasta.gz hifiasm minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ

Metaflye:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz assembly_info.txt metaflye minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ
```

After successful execution, the file "outputDir/checkm/\_\_checkm/binScore.csv" contains the results with the following format:
49 41 19    83 (near-complete, high-quality, medium-quality, contaminated)

# Assess assembly completeness and fragmentation with reference sequences
Map contigs to references and compute the number of contigs required to cover at least 99% of the references.

```
python3 ./computeReferenceCompleteness.py referenceFile contigs.fasta.gz contigs.fasta.gz mdbg tmpDir 0.99 nbCores
```
"referenceFile" contains the list of reference filenames, one filename per line.
The result file tmpDir/results.txt provides the following information for each reference:
```
ReferenceName (number of contig of reference): [Assembly status: circular| number of contigs] completeness ANI_with_reference
Staphylococcus_aureus_ATCC_BAA_1556 (1 contigs):  circular 0.9991514199561156 0.999987844786959
```
