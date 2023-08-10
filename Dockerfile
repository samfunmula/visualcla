FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

COPY main .

EXPOSE 8000

CMD python3 api.py
