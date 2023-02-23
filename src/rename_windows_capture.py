#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-21 18:53:14

# Import
import os
import re

dic = {
        "エクスプローラー":"Explorer"  
      }

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
Change Japanese filenames of Windows capture to English.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("--format", metavar="format", default="[0-9]+_[0-9]+_[0-9]+\ [0-9]+_[0-9]+_[0-9]", help="format of input-file without first halg and extension")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  for file in options.files:
    t = re.search(options.format,file)
    if t != None:
      base = os.path.basename(file)
      for i in dic.keys():
        if i in base:
          base = base.replace(i,dic[i])
      new_filename=""
      for w in list(base):
        if w == " ":
          new_filename += "_"
        if w in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_.0123456789":
          new_filename += w
      while True:
        for b,a in zip(["_-","-_","__","--"],["-","-","_","-"]):
          if b in new_filename:
            new_filename = new_filename.replace(b,a)
            break
        else:
          break
      while True:
        if new_filename[0] in "-_":
          new_filename = new_filename[1:]
        else:
          break
      if os.path.exists(os.path.join(os.path.dirname(file),new_filename)):
        print(f"Skip `{file}` because there is an existing file.")
        continue
      else:
        os.rename(file,os.path.join(os.path.dirname(file),new_filename))

if __name__ == '__main__':
  main()
