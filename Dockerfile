#base image
FROM python:3.11-alpine3.15
#specify the maintainer of the docker file
LABEL maintainer="Marcus"

ENV PYTHONUNBUFFERED 1

#copy application files and dependancies into docker image
COPY ./dependencies.txt /tmp/dependencies.txt
COPY ./dependencies.dev.txt /tmp/dependencies.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

#install packages & dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/dependencies.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/dependencies.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol   && \
    /py/bin/pip freeze

ENV PATH="/py/bin:$PATH"

USER django-user