FROM python:3.10.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

RUN apt-get update

RUN apt-get install poppler-utils -y

ENV FLASK_APP="src/webapp/main.py"

CMD ["gunicorn", "src.webapp.main:app", "--workers", "1", "--timeout", "360"]

