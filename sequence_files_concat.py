#!/usr/bin/env python

import argparse
import re
import sys
import os

import fasta

description = '''Concatenate all found sequences in each provided fasta file.
The order of the concatenation depends on the numerical sort of the input files.
That is, make sure the files you pass in are in the order you want them
concatenated.
Additionally, all fasta files must contain the same amount of sequences.'''

def parse_args():
  parser = argparse.ArgumentParser(
    description=description
  )
  parser.add_argument(
    'fasta_files',
    help='Fasta files to concatenate',
    nargs='+'
  )
  parser.add_argument(
    '--identifier-pattern',
    '-i',
    help='Regex to match each identifier on to create unique identifier. ' \
         'Must contain only one group. [Default: %(default)s]',
    default='(.*)'
  )
  return parser.parse_args()

class InvalidIdentifier(Exception): pass
def extract_identifier(identifier, pattern):
  '''
  >>> extract_identifier('a|a.1', '(\w+\|\w+)\.\d')
  'a|a'
  '''
  m = re.search(pattern, identifier)
  if m is None:
    raise InvalidIdentifier(
      "Identifier {} did not match regular expression {}".format(
        identifier, pattern
      )
    )
  return m.group(1)

class MissingIdentifier(Exception): pass
def concat(files, identifier_pattern):
  '''
  >>> f = ['tests/sequence_concat/{}.fasta'.format(i) for i in range(1,4)]
  >>> concat(f, '(\w+\|\w+)\.\d')
  {'a|a': '123456789', 'b|b': '123456789', 'c|c': '123456789'}
  '''
  # Start the sequences with the first file
  sequences = {
    extract_identifier(_id, identifier_pattern):seq \
    for _id, seq in fasta.read_fasta_file(files[0]).items()
  }
  for _file in files[1:]:
    sys.stderr.write('Concatenating {} onto sequences\n'.format(_file))
    for identifier, sequence in fasta.read_fasta_file(_file).items():
      ident = extract_identifier(identifier, identifier_pattern)
      if ident not in sequences:
        raise MissingIdentifier(
          'Identifier {} was found in {}, but was not present in the first ' \
          'file read.'.format(ident, _file)
        )
      sequences[ident] += sequence
  return sequences

def seq_dict_to_fasta(seq_dict):
  '''
  >>> x = {'a|a': '123456789', 'b|b': '123456789', 'c|c': '123456789'}
  >>> seq_dict_to_fasta(x)
  '>a|a\\n123456789\\n>b|b\\n123456789\\n>c|c\\n123456789'
  '''
  fasta = []
  for identifier, sequence in seq_dict.items():
    fasta.append('>{}'.format(identifier))
    fasta.append('{}'.format(sequence))
  return '\n'.join(fasta)

def natural_sort(filepaths):
  '''
  >>> x = ['a/10.fasta', 'a/1.fasta', 'a/2.fasta']
  >>> natural_sort(x)
  ['a/1.fasta', 'a/2.fasta', 'a/10.fasta']
  >>> x = ['10.fasta', '1.fasta', '2.fasta']
  >>> natural_sort(x)
  ['1.fasta', '2.fasta', '10.fasta']
  '''
  def tryint(s):
      try:
          return int(s)
      except:
          return s
     
  def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

  return sorted(filepaths, key=alphanum_key)

def main():
  args = parse_args()
  fasta_files = natural_sort(args.fasta_files)
  concat_seqs = concat(fasta_files, args.identifier_pattern)
  concat_fasta = seq_dict_to_fasta(concat_seqs)
  sys.stdout.write(concat_fasta)
  sys.stdout.flush()

if __name__ == '__main__':
  main()
