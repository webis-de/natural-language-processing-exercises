# The evaluator for the Spam Classification Task at IRIXYS'23

```
tira-run --image webis/irixys23:evaluator-0.0.2 --input-directory example-data/truth --input-run ${PWD}/tira-output --output-directory tira-evaluation --command '/evaluation.py -o $outputDir/evaluation.prototext -t $inputDataset/truths.jsonl -p $inputRun/predictions.jsonl'
```

### Development

```
docker build -t webis/irixys23:evaluator-0.0.2 .
docker push webis/irixys23:evaluator-0.0.2
```

