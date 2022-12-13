FROM python:3.10

WORKDIR /viggy

ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENV FLASK_APP="src/webapp/main.py"

CMD ["python", "-m", "flask", "run", "--port 5002"]

