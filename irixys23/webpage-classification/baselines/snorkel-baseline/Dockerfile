FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt \
	&& rm -Rf /var/cache/apt \
	&& rm -Rf /requirements.txt \
	&& rm -Rf /root/.cache/pip

ENV PYTHONPATH=/app

ADD * /app/

ENTRYPOINT [ "python3", "/app/snorkel_baseline.py", "-i", "$inputDataset/inputs.jsonl", "-o", "$outputDir/predictions.jsonl", "-m", "/app/snrkl_model.pkl" ]

