#!/usr/bin/env python3
import argparse
import jsonlines
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import os

def load_data(file_path):
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            obj_keys = obj.keys()
            break
    
    data = {k: [] for k in obj_keys}
    
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            for k in obj_keys:
                data[k].append(obj[k])
    return pd.DataFrame(data)

def parse_args():
    parser = argparse.ArgumentParser(description='Webpage classification with sklearn pipeline')
    parser.add_argument("-i", "--input_data", help="Path to the jsonl file for which predictions should be made.", required=True)
    parser.add_argument("-m", "--model", help="The sklearn SGDClassifier model to use for the predictions.", required=True)
    parser.add_argument("-o", "--output", help="Path to the directory to write the results to.", required=True)
    return parser.parse_args()

def preprocess(content):
    # Placeholder for the content preprocessing
    # You might want to add actual preprocessing logic here
    return content

def load_model(model_file):
    return SGDClassifier()# TODO: Load model here

def main(input_file, output_dir, model_file):
    # Load datasets
    test_data = load_data(input_file)

    # Preprocess the content
    test_data['url'] = test_data['url'].apply(preprocess)

    # Feature extraction and classifier pipeline
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', load_model(model_file))
    ])

    # Make predictions on the test data
    test_predictions = pipeline.predict(test_data['url'])

    # Save the predictions
    test_data['label'] = test_predictions
    output_path = os.path.join(output_dir, 'predictions.jsonl')
    test_data[['uid', 'label']].to_json(output_path, orient='records', lines=True)

if __name__ == "__main__":
    args = parse_args()
    main(args.data_dir, args.output, args.model)
