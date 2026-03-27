FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    spacy \
    nltk \
    pandas \
    numpy \
    scikit-learn \
    joblib

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt'); nltk.download('omw-1.4'); nltk.download('punkt_tab')"

# Copy application files
COPY . .

# Initialize DATA.json
RUN echo '{"users": []}' > DATA.json

EXPOSE 5000

CMD python -c "from app import app; import random, string; app.secret_key=''.join(random.choices(string.ascii_uppercase+string.digits,k=10)); app.run(host='0.0.0.0', port=5000)"
