from pathlib import Path

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory

if __name__ == "__main__":

    tira = Client()

    # when testing on TIRA, the dataset is automatically replaced by the test dataset
    df = tira.pd.inputs(
        "nlpbuw-fsu-sose-24", "authorship-verification-train-20240408-training"
    )

    prediction = df.set_index("id")["text"].str.contains("delve", case=False)
    prediction.name = "label"
    prediction = prediction.reset_index()
    output_directory = get_output_directory(str(Path(__file__).parent))
    prediction.to_json(
        Path(output_directory) / "predictions.jsonl", orient="records", lines=True
    )
