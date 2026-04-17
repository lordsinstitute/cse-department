FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask werkzeug

EXPOSE 5005

CMD ["python", "app.py"]
