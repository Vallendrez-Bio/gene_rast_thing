# gene_rast_thing

```
./genes.py genes.tsv index_files/*
```

## Setup

1. Install Python 3.x version of [miniconda](https://conda.io/miniconda.html)
1. Install dependencies

    ```
    conda install bio
    ```

## Shit manual pipeline

1. Do gene thing

   ```
   ./gene.py genes.tsv  RAST/*
   ```

1. Align

   ```
   ./align.sh output
   ```

1. Rename output files so they sort gooder

   ```
   ls -1 output_aln/* | while read f; do nn=$(echo $f | sed 's|output_aln/fig_321327_43_peg_\([0-9]\+\).aln.fasta|\1.aln.fasta|'); mv $f output_aln/$nn; done
   ```

1. Make bigass fasta concatted file

   ```
   ./sequence_files_concat.py --identifier-pattern "(fig\|\d+\.\d+\.peg)" output_aln/* > out.fasta
   ```
