# docker build -t fschlatt/authorship-verification-naive-bayes:0.0.1 .
FROM fschlatt/natural-language-processing-exercises:0.0.1

ADD run.py /code/run.py
ADD model.joblib /code/model.joblib

ENTRYPOINT [ "python3", "/code/run.py" ]
