FROM python:3.11.5-alpine3.18
LABEL maintainer="dodgydesigns@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./buffetiser_api /buffetiser_api
WORKDIR /buffetiser_api
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip
RUN /py/bin/pip install -r requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r requirements-dev.txt ; \
    fi
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user 

ENV PATH="/py/bin:$PATH"

USER django-user