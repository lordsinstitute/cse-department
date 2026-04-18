FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask scikit-learn pandas numpy matplotlib seaborn joblib werkzeug nltk

RUN python -c "import nltk; nltk.download('stopwords', quiet=True)"

COPY . .

RUN python generate_dataset.py && python train_model.py

EXPOSE 5007

CMD ["python", "-c", "from app import app; app.run(host='0.0.0.0', port=5007)"]
