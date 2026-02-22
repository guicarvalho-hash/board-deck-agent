FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY email_monitor.py .
COPY insight_analyzer.py .
COPY insight_store.py .

# Create volume mount points for persistent data
VOLUME ["/app/data"]

# Set environment variables (override with -e or --env-file)
ENV DATA_FILE=/app/data/board_insights.json

# Run the application
CMD ["python", "main.py", "--mode", "continuous"]
