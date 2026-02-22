FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY conversion_data_train.csv conversion_data_train.csv
COPY conversion_data_test.csv conversion_data_test.csv

USER appuser

ENTRYPOINT ["python", "-m", "conversion_rate_mlops.bootstrap.cli"]
