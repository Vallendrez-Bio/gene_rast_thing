#!/bin/bash

INPUTDIR=$1
OUTPUTDIR=${2:-output_aln}

USAGE="./$0 <input fasta dir> [<output alignment dir>]"
if [[ -z $INPUTDIR ]]; then
  echo $USAGE
  exit 1
fi

function get_cpu_count() {
  echo $(grep processor /proc/cpuinfo | wc -l)
}

mkdir -p ${OUTPUTDIR}
for fasta in ${INPUTDIR}/*.fasta
do
  echo "Aligning $fasta" >&2
  output_fasta=$(basename $fasta)
  output_fasta=${OUTPUTDIR}/${output_fasta/.fasta/.aln.fasta}
  echo $fasta ${output_fasta}
done | xargs -n 2 -P $(get_cpu_count) ./muscle.sh 
