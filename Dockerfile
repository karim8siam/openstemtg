FROM python:3.11-slim

WORKDIR /app

# Copy dependency definition
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code and datasets
COPY bot/ bot/
COPY data/ data/

# Use the committed, prebuilt SQLite database. Rebuilding it against existing FTS tables can fail.
RUN test -s data/openstem.db
RUN python3 -m compileall -q bot

CMD ["python3", "bot/main.py"]
