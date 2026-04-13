FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask scikit-learn pandas numpy matplotlib seaborn werkzeug

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]
