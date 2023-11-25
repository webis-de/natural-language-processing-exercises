# Scikit-Learn Baseline for The Webpage Classification Task

This is a scikit-learn baseline for the webpage classification task.

## Run this baseline:

To run this baseline with tira-run, please execute:

```
tira-run --image webis/irixys23:scikit-learn-baseline --input-dataset webpage-classification/tiny-sample-20231023-training
```

## Development

```
docker build -t webis/irixys23:scikit-learn-baseline .
docker push webis/irixys23:scikit-learn-baseline
```

