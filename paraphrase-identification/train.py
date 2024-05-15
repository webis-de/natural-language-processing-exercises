from tira.rest_api_client import Client

from levenshtein import levenshtein_distance

if __name__ == "__main__":

    # Load the data
    tira = Client()
    text = tira.pd.inputs(
        "nlpbuw-fsu-sose-24", "paraphrase-identification-train-20240515-training"
    ).set_index("id")
    labels = tira.pd.truths(
        "nlpbuw-fsu-sose-24", "paraphrase-identification-train-20240515-training"
    ).set_index("id")
    text["distance"] = levenshtein_distance(text)
    df = text.join(labels)

    mccs = {}
    for threshold in sorted(text["distance"].unique()):
        tp = df[(df["distance"] <= threshold) & (df["label"] == 1)].shape[0]
        fp = df[(df["distance"] <= threshold) & (df["label"] == 0)].shape[0]
        tn = df[(df["distance"] > threshold) & (df["label"] == 0)].shape[0]
        fn = df[(df["distance"] > threshold) & (df["label"] == 1)].shape[0]
        try:
            mcc = (tp * tn - fp * fn) / (
                (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
            ) ** 0.5
        except ZeroDivisionError:
            mcc = 0
        mccs[threshold] = mcc
    best_threshold = max(mccs, key=mccs.get)
    print(f"Best threshold: {best_threshold}")
