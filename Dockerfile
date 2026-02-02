FROM python:3.10-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy analysis script
COPY fetch_and_analyze.py .

# Output folder (mounted from Jenkins)
VOLUME ["/output"]

# Execute script
CMD ["python", "fetch_and_analyze.py"]
