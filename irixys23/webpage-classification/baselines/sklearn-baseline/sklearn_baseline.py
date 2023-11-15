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
    parser.add_argument("-d", "--data_dir", help="Path to the directory containing the data subfolders.", required=True)
    parser.add_argument("-o", "--output", help="Path to the directory to write the results to.", required=True)
    return parser.parse_args()

def preprocess(content):
    # Placeholder for the content preprocessing
    # You might want to add actual preprocessing logic here
    return content

def main(data_dir, output_dir):
    # Load datasets
    train_data = load_data(os.path.join(data_dir, 'train/D1_train.jsonl'))
    train_labels = load_data(os.path.join(data_dir, 'train/D1_train-truth.jsonl'))['label']

    validation_data = load_data(os.path.join(data_dir, 'validation/D1_validation.jsonl'))
    validation_labels = load_data(os.path.join(data_dir, 'validation/D1_validation-truth.jsonl'))['label']

    test_data = load_data(os.path.join(data_dir, 'test/D1_test.jsonl'))

    # Preprocess the content
    train_data['url'] = train_data['url'].apply(preprocess)
    validation_data['url'] = validation_data['url'].apply(preprocess)
    test_data['url'] = test_data['url'].apply(preprocess)

    # Feature extraction and classifier pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SGDClassifier())
    ])

    # Train the model
    pipeline.fit(train_data['url'], train_labels)

    # Validate the model
    validation_predictions = pipeline.predict(validation_data['url'])
    print(classification_report(validation_labels, validation_predictions))

    # Make predictions on the test data
    test_predictions = pipeline.predict(test_data['url'])

    # Save the predictions
    test_data['label'] = test_predictions
    output_path = os.path.join(output_dir, 'test_predictions.jsonl')
    test_data[['uid', 'label']].to_json(output_path, orient='records', lines=True)

if __name__ == "__main__":
    args = parse_args()
    main(args.data_dir, args.output)