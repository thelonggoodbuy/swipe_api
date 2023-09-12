# FROM python:3.10-slim-buster

# WORKDIR /usr/src/app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y netcat
# # RUN apk update
# # RUN apk add postgresql-dev gcc python3-dev musl-dev

# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# COPY ./entrypoint.sh .

# RUN echo "Hello World!!"

# RUN sed -i 's/\r$//g' ./entrypoint.sh
# RUN chmod +x ./entrypoint.sh

# COPY . . 

# # ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]



# pull official base image
FROM python:3.10.13-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# copy entrypoint-prod.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]