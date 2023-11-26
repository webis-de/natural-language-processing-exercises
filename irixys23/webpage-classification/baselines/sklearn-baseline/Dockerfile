FROM python:3.9

ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt \
	&& rm -Rf /var/cache/apt \
	&& rm -Rf /requirements.txt \
	&& rm -Rf /root/.cache/pip

ENV PYTHONPATH=/app

ADD * /app/

ENTRYPOINT [ "python3", "/app/sklearn_baseline.py", "-i", "$inputDataset/inputs.jsonl", "-o", "$outputDir", "-m", "/app/sk_model.pkl" ]
