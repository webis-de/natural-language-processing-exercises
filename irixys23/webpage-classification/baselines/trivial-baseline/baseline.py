#!/usr/bin/env python3
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description='Webpage classification baseline')
    parser.add_argument("-i", "--input", help="Path to the .jsonl file containing the inputs.", required=True)
    parser.add_argument("-o", "--output", help="Path to the file to write the results to.", required=True)
    parser.add_argument("-p", "--prediction", help="The to-be-predicted label. This classifier always predicts the passed label", choices=["Adult", "Benign", "Malicious"], default="Benign")
    return parser.parse_args()


def predict_class(web_page, prediction):
    # In reality, here would come the interesting part.
    # But in this baseline, we just return the label passed via --prediction
    return prediction


def main(input_file, output_file, prediction):
    with open(input_file, 'r') as inp, open(output_file, 'w+') as outp:
        for l in inp:
            l = json.loads(l)
            output = {'uid': l['uid'], 'prediction': predict_class(l, prediction)}
            outp.write(json.dumps(output) + '\n')


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output, args.prediction)

