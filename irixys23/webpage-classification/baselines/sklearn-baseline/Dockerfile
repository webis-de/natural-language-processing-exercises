FROM python:3.9

RUN pip3 install scikit-learn==1.1.1 joblib pandas joblib jsonlines

ENV PYTHONPATH=/app

ADD sklearn_baseline.py  sklearn_baseline_train.py  sk_model.pkl /app/

ENTRYPOINT [ "python3", "/app/sklearn_baseline.py", "-i", "$inputDataset/inputs.jsonl", "-o", "$outputDir", "-m", "/app/sk_model.pkl" ]
