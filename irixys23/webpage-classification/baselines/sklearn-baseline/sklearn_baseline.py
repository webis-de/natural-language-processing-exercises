#!/usr/bin/env python3
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import os
import joblib
from sklearn_baseline_train import load_data, preprocess

def parse_args():
    parser = argparse.ArgumentParser(description='Webpage classification with sklearn pipeline')
    parser.add_argument("-i", "--input_data", help="Path to the jsonl file for which predictions should be made.", required=True)
    parser.add_argument("-m", "--model", help="The sklearn SGDClassifier model to use for the predictions.", required=True)
    parser.add_argument("-o", "--output", help="Path to the directory to write the results to.", required=True)
    return parser.parse_args()

def load_model(model_file):
    # Load the trained model
    pipeline = joblib.load(model_file)
    return pipeline

def main(input_file, output_dir, model_file):
    # Load datasets
    test_data = load_data(input_file)

    # Preprocess the content
    test_data['url'] = test_data['url'].apply(preprocess)

    # Feature extraction and classifier pipeline
    pipeline = load_model(model_file)
    
    # Make predictions on the test data
    test_predictions = pipeline.predict(test_data['url'])

    # Save the predictions
    test_data['prediction'] = test_predictions
    output_path = os.path.join(output_dir, 'predictions.jsonl')
    test_data[['uid', 'prediction']].to_json(output_path, orient='records', lines=True)

if __name__ == "__main__":
    args = parse_args()
    main(args.input_data, args.output, args.model)
