# Trivial Baseline The Webpage Classification Task

This is a trivial baseline for the webpage classification task that always predicts `Benign`.

## Run this baseline:

To run this baseline with tira-run, please execute:

```
tira-run --image webis/irixys23:trivial-baseline --input-dir example-data/input/ --command '/baseline.py -i $inputDataset/inputs.jsonl -o $outputDir/predictions.jsonl'
```

## Development

```
docker build -t webis/irixys23:trivial-baseline .
docker push webis/irixys23:trivial-baseline
```

