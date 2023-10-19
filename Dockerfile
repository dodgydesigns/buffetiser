FROM python:3.11.5-alpine3.18
LABEL maintainer="dodgydesigns@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY ./requirements/requirements-dev.txt /tmp/requirements-dev.txt
COPY ./scripts /scripts
COPY ./buffetiser_api /buffetiser_api
WORKDIR /buffetiser_api
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip  && \
    /py/bin/pip install "psycopg[binary,pool]" && \
    /py/bin/pip install psycopg2-binary
# RUN /py/bin/pip install zlib zlib-dev
# RUN /py/bin/pip install linux-headers
# RUN apk add --update --no-cache postgresql-client && \
#     apk add --update --no-cache --virtual .tmp-build-deps \
#     build-base postgresql-dev musl-dev
RUN apk update  && \
    apk add linux-headers g++ && \
    /py/bin/pip install uwsgi  && \
    apk add --update uwsgi-python  && \
    /py/bin/pip install -r /tmp/requirements.txt
RUN echo $DEV
RUN if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements-dev.txt ; \
    fi
# apk del .tmp-build-deps
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user &&\
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]