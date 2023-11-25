#!/usr/bin/env python3
import argparse
import jsonlines
import pandas as pd
import joblib
import os
import numpy as np
from snorkel_baseline_train import label_names, ABSTAIN, BENIGN, MALICIOUS, ADULT, get_snorkel_pandas_lf_applier, load_data


def predict_with_tie_break(label_model, L, tie_break_label=BENIGN):
    # Get the probabilistic predictions
    probas = label_model.predict_proba(L)

    # Initialize an array to store the final predictions
    predictions = -1 * np.ones(L.shape[0])

    # Iterate over each item
    for i, prob in enumerate(probas):
        # Find the maximum probability
        max_prob = max(prob)

        # Check if there's a tie
        if (prob == max_prob).sum() > 1:
            # If there's a tie, predict BENIGN
            predictions[i] = tie_break_label
        else:
            # Otherwise, choose the label with the highest probability
            predictions[i] = np.argmax(prob)

    return predictions

def parse_args():
    parser = argparse.ArgumentParser(description='Make predictions using a trained Snorkel labeling model')
    parser.add_argument("-i", "--input_data", help="Path to the JSONL file for making predictions.", required=True)
    parser.add_argument("-m", "--model", help="Path to the trained model.", required=True)
    parser.add_argument("-o", "--output", help="Path to save the predictions.", required=True)
    return parser.parse_args()

def main(input_data, model_path, output_file):
    # Load the test data
    test_data = load_data(input_data)

    # Apply the labeling functions to the test dataset
    applier = get_snorkel_pandas_lf_applier()
    L_test = applier.apply(df=test_data)

    # Load the trained label model
    label_model = joblib.load(model_path)

    # Use the custom prediction function with tie-break handling
    test_predictions = predict_with_tie_break(label_model, L_test)

    # Map numeric labels to string labels
    test_predictions_mapped = [label_names.get(label, 'Unknown') for label in test_predictions]

    # Save the predictions
    test_data['prediction'] = test_predictions_mapped
    test_data[['uid', 'prediction']].to_json(output_file, orient='records', lines=True)

if __name__ == "__main__":
    args = parse_args()
    main(args.input_data, args.model, args.output)
