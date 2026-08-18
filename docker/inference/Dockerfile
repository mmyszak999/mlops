FROM python:3.11-slim

WORKDIR /app

COPY ml/kubernetes/inference-requirements.txt .

RUN pip install --no-cache-dir -r inference-requirements.txt

COPY ml/kubernetes/predict.py .

EXPOSE 8080

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8080"]