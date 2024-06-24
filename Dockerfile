FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /memes_app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV USE_DOCKER=1

COPY . .

CMD ["python3", "main.py"]
