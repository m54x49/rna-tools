#!/usr/bin/env python

"""
Usage::

  $ rna_rosetta_n.py ade.out
  21594

"""

import subprocess
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='ade.out')
    return parser

def get_no_structures(file):
    p = subprocess.Popen('cat ' + file + ' | grep SCORE | wc -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stderr = p.stderr.read().strip()
    if stderr:
        print(stderr)
    return int(p.stdout.read().strip()) - 1

def run():
    """Pipline for modeling RNA"""
    args = get_parser().parse_args()
    ns = get_no_structures(args.file)
    print(ns)

#main
if __name__ == '__main__':
    run()
    
