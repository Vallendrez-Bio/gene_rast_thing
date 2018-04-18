def read_fasta_file(fasta_file_path):
  '''
  Reads a fasta file and outputs a dictionary where the key is the 
  sequence name and the value is the sequence
  >>> read_fasta_file('tests/sequence_concat/1.fasta')
  {'a|a.1': '123', 'b|b.1': '123', 'c|c.1': '123'}
  '''
  sequences = {}
  lines = []
  fh = open(fasta_file_path, 'r')
  name_line = True
  last_name = ''
  for line in fh:
    if line.startswith('>'):
      last_name = line[1:].strip()
      name_line = True
      sequences[last_name] = ''
    else:
      sequences[last_name] += line.strip()
  return sequences
