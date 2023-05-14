FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
RUN mkdir code/staticfiles
RUN mkdir code/mediafiles
WORKDIR /code

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install psycopg2
RUN pip install gunicorn
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh .
ENTRYPOINT [ "sh", "/code/entrypoint.sh" ]