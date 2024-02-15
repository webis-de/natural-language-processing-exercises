FROM ubuntu:22.04

# Install dependencies
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y python3 python3-pip python-is-python3 openjdk-11-jdk wget \
	&& pip3 install jupyter ir_datasets tira>=0.0.89 \
	&& rm -Rf /var/cache/apt \
	&& rm -Rf /root/.cache/pip

ADD baseline_query_processing.py /code/baseline_query_processing.py

ENTRYPOINT [ "python3", "/code/baseline_query_processing.py" ]

