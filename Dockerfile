FROM python:3.8-alpine3.16

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

COPY requirements.txt /requirements.txt

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

COPY . /code
WORKDIR /code

RUN adduser --disabled-password --no-create-home django

USER django

# define the default command to run when starting the container
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8082", "--chdir", "siam", "siam.wsgi:application"]