#!/usr/bin/env python

import argparse
import string
import os

def parse_delimited_file(fh, delimiter='\t', index=False):
  header = [x.strip() for x in fh.readline().split(delimiter)]
  parsed = []
  for line in fh:
    values = [x.strip() for x in line.split(delimiter)]
    z = zip(header, values)
    if index:
      parsed.append(dict(z))
    else:
      parsed.append(list(z))
  return parsed

def normalize_filename(filename):
  for s in string.punctuation:
    filename = filename.replace(s, '_')
  return filename

def fasta_filename(row):
  fasta_filename = None
  for key, value in row:
    if key == 'Gene id':
      return normalize_filename(value) + '.fasta'

class MissingIndexesError(Exception): pass
def rows_to_fasta(rows, sequence_index, output_dir):
  '''
  convert parse_tsv_file rows into fasta by looking up every Gene id
  in sequence_index and grabbing the sequence from there
  Then making a fasta entry similar to
  >{{gene_id}}
  {{sequence}}
  '''
  fasta_fmt = '>{}\n{}'
  missing_indexes = []
  # iterate over every row in genes rows
  for row in rows:
    filename = fasta_filename(row)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as fh:
      # iterate over every column in the row
      for key, value in row:
        if key == 'Gene id':
          if value not in sequence_index:
            missing_indexes.append(value)
            sequence = ''
          else:
            sequence = sequence_index[value]
          fh.write(fasta_fmt.format(value, sequence)+'\n')
  if missing_indexes:
    raise MissingIndexesError('The following identifiers could not be found in any of the index files: {}'.format(missing_indexes))

def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument(
    'gene_file',
    help='File with gene identifiers in it'
  )
  args.add_argument(
    'index_files',
    nargs='+',
    help='File[s] that will generate the sequence index'
  )
  args.add_argument(
    '--output_dir',
    default='output',
    help='Directory to place output files into'
  )
  args.add_argument(
    '--genefile-delimiter',
    default='\t',
    help='Delmiter of gene file[Default: %(default)s]'
  )
  return args.parse_args()

def parse_index_files(files):
  index = {}
  for _file in files:
    with open(_file) as fh:
      for row in parse_delimited_file(fh, index=True):
        index[row['feature_id']] = row['nucleotide_sequence']
  return index

def main():
  args = parse_args()
  if os.path.exists(args.output_dir):
    print("Will not overwrite existing output directory {}".format(args.output_dir))
    return
  os.makedirs(args.output_dir)
  with open(args.gene_file) as fh:
    rows = parse_delimited_file(fh, args.genefile_delimiter)
  sequence_index = parse_index_files(args.index_files)
  rows_to_fasta(rows, sequence_index, args.output_dir)

if __name__ == '__main__':
  main()
