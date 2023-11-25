#!/usr/bin/env python3
import ir_datasets
import argparse
import json
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description='Create ClueWeb09/ClueWeb12 webpage classification datasets.')
    parser.add_argument("-i", "--input", help="Path to spam rank file.", required=True)
    parser.add_argument("-o", "--output", help="Path to the file where the outputs are to be stored.", required=True)
    parser.add_argument("--dataset-id", help="The id of the ir_dataset.", required=True, choices=['clueweb09', 'clueweb12'])
    return parser.parse_args()


def main(input_file, output_file, ir_datasets_id):
    dataset = ir_datasets.load(ir_datasets_id)
    docs_store = dataset.docs_store()

    with open(input_file, 'r') as inp:
        for line in tqdm(inp):
            spam_rank, doc_id = line.strip().split(' ')
            # From the spam rank documentation: percentile-score<70 is spam, and the rest non-spam.
            label = 'Benign' if int(spam_rank) >= 70 else 'Malicious'

            docs_store.get(doc_id)

if __name__ == '__main__':
    args = parse_args()
    main(args.input, args.output, args.dataset_id)

