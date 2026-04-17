FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask scikit-learn pandas numpy matplotlib seaborn werkzeug
EXPOSE 5004
CMD ["python", "app.py"]
