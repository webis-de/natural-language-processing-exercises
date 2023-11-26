# Snorkel Baseline for The Webpage Classification Task

This is a snorkel baseline for the webpage classification task.

## Run this baseline:

To run this baseline with tira-run, please execute:

```
tira-run --image webis/irixys23:snorkel-baseline --input-dataset webpage-classification/tiny-sample-20231023-training
```


## Development

```
docker build -t webis/irixys23:snorkel-baseline .
docker push webis/irixys23:snorkel-baseline
```

python3 /app/sklearn_baseline.py -i $inputDataset/inputs.jsonl -o $outputDir -m /app/sk_model.pkl
