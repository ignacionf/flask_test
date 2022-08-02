FROM python:3.9-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt update
RUN apt -y install postgresql-client python3-dev build-essential libpcre2-dev
COPY . /code/
RUN pip install -r /code/requirements.txt

RUN useradd app
USER app

CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]
