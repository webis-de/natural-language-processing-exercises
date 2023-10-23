#!/usr/bin/env python3
import argparse
import json
from sklearn.metrics import f1_score

def read_jsonl_file(file_path: str) -> dict:
    """
    Reads the .jsonl file into a dictionary
    param file_path: path to the .jsonl file
    return: dictionary of UID to value from the file
    """
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            data[item['uid']] = item['prediction']
    return data

def compute_f1_score(predictions: dict, truth: dict) -> float:
    """
    Computes F1 score from the predictions and truth dictionaries
    param predictions: dictionary of UUID to predicted value
    param truth: dictionary of UUID to ground truth value
    return: computed F1 score
    """
    pred_list = [predictions[uuid] for uuid in sorted(predictions.keys())]
    truth_list = [truth[uuid] for uuid in sorted(truth.keys())]
    return f1_score(truth_list, pred_list, average='macro')

def write_output(filename: str, k: str, v: float):
    """
    print() and write the F1 score to the indicated output file
    param filename: full path of the file, where to write to
    param k: the name of the metric
    param v: the value of the metric
    return: None
    """
    line = 'measure{{\n  key: "{}"\n  value: "{}"\n}}\n'.format(k, str(v))
    print(line)
    open(filename, "w").write(line)

def main():
    parser = argparse.ArgumentParser(description='Webpage classification | Evaluation: Compute F1 Score')
    parser.add_argument("-p", "--predictions", help="path to the .jsonl file containing predictions", required=True)
    parser.add_argument("-t", "--truth", help="path to the .jsonl file containing ground truth", required=True)
    parser.add_argument("-o", "--output", help="path to the file to write the results to", required=True)
    args = parser.parse_args()

    # Read JSONL files
    predictions = read_jsonl_file(args.predictions)
    truth = read_jsonl_file(args.truth)

    # Ensure both dictionaries have the same UUIDs
    if set(predictions.keys()) != set(truth.keys()):
        print("Error: Some UUIDs in the Predictions and Truth files don't match.")
        return

    # Compute F1 score
    f1 = compute_f1_score(predictions, truth)
    write_output(args.output, "f1_score", f1)

if __name__ == "__main__":
    main()

