#!/usr/bin/env python3
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description='Webpage classification baseline')
    parser.add_argument("-i", "--input", help="Path to the .jsonl file containing the inputs.", required=True)
    parser.add_argument("-o", "--output", help="Path to the file to write the results to.", required=True)
    return parser.parse_args()


def predict_class(web_page):
    return 'Benign'


def main(input_file, output_file):
    with open(input_file, 'r') as inp, open(output_file, 'w+') as outp:
        for l in inp:
            l = json.loads(l)
            output = {'uid': l['uid'], 'prediction': predict_class(l)}
            outp.write(json.dumps(output) + '\n')


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)

