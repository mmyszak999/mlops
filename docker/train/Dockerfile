FROM python:3.11-slim

WORKDIR /app

COPY ml/kubernetes/train-requirements.txt .

RUN pip install --no-cache-dir -r train-requirements.txt

COPY ml/kubernetes/train.py .
COPY data ./data

CMD ["python", "train.py"]