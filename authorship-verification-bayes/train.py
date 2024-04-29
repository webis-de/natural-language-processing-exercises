from pathlib import Path

from joblib import dump
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from tira.rest_api_client import Client

if __name__ == "__main__":

    # Load the data
    tira = Client()
    text = tira.pd.inputs(
        "nlpbuw-fsu-sose-24", "authorship-verification-train-20240408-training"
    )
    text = text.set_index("id")
    labels = tira.pd.truths(
        "nlpbuw-fsu-sose-24", "authorship-verification-train-20240408-training"
    )
    df = text.join(labels.set_index("id"))

    # Train the model
    model = Pipeline(
        [("vectorizer", CountVectorizer()), ("classifier", MultinomialNB())]
    )
    model.fit(df["text"], df["generated"])

    # Save the model
    dump(model, Path(__file__).parent / "model.joblib")
