#!/usr/bin/env python3
import argparse
from sklearn.metrics import f1_score

def read_txt_file(file_path: str) -> list:
    """
    reads the .txt file into a list
    param file_path: path to the .txt file
    return: list of values from the file
    """
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]

def compute_f1_score(predictions: list, truth: list) -> float:
    """
    Computes F1 score from the predictions and truth lists
    param predictions: list of predicted values
    param truth: list of ground truth values
    return: computed F1 score
    """
    return f1_score(truth, predictions, average='macro')

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
    parser.add_argument("-p", "--predictions", help="path to the .txt file containing predictions", required=True)
    parser.add_argument("-t", "--truth", help="path to the .txt file containing ground truth", required=True)
    parser.add_argument("-o", "--output", help="path to the file to write the results to", required=True)
    args = parser.parse_args()

    # Read TXT files
    predictions = read_txt_file(args.predictions)
    truth = read_txt_file(args.truth)

    # Ensure lengths of both lists are equal
    if len(predictions) != len(truth):
        print("Error: Predictions and Truth files have different lengths.")
        return

    # Compute F1 score
    f1 = compute_f1_score(predictions, truth)
    write_output(args.output, "f1_score", f1)

if __name__ == "__main__":
    main()
