
FROM nvcr.io/nvidia/driver

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl

FROM nvcr.io/nvidia/cuda

CMD nvidia-smi

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl


FROM python:3.10.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY . .

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV FLASK_APP="src/webapp/main.py"

CMD ["gunicorn", "src.webapp.main:app", "--workers", "1", "--timeout", "360"]

