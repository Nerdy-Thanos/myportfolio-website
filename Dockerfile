
FROM python:3.10.8-slim-buster


ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY . .

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV FLASK_APP="src/webapp/main.py"

CMD ["gunicorn", "src.webapp.main:app", "--workers", "1", "--timeout", "360"]

