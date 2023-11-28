![](img/banner.png)

# Code for the Search Engine Prototyping Hackathon at [IRIXYS'23](https://irixys.uni-passau.de/workshops-summer-schools/)

The International Research & Innovation Centre on Digital Intelligent Systems (IRIXYS) hosts a hackathon on Open Web Search from the 28th to 29th of November 2023.

## Homepage

For more information, please visit the [Prototype Search Application (Prosa) homepage](https://qnode.eu/ows/prosa/).

## Task: Build your own conversational Search Engine

This task is very much about creativity. Do you have an innovative idea for a new, exciting search application? The [OpenWebSearch.eu](https://openwebsearch.eu/) initiative encourages all teams to make their ideas come true and work on interesting new concepts around Web Search. The teams will not need to start from scratch, but they can build off of an existing [Prototype Search Application](https://opencode.it4i.eu/openwebsearcheu-public/prototype-search-application). This prototype relies on data provided by the Open Web Index, which makes the Search Application independent from proprietary Web Indices. It is up to your choice whether you want to focus on the search backend, which is implemented in Java, the web frontend or concentrate on the conceptual elaboration. In order open more opportunities for the participants, we additionally provide API endpoints for a Mistral 7b Instruct and Zephyr 7b model for assistant style tasks (suited for Chat Completion) and a Mistral 7b 128k Base model with longer context (suited for General Prompting). For further details, please visit the [LLM API documentation](https://llm-api.pads.fim.uni-passau.de/docs).

## Local Index Creation Pipeline

### Step 1: Perform crawling and create warc file
```
mkdir data
wget --input-file urls.txt --recursive --level 2 --delete-after --no-directories --warc-file data/crawl
```

### Step 2: Extract metadata
```
docker run --rm -v "$PWD/data":/data opencode.it4i.eu:5050/openwebsearcheu-public/preprocessing-pipeline /data/crawl.warc.gz /data/example-index.parquet.gz
```

### Step 3: Create index
```
docker run --rm -v "$PWD/data":/data opencode.it4i.eu:5050/openwebsearcheu-public/spark-indexer --description "CIFF description" --input-format parquet --output-format ciff --id-col record_id --content-col plain_text /data/example- index.parquet.gz /data/index/
```

### Step 4: Convert CIFF file to Lucene index
```
gunzip data/index/index.ciff.gz
docker run --rm -v "$PWD/data":/data opencode.it4i.eu:5050/openwebsearcheu-public/prototype-search-application/ciff- lucene-converter /data/index/index.ciff /data/index/example-index
```

### Step 5: Run the search application
```
docker run --rm -v "$PWD/data":/data -p 8000:8000 opencode.it4i.eu:5050/openwebsearcheu-public/prototype-search- application/search-service -default-index example-index --port 8000 --lucene-dir-path /data/index/ --parquet-dir-path /data/
```
