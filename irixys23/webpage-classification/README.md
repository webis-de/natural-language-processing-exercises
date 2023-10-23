# Code for the Webpage Classification Task at [IRIXYS'23](https://irixys.uni-passau.de/workshops-summer-schools/)

The International Research & Innovation Centre on Digital Intelligent Systems (IRIXYS) hosts a [hackathon](https://irixys.uni-passau.de/workshops-summer-schools/) on

## Setup

Please install `python` (version 3.7 or newer),`tira-run` and `Docker` on your machine.
To install `tira-run`, please use `pip3 install tira`.

## Running the Evaluator

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

## Running Baselines

You can find the baselines and their code in the [baselines](baselines) directory.

To run the trivial baseline that always predicts `Benign`, please run:

```
tira-run \
	--image webis/irixys23:trivial-baseline \
	--input-dir example-data/input/ \
	--command '/baseline.py -i $inputDataset/inputs.jsonl -o $outputDir/predictions.jsonl'
```

