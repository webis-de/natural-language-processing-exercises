# Baseline Submission for a Document Processor in the 1st International Workshop on Open Web Search #wows2024

This is a baseline document processor that does some dummy processing by classifying each document as a spam document.

You can run it directly via (please install `tira` via `pip3 install tira`, Docker, and Python >= 3.7 on your machine): 

```
tira-run \
	--input-dataset workshop-on-open-web-search/document-processing-20231027-training \
	--image mam10eks/wows-baselines:doc-processor-0.0.1 \
	--command 'python3 /code/baseline_document_processing.py'
```

## Development

You can build the Docker image via:

```
docker build -t mam10eks/wows-baselines:doc-processor-0.0.1 .
```

To publish the image to dockerhub, run:

```
docker push mam10eks/wows-baselines:doc-processor-0.0.1
```
