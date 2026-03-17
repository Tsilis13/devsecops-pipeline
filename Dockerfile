FROM python:3.9-slim

WORKDIR /app

COPY finalELscenarios.py .

CMD ["python", "finalELscenarios.py"]
