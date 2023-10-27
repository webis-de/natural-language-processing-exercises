#!/usr/bin/env python3
# Load a patched ir_datasets that loads the injected data inside the TIRA sandbox
from tira.third_party_integrations import ir_datasets, get_output_directory
from pathlib import Path
import pandas as pd


def process_query(query):
    # Dummy processing of queries: Append the query id to each query.
    return {'qid': query.query_id, 'query': query.default_text() + ' ' + str(query.query_id)}


def process_queries(queries_iter):
    return pd.DataFrame([process_query(i) for i in queries_iter])


if __name__ == '__main__':
    # In the TIRA sandbox, this is the injected ir_dataset, injected via the environment variable TIRA_INPUT_DIRECTORY
    dataset = ir_datasets.load('workshop-on-open-web-search/query-processing-20231027-training')

    # The expected output directory, injected via the environment variable TIRA_OUTPUT_DIRECTORY
    output_dir = get_output_directory('.')
    
    # Query processors persist their results in a file queries.jsonl in the output directory.
    output_file = Path(output_dir) / 'queries.jsonl'
    
    # You can pass as many additional arguments to your program, e.g., via argparse, to modify the behaviour
    
    # process the queries, store results at expected location.
    processed_queries = process_queries(dataset.queries_iter())
    processed_queries.to_json(output_file, lines=True, orient='records')
    
