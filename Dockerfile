FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY governance/ ./governance/

ENV PYTHONPATH=/app
ENV ENV=production

CMD ["python3", "src/agent.py"]
