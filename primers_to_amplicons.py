#!/usr/bin/env python

import argparse
import csv
import itertools
import json

from pprint import pprint

def parse_primer_scheme(path_to_primer_scheme):
    primer_scheme = []
    fieldnames = [
        'chrom',
        'chromStart',
        'chromEnd',
        'name',
        'score',
        'strand',
    ]
    with open(path_to_primer_scheme) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='\t')
        for row in reader:
            row['chromStart'] = int(row['chromStart'])
            row['chromEnd'] = int(row['chromEnd'])
            primer_name_split = row['name'].split('_')
            row['amplicon_id'] = '_'.join(primer_name_split[0:2])
            row['amplicon_number'] = int(primer_name_split[1])
            row['orientation'] = primer_name_split[2]
            if len(primer_name_split) > 3:
                row['is_alt'] = True
                row['alt_id'] = primer_name_split[3]
            else:
                row['is_alt'] = False
            primer_scheme.append(row)

    return primer_scheme


def parse_depth(path_to_depth):
    depth = []
    fieldnames = [
        'chrom',
        'position',
        'depth',
    ]
    with open(path_to_depth) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='\t')
        for row in reader:
            row['position'] = int(row['position'])
            row['depth'] = int(row['depth'])
            depth.append(row)

    return depth


def primers_to_amplicons(primers):
    amplicons = []
    grouped_primers = {}
    for key, group in itertools.groupby(primers, lambda x: x['amplicon_id']):
        grouped_primers[key] = list(group)

    for amplicon_id, primers in grouped_primers.items():
        print(amplicon_id, len(primers))
            
    return amplicons

def main(args):
    primer_scheme = parse_primer_scheme(args.primer_scheme)
    depth = parse_depth(args.depth)
    amplicons = primers_to_amplicons(primer_scheme)
    
    # print(json.dumps(primer_scheme))
    # print(json.dumps(depth))
    # print(json.dumps(amplicons))
    #amplicon_depths_1 = [d for d in depth if d['position'] in keyValList]
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='depth')
    parser.add_argument('-p', dest='primer_scheme')
    args = parser.parse_args()

    main(args)
    
