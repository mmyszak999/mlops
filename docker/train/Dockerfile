FROM python:3.11-slim

WORKDIR /app

COPY ml/kubernetes/train-requirements.txt .

RUN pip install --no-cache-dir -r train-requirements.txt

COPY ml/__init__.py ./ml/__init__.py
COPY ml/core ./ml/core
COPY ml/kubernetes ./ml/kubernetes

COPY data ./data

CMD ["python", "-m", "ml.kubernetes.train"]