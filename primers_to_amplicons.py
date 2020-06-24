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



def group_primers(primers):
    primers_grouped_by_amplicon = {}
    primers_grouped_by_amplicon_and_orientation = {}
    for key, group in itertools.groupby(primers, lambda x: x['amplicon_id']):
        primers_grouped_by_amplicon[key] = list(group)

    for amplicon_id in primers_grouped_by_amplicon.keys():
        primers_grouped_by_amplicon_and_orientation[amplicon_id] = {}
        for key, group in itertools.groupby(primers_grouped_by_amplicon[amplicon_id], lambda x: x['orientation']):
            primers_grouped_by_amplicon_and_orientation[amplicon_id][key] = list(group)

    return primers_grouped_by_amplicon_and_orientation


def pairwise_combinations(grouped_primers):
    all_pairs = []
    for amplicon_id, primers in grouped_primers.items():
        amplicon_pairs = list(itertools.product(primers["LEFT"], primers["RIGHT"]))
        all_pairs.append(amplicon_pairs)

    return all_pairs


def main(args):
    primer_scheme = parse_primer_scheme(args.primer_scheme)
    grouped_primers = group_primers(primer_scheme)
    all_pairs = pairwise_combinations(grouped_primers)

    for amplicon in all_pairs:
        for pair in amplicon:
            if args.inner:
                print('\t'.join([
                    pair[0]['chrom'],
                    str(pair[0]['chromEnd']),
                    str(pair[1]['chromStart']),
                    pair[0]['name'] + '|' + pair[1]['name'],
                    '60',
                    '+'
                ]))
            else:
                print('\t'.join([
                    pair[0]['chrom'],
                    str(pair[0]['chromStart']),
                    str(pair[1]['chromEnd']),
                    pair[0]['name'] + '|' + pair[1]['name'],
                    '60',
                    '+'
                ]))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('primer_scheme')
    parser.add_argument('--inner', action='store_true')
    args = parser.parse_args()

    main(args)
    
