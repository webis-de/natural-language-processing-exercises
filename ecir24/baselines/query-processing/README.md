# Baseline Submission for a Query Processor in the 1st International Workshop on Open Web Search #wows2024

This is a baseline query processor that appends the query id to each query.

You can run it directly via (please install `tira` via `pip3 install tira`, Docker, and Python >= 3.7 on your machine): 

```
tira-run \
	--input-dataset workshop-on-open-web-search/query-processing-20231027-training \
	--image mam10eks/wows-baselines:query-processor-0.0.1
```

## Development

You can build the Docker image via:

```
docker build -t mam10eks/wows-baselines:query-processor-0.0.1 .
```

To publish the image to dockerhub, run:

```
docker push mam10eks/wows-baselines:query-processor-0.0.1
```
