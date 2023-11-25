# Trivial Baseline The Webpage Classification Task

This is a trivial baseline for the webpage classification task that always predicts the passed label (e.g., `Benign` for --prediction Benign).

## Run this baseline:

To run this baseline with tira-run, please execute:

```
tira-run --image webis/irixys23:trivial-baseline --input-dataset webpage-classification/tiny-sample-20231023-training --command '/baseline.py -i $inputDataset/inputs.jsonl -o $outputDir/predictions.jsonl'
```

or, to always predict malicious, please execute:

```
tira-run --image webis/irixys23:trivial-baseline --input-dataset webpage-classification/tiny-sample-20231023-training --command '/baseline.py -i $inputDataset/inputs.jsonl -o $outputDir/predictions.jsonl --prediction Malicious'
```

## Development

```
docker build -t webis/irixys23:trivial-baseline .
docker push webis/irixys23:trivial-baseline
```

