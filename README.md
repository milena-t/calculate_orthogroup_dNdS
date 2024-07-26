# Introduction

This script contains a workflow that calculates the pairwise dNdS ratios of a single 1-to-1 orthogroup created with Orthofinder wit PAML.

### Quick start
Use `-h` for more info.
```
python3 calculate_orthogroup_dNdS.py \
--orthogroup /path/to/orthofinder/results/Orthogroup_Sequences/OG0006980.fa \
--cds /path/to/dir/cds_complete \
--pal2nalbin /path/to/pal2nal.pl \
--verbose --overwrite
```

## Dependencies

* [Orthofinder](https://github.com/davidemms/OrthoFinder) (The script assumes the file structure of orthofinder output to create the default output directory and to retrieve the gene tree)
* Python3 (libraries: os, subprocess, re, time)
* [BioPython](https://biopython.org/wiki/Download) (specifically SeqIO and AlignIO)
* [Clustal Omega](http://www.clustal.org/omega/) (for the alignment)
* [PAML](http://abacus.gene.ucl.ac.uk/software/paml.html) (the script has yn00 and codeml implemented)
* [pal2nal](https://www.bork.embl.de/pal2nal/) (to make the protein alignment codon-based)
  (Here I allow to give a custom path to the executeable since it wasn't installed in the HPC already. Remember to make the `pal2nal.pl` file executeable!)

Dependencies can be loaded like this on uppmax:
```
module load bioinfo-tools clustalo/1.2.4 biopython/1.80-py3.10.8 paml/4.10.7
```

## Input data

* `--orthogroup`: The orthogroup protein sequence file of a 1-to-1 ortholog generated by orthofinder (in the Orthogroup_Sequences directory)
* `--cds`: nucleotide sequences (for the codon-based alignment), and there are two options here:
    * _Directory_: contains fasta files of all cds (nucleotide sequences!) for each species in your orthogroup. The script then makes a nucleotide fasta file corresponding to the input orthogroup by extracting all cds sequences with matching headers. Therefore, the headers have to match the protein-fasta files from the orthofinder run! Depending on the size of your fasta files this may take a little while.
    * _File_: A nucleotide fasta file containing the nucleotide sequences that correspond to the protein sequences in the orthogroup input.
* `--pal2nalbin`: path to an executeable of pal2nal.

### other options available
* `--verbose`: verbose output, not recommended when you run a bunch of orthogroups.
* `--overwrite`: the script checks for presence of the cds fasta (if `--cds` is a file) and the alignment file, and by default will then use preexisting ones. If you specify overwrite, the script will overwrite preexisting files.
* `--codeml`: The script runs yn00 by default because it's faster and only tries codeml if the output files of yn00 are empty. This option skips yn00 and forces codeml.

also use `--help` for more information.

# Workflow inside the script

1. Prepare input data (set up directories, retrieve relevant files from the orthofinder run, make cds fasta)
2. *Alignment* with clustal omega, all default settings
3. *codon-based conversion* with pal2nal.
     1. Also do some reformatting of the default phylip output of pal2nal to be compatible with paml)
4. *PAML* returns two files ending in .dN and .dS which contain matrices with the pairwise substitution rates between all species
     1. yn00: quick and basic calculation of pairwise dNdS from the codon-based alignment. However, it is less accurate! The [PAML documentation](http://abacus.gene.ucl.ac.uk/software/pamlDOC.pdf) says "_We recommend that you use the ML method (runmode= -2, CodonFreq = 2 in codeml.ctl) as much as possible even for pairwise sequence comparison._".
     2. codeml: this uses the gene tree generated by orthofinder that corresponds to the name of the orthogroup you used and is automatically retrieved from the preexisting orthofinder output directory structure. It also takes 1-3 minutes per orthogroup, so it will drastically increase runtime.
5. Calculate dNdS ratio from the .dN and .dS output files. The dNdS file is also a matrix of all pairwise comparisons in the same format as the .dN and .dS files.

## Running over a list of orthogroups

Orthofinder automatically returns a list of single-copy orthologs (1-to-1 orthologs). The script `calculate_pairwise_dNdS_all_orthogroups.py` contains a function to split this file into many files that can be run in parallel, and also the functionality to run `calculate_orthogroup_dNdS.py` for each orthogroup in an input list passed as a command line argument. Since it is assumed that all these orthogroups are from the same orthofinder run, the path to the orthogroup sequences is hardcoded into `calculate_pairwise_dNdS_all_orthogroups.py` and has to be changed manually before running! The line is highlighted with a comment.






