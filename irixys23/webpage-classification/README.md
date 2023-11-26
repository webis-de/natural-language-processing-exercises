# Code for the Webpage Classification Task at [IRIXYS'23](https://irixys.uni-passau.de/workshops-summer-schools/)

The International Research & Innovation Centre on Digital Intelligent Systems (IRIXYS) hosts a hackathon on Open Web Search from the 28th to 29th of November 2023.

## Task

The internet is full of fascinating web pages, but also flooded with spam content. In this task, we want to encourage the teams to separate the righteous from the wicked by applying state-of-the-art ML & NLP techniques. You will work with comprehensive [training and validation datasets](https://doi.org/10.5281/zenodo.10118828) containing URLs and content of benign, malicious and adult pages. The task is therefore to create an accurate Classification model. Note that it is recommended, but not required to use the programming language Python. The concrete software framework, e.g. scikit-learn, snorkel, or transformers, is up to your choice. We particularly encourage the teams to try [snorkel](https://www.snorkel.org/), as its intuitive and rule-based approach on creating Machine Learning models seems promising to achieve good and reproducible results in short time. The teams will use the [TIRA platform](https://github.com/tira-io/tira) for submitting their software solutions and compete with each other on a shared TIRA leaderboard.

## Dataset

The training and validation dataset is available on [Zenodo](https://doi.org/10.5281/zenodo.10118828). Please find a tutorial on Snorkel in the [baselines](baselines) directory, which showcases how to work with the dataset.

## Submission with TIRA

### Setup

Please install `python` (version 3.7 or newer),`tira-run` and `Docker` on your machine.
To install `tira-run`, please use `pip3 install tira`.

### Running the Evaluator

If you have preditions in a file `tira-output/predictions.jsonl`, you can run the evaluator via:

```
tira-run \
	--image webis/irixys23:evaluator \
	--input-directory example-data/truth \
	--input-run ${PWD}/tira-output \
	--output-directory tira-evaluation \
	--command '/evaluation.py -o $outputDir/evaluation.prototext -t $inputDataset/truths.jsonl -p $inputRun/predictions.jsonl'
```

For more details, see the [code of the evaluator](evaluation).

### Running Baselines

You can find the baselines and their code in the [baselines](baselines) directory.

To run the trivial baseline that always predicts `Benign`, please run (the `--evaluate true` flag indicates that the evaluator directly tests if the results of your submission are valid):

```
tira-run \
  --input-dataset webpage-classification/tiny-sample-20231023-training \
  --image webis/irixys23:trivial-baseline \
  --evaluate true \
  --command '/baseline.py -i $inputDataset/inputs.jsonl -o $outputDir/predictions.jsonl'
```
