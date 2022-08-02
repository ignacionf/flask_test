FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=crud
ENV FLASK_DEBUG=1
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/app

WORKDIR /code
RUN apt update
RUN apt -y install postgresql-client python3-dev build-essential libpcre2-dev
COPY . /code/
COPY .env /code/
RUN pip install -r /code/requirements.txt

RUN useradd app
USER app

CMD ["flask", "run", "-h", "0.0.0.0"]
