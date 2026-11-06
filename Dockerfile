FROM python:3.11-slim

WORKDIR /app

# Copy dependency definition
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code and datasets
COPY bot/ bot/
COPY data/ data/

# Ensure DB is populated
RUN python3 bot/db.py

CMD ["python3", "bot/main.py"]
