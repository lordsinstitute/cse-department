FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask torch torchvision pillow werkzeug scikit-learn --extra-index-url https://download.pytorch.org/whl/cpu

EXPOSE 5001

CMD ["python", "app.py"]
