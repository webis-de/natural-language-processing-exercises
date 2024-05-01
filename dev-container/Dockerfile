# docker build -t fschlatt/natural-language-processing-exercises:0.0.1 .
FROM continuumio/miniconda3

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y git curl wget gcc zip unzip
RUN pip3 install pandas jupyter nltk spacy tira scikit-learn matplotlib
RUN python3 -m nltk.downloader punkt \
	&& python3 -m spacy download en_core_web_sm \
	&& python3 -m nltk.downloader stopwords
