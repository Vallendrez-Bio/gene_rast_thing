#!/usr/bin/env python

import argparse
import sys

import fasta

description = '''Finds columns where any of the sequences contain any of the
given characters and removes those columns from all sequences'''

def parse_args():
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument(
    'alignment_fasta',
    help='Fasta alignment file to trim'
  )
  parser.add_argument(
    '--character',
    '-c',
    help='If any of these characters exist in a column, remove that entire' \
         ' column. [Default: %(default)s]',
    nargs='+',
    default=['-']
  )
  return parser.parse_args()

def trim_indexes(seq_dict, trim_characters):
  '''
  >>> d = {'a': '12345', 'b': '12345', 'c': '12345'}
  >>> x = trim_indexes(d, ['3', '5'])
  >>> sorted(list(x))
  [2, 4]
  '''
  # Will contain all columns that need to be removed
  trim_indexes = set()
  for seq in seq_dict.values():
    for index, value in enumerate(seq):
      if value in trim_characters:
        trim_indexes.add(index)
  return trim_indexes

def trim_sequences(seq_dict, trim_characters):
  '''
  >>> d = {'a': '12345', 'b': '12345', 'c': '12345'}
  >>> trim_sequences(d, ['3', '5'])
  {'a': '124', 'b': '124', 'c': '124'}
  '''
  _trim_indexes = trim_indexes(seq_dict, trim_characters)
  sys.stderr.write('Trimming {} columns'.format(len(_trim_indexes)))
  for ident, sequence in seq_dict.items():
    trimmed_sequence = []
    for i, value in enumerate(sequence):
      if i not in _trim_indexes:
        trimmed_sequence.append(value)
    seq_dict[ident] = ''.join(trimmed_sequence)
  return seq_dict

def main():
  args = parse_args()
  seqs = fasta.read_fasta_file(args.alignment_fasta)
  trimmed_seqs = trim_sequences(seqs, args.character)
  sys.stdout.write(fasta.seq_dict_to_fasta(trimmed_seqs))
  sys.stdout.flush()

if __name__ == '__main__':
  main()
