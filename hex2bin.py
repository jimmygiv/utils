#!/usr/bin/env python3
from argparse import ArgumentParser
from re import sub,findall
from os import path
from binascii import unhexlify

#Arguments
parser = ArgumentParser()
parser.add_argument("-i", "--in-file", type=str, required=True , help="Source hex file")
parser.add_argument("-o", "--out-file", type=str, required=True, help="Destination binary file")
args = parser.parse_args()

#Sanitize for bad characters\r\n\t\s
def sanitize(text):
  text = sub(r'\r', '', text)
  text = sub(r'\n', '', text)
  text = sub(r'\s', '', text)
  text = sub(r'\t', '', text)
  return text

#Begin
infile = args.in_file
outfile = args.out_file
hexreg = r'[a-zA-Z0-9]{2,}'

if not path.isfile(infile):
  print(f"[!] No such file or directory: {infile}")
  exit()

content = sanitize( open(infile, 'r').read() )

#check hex length
if not len(content) % 2 == 0:
  print("[!] File is not an even amount of characters. Are you sure its hex?")
  exit()
elif not len(findall(hexreg, content)) == 1:
  print("[!] Are you sure this is hex? Non hex characters detected.")
  exit()

try:
  unhex = unhexlify(content)
except:
  print("[!] Unable to convert hex to bin")
  exit()

try:
  open(outfile, 'wb').write(unhex)
except:
  print(f"[!] Unable to write to location: {outfile}")
  exit()
