#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-21 18:53:14

# Import
import sys
import os
import re

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
Change Japanese filenames of Windows screenshots to English.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("--input-format", metavar="format", default="スクリーンショット\ \([0-9]+\).png", help="format of input-file")
  parser.add_argument("--output-format", metavar="format", default="screenshot_{0:06d}.png", help="format of output-file")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  for file in options.files:
    t = re.search(options.input_format,file)
    if t != None:
      filename = t.group()
      n = re.findall(r'\d+',filename)[0]
      new_filename = options.output_format.format(int(n))
      if os.path.exists(file.replace(filename,new_filename)):
        print("Exit the program because there is an existing file.")
        sys.exit()
      else:
        os.rename(file,file.replace(filename,new_filename))

if __name__ == '__main__':
  main()
