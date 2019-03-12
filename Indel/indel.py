#!/usr/bin/env python
import os, sys
from optparse import OptionParser
import csv
import difflib
from difflib import SequenceMatcher

parser = OptionParser()
parser.add_option("-i", "--ifile", action="store", type="string", dest="input_file", help="File for processing")
parser.add_option("-o", "--ofile", action="store", type="string", dest="output_file", help="File for store result")
parser.add_option("-r", "--reference", action="store", type="string", dest="reference_file", help="DNA sequence as wt for reference")
parser.add_option("-L", "--min_num", action="store", type="int", dest="minimum_number", default="40", help="left border")
parser.add_option("-R", "--max_num", action="store", type="int", dest="maximum_number",  default="50", help="right border")
(options, args) = parser.parse_args()

if not(options.input_file and options.output_file and options.reference_file):
  parser.print_help()
  print 'Example:','\033[1;31mpython indel.py -i input.txt -o output.txt -r GTTTTGGCGGCGACAAATTCGGATCTTGGCTCACTGCAACCTCCGCCTCCCAGGTTCAAGCGATTCTCCTGCCTCAGCCTCCTGGGTAGCTGGGATTATAGGCACCTGCCACCACGCC -L 40 -R 60\033[0m'
  sys.exit(0)

fi = open(options.input_file, 'r')
fo = open(options.output_file, 'w')
wt = options.reference_file[0:120]

lines = csv.reader(fi, delimiter = '\t')

w = []
reads = 0
for line in lines:
  if line[0][0] != 'S':
    reads = reads + int(line[2])
    diff = SequenceMatcher(None, wt, line[0][0:120])
    findsequence = diff.get_matching_blocks()
    i = 0
    c = None
    for s1, s2, s3 in findsequence:
      sd = s2-s1
      if sd != 0:
        a = s1  # a = end, b = start
        b = s2
      if sd ==0 and options.minimum_number < s2 < options.maximum_number:
        c = s1
      i = sd +i

    if i == 0:
      if c:
        s = ['SNP', c, wt[c-1]+'>'+line[0][c-1], line[2]]
      else:
        s = ['wt', ' ', ' ', line[2]]
    if i > 0: 
      s = ['insert', str(a)+'-'+str(b), line[0][a:b], line[2]]
    if i < 0:
      s = ['delete', str(b)+'-'+str(a), wt[b:a], line[2]]
    w.append(s)

num = len(w)

repeat = []
for e in range(0, num):
  r = (w[e][0], w[e][1], w[e][2])
  if r not in repeat:
    repeat.append(r)

j = 1 
seq_sum = [] 
for rset in repeat:
  rnum = 0
  for e in range(0, num):
    r = (w[e][0], w[e][1], w[e][2])
    if r == rset:
      rnum = int(w[e][3])+rnum
  f = (j, rset[0], rset[1], rset[2], rnum , float(rnum)/float(reads), ' ')
  seq_sum.append(f) 
  j += 1


for line in seq_sum:
  if line[1] == 'delete':
    delate_DNA = line[3]
    delate_site = line[2]
    start = int(delate_site.split('-')[0])
    end =   int(delate_site.split('-')[1])
  
    length = len(delate_DNA) 
    if len(wt) - end < length:
      length = len(wt) - end
    right_wt = wt[end:end+length]
    Rnum = 0
    for i in range(0, length):
      if delate_DNA[i] == right_wt[i]:
        Rnum += 1
      else:
        break  
    if Rnum > 0:
      RSH = delate_DNA[0:Rnum]
  

    length = len(delate_DNA)     
    if start < length:
      length = start
    left_wt = wt[start-length:start]  
    Lnum = 0
    for j in range(0, length)[::-1]:
      if delate_DNA[j] == left_wt[j]:
        Lnum = Lnum + 1
      else:
        break
    if Lnum > 0:
      LSH = delate_DNA[length-Lnum:]
    
    if Rnum > 0 and Lnum == 0:
      print >> fo,'%s\t%s\t%s\t%s\t%s\t%s\t%s' % (line[0], line[1], line[2], line[3], line[4], line[5], RSH) 
    
    if Rnum == 0 and Lnum > 0:
      print >> fo,'%s\t%s\t%s\t%s\t%s\t%s\t%s' % (line[0], line[1], line[2], line[3], line[4], line[5], LSH)

    if Rnum > 0 and Lnum > 0:       
      print >> fo,'%s\t%s\t%s\t%s\t%s\t%s\t%s/%s' % (line[0], line[1], line[2], line[3], line[4], line[5], RSH, LSH) 
  
    if Rnum == 0 and Lnum ==0:
      print >> fo,'%s\t%s\t%s\t%s\t%s\t%s\t%s' % (line[0], line[1], line[2], line[3], line[4], line[5], line[6])
    
  else:
      print >> fo,'%s\t%s\t%s\t%s\t%s\t%s\t%s' % (line[0], line[1], line[2], line[3], line[4], line[5], line[6])   

fwt.close()
fi.close()
fo.close()

