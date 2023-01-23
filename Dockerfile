FROM python:3.11-alpine as dependencies

ENV DOCKERIZE_VERSION v0.6.1

COPY requirements.txt /opt/app/requirements.txt

RUN apk update && apk add --update --no-cache --progress \
    postgresql-dev \
    bash \
    openssl \
    && apk add --no-cache --virtual=.build-dependencies \
    build-base.py \
    python3-dev \
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r /opt/app/requirements.txt \
    && apk del .build-dependencies \
    && rm -rf \
        /var/cache/apk/* \
        /root/.cache

WORKDIR /opt/app

EXPOSE 8000

COPY . /opt/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


