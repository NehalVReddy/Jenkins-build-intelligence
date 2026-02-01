FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY fetch_and_analyze.py .

CMD ["python", "fetch_and_analyze.py"]
