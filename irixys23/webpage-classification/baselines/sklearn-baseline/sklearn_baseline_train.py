#!/usr/bin/env python3
import argparse
import jsonlines
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import os
import joblib

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
    parser = argparse.ArgumentParser(description='Train a webpage classification model')
    parser.add_argument("-d", "--data_dir", help="Path to the directory containing the data subfolders.", required=True)
    parser.add_argument("-m", "--model_output", help="Path to save the trained model.", required=True)
    return parser.parse_args()

def preprocess(content):
    # Placeholder for the content preprocessing
    return content

def main(data_dir, model_output):
    # Load datasets
    train_data = load_data(os.path.join(data_dir, 'train/D1_train.jsonl'))
    train_labels = load_data(os.path.join(data_dir, 'train/D1_train-truth.jsonl'))['label']

    # Preprocess the content
    train_data['url'] = train_data['url'].apply(preprocess)

    # Feature extraction and classifier pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SGDClassifier())
    ])

    # Train the model
    pipeline.fit(train_data['url'], train_labels)

    # Save the trained model
    joblib.dump(pipeline, model_output)

if __name__ == "__main__":
    args = parse_args()
    main(args.data_dir, args.model_output)
