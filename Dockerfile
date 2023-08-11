FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY setup.py .

RUN apt update

RUN pip install --no-cache-dir -r requirements.txt

COPY main .

COPY models .

EXPOSE 8000

CMD python3 api.py
