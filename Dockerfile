# the base image for the python that we are using for the project
FROM python:3.8.1-alpine

ENV PYHTONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# creating a folder.
RUN mkdir -p /home/user


ENV HOME=/home/user
ENV APP_HOME=/home/user/web

WORKDIR ${APP_HOME}

RUN mkdir ${APP_HOME}/staticfiles
RUN mkdir ${APP_HOME}/media
# RUN mkdir ${APP_HOME}/front
# RUN mkdir ${APP_HOME}/front/build

# COPY ./front/build ${APP_HOME}/front/build


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add zlib zlib-dev jpeg-dev 

RUN apk add --no-cache bash

RUN pip install --upgrade pip

COPY ./requirements.txt ${APP_HOME}/requirements.txt

RUN pip install -r requirements.txt
COPY entrypoint.sh ${APP_HOME}/entrypoint.sh

COPY . ${APP_HOME}

RUN adduser -D user
USER user

ENTRYPOINT [ "/home/user/web/entrypoint.sh" ]
