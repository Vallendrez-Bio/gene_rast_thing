# Disclaimer

This is a pretty specific quick script that can be improved if there is interest.

# What do I do?

This program:
1. Compiles and concatenates sequence output from RAST annotation TSV file downloads from any genome annotation project if given a comparison TSV file for each gene.
1. Takes all compiled gene files and aligns them using MUSCLE
1. Concatenates all aligned gene files in order
1. Trims out all columns that contain a gap

# Output

This program outputs a common gene set, aligned and ready for phylogenetic tree construction based on common nucleotide sites across common genes in all isolates.

# Input

1. Genome/isolate annotation TSV or CSV formatted file. Right now the file cannot contain extra tab or commas so if some of the unused columns have tabs or columns in them delete those columns for now(See https://github.com/Vallendrez-Bio/gene_rast_thing/issues/2)
1. Comparison TSV file generated from RAST genome comparison program.
1. Make sure you do not edit the information inside the cells of the TSV files.

Comparison TSV files are generated in RAST when you select the compare genomes option and select your genome contents to compare export the results to a TSV file. The TSV file will start with columns: Contig, Gene, Length, gene id and function for the reference you selected followed by Hit, contig, gene, gene id, percent id and function for each of your isolates.

# Preprocessing steps to facilitate script working

1. Remove the first 4 columns from the RAST comparison file TSV, the Contig, gene, length and gene id for your reference in the RAST TSV comparison output.
1. Make a directory called ```RAST``` where you store all of the individual isolate genome annotation TSV files you download from each project.
1. Ensure you have no missing genes in your comparison TSV. This program is only meant to work with common gene sets among genomes.

## Setup

1. Install Python 3.x version of [miniconda](https://conda.io/miniconda.html)
1. git clone https://github.com/Vallendrez-Bio/gene_rast_thing.git
1. If you do not have git installed, download and unzip the directory

## gene_rast_thing

1. Do gene thing

   Compilation of all gene files given a TSV comparison file and a directory of all annotation files TSV format from RAST. This script relys on default RAST outputs including file names and column inputs so do not change anything from the downloads. The script uses the gene_id column to fine the correct annotation file and then file the correct gene within feature_id of the RAST isolate annotation files.

   ```
   ./gene.py genes.tsv  RAST/*
   ```

1. Align

   Aligns using MUSCLE (https://www.drive5.com/muscle/) at default settings. For right now this script is picky and needs to be in the same directory as your output directory from the previous step. AND since this script calls on the muscle.sh script you will need to make sure the muscle.sh script is also in the same directory as your output directory from the previous step. Don't worry about the fact you don't see muscle.sh in the command below, the script will deal with muscle.

   ```
   ./align.sh output
   ```

   MUSCLE citations: 

   Edgar, R.C. (2004) MUSCLE: multiple sequence alignment with high accuracy and high throughput
  Nucleic Acids Res. 32(5):1792-1797 [Link to PubMed]. 

   Edgar, R.C. (2004) MUSCLE: a multiple sequence alignment method with reduced time and space complexity
  BMC Bioinformatics, (5) 113 [Link to PubMed]. 

1. Rename output files so they sort gooder

   This renames all output alignment files such that they can be sorted using natural order. That is, the files should be named 1.aln.fasta, 2.aln.fasta, 3.aln.fasta where the digit comes from the column in the fasta filename `fig_321327_43_peg_<somedigits>.aln.fasta`.
   *Note*: You need to change the command below to match your data(change the `fig_321327_43` to whatever your sequence names are.
   
   ```
   ls -1 output_aln/* | while read f; do nn=$(echo $f | sed 's|output_aln/fig_321327_43_peg_\([0-9]\+\).aln.fasta|\1.aln.fasta|'); mv $f output_aln/$nn; done
   ```

1. Make big-ass fasta concatenated file

   Takes all of your aligned gene files and concatenates them into one long "common gene set - genome". See the identifer pattern? That's why you cannot deviate from what RAST outputs.

   ```
   ./sequence_files_concat.py --identifier-pattern "(fig\|\d+\.\d+\.peg)" output_aln/* > out.fasta
   ```

1. Trim out all '-' columns

   Removes any site (column) from the entire alignment if it contains a dash.

Remember: This script trashes frame - so don't count of changing anything to amino acids, translation will be incorrect!

   ```
   ./trim_alignment.py out.fasta > out.trim.fasta
   ```
