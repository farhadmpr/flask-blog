FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine


RUN apk update && apk upgrade

RUN apk add --no-cache \
    python3-dev \
    musl-dev \
    openssl-dev \
    libffi-dev \
    make \
    gcc \
    g++ \
    && pip3 install --upgrade pip
    
RUN pip install setuptools

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY ./blog_project /app