FROM python:3.11-slim

WORKDIR /app

COPY ml/train-requirements.txt .

RUN pip install --no-cache-dir -r train-requirements.txt

COPY ml/train.py .
COPY data ./data

CMD ["python", "train.py"]