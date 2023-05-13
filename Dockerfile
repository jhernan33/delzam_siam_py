FROM alpine:3.18

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

COPY requirements.txt /requirements.txt

ARG GDAL_VERSION=v2.2.4
ARG LIBKML_VERSION=1.3.0

# RUN apk add --no-cache --virtual .build-deps \
#     ca-certificates gcc postgresql-dev linux-headers musl-dev \
#     libffi-dev jpeg-dev zlib-dev gdal-dev \
#     && apk add --no-cache \
#                --upgrade \
#                --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
#         geos \
#         proj \
#         gdal \
#         binutils \
#     && ln -s /usr/lib/libproj.so.15 /usr/lib/libproj.so \
#     && ln -s /usr/lib/libgdal.so.20 /usr/lib/libgdal.so \
#     && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so \
#     && pip install -r requirements.txt \
#     && find /usr/local \
#         \( -type d -a -name test -o -name tests \) \
#         -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#         -exec rm -rf '{}' + \
#     && runDeps="$( \
#         scanelf --needed --nobanner --recursive /usr/local \
#                 | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#                 | sort -u \
#                 | xargs -r apk info --installed \
#                 | sort -u \
#     )" \
#     && apk add --virtual .rundeps $runDeps 
#     # && apk del .build-deps

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client


# ADD PostGIS here
# POSTGIS dependencies
ENV POSTGIS_VERSION 2.4.4
ENV POSTGIS_SHA256 0dff4902556ad45430e2b85dbe7e9baa758c6eb0bfd5ff6948f478beddd56b67


RUN set -ex \
    \
    && apk add --no-cache --virtual .fetch-deps \
        ca-certificates \
        openssl \
        tar \
    \
    && apk add --no-cache --virtual .build-deps \
        autoconf \
        automake \
        g++ \
        json-c-dev \
        libtool \
        libxml2-dev \
        make \
        perl \
    \
    # add libcrypto from (edge:main) for gdal-2.3.0
    && apk add --no-cache --virtual .crypto-rundeps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        libressl2.7-libcrypto \
    && apk add --no-cache --virtual .build-deps-testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        gdal-dev \
        geos-dev \
        proj4-dev \
        protobuf-c-dev \
    && ./autogen.sh \
# configure options taken from:
  https://anonscm.debian.org/cgit/pkg-grass/postgis.git/tree/debian/rules?h=jessie
    && ./configure \
#       --with-gui \
    && make \
    && make install \
    && apk add --no-cache --virtual .postgis-rundeps \
        json-c \
    && apk add --no-cache --virtual .postgis-rundeps-testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        geos \
        gdal \
        py-gdal \
        proj4 \
        protobuf-c \
    && cd / \
    && rm -rf /usr/src/postgis 
    # \
    # && apk del .fetch-deps .build-deps .build-deps-testing
#  && apk del .fetch-deps .build-deps .build-deps-testing
# END POSTGIS Changes

COPY . /code/
WORKDIR /code

RUN adduser --disabled-password --no-create-home django

USER django

# define the default command to run when starting the container
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8082", "--chdir", "siam", "siam.wsgi:application"]
# CMD ["gunicorn", "--workers=2", "--bind", ":8082", "--chdir", "siam/siam", "siam.wsgi:application"]