FROM ubuntu:22.04

# Install dependencies
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y jq libffi-dev python3 python3-pip python-is-python3 openjdk-11-jdk wget \
	&& pip3 install jupyter ir_datasets tira>=0.0.72 \
	&& rm -Rf /var/cache/apt \
	&& rm -Rf /root/.cache/pip

ADD baseline_document_processing.py /code/baseline_document_processing.py

