#see https://github.com/OpenWebSearch/wows-code/tree/main/ecir24/baselines/dev-container
FROM webis/wows-2024-baseline:0.0.5

ADD baseline_query_processing.py /code/baseline_query_processing.py

ENTRYPOINT [ "python3", "/code/baseline_query_processing.py" ]
