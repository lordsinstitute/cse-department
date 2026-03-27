FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python generate_dataset.py && python train_model.py

EXPOSE 5012

CMD ["python", "app.py"]
