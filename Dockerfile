# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app

RUN apk update && apk upgrade
RUN apk add --no-cache bash\
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

RUN python manage.py collectstatic --noinput 
