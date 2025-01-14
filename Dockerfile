# Base image with GDAL and PostGIS support
FROM python:3.10-alpine as base

# Install Python and system dependencies
RUN apk update && apk add --no-cache \
    python3 py3-pip py3-wheel py3-setuptools pango\
    postgresql-dev gdal gdal-dev \
    musl-dev gcc libc-dev linux-headers \
    geos geos-dev \
    libjpeg-turbo-dev libpng-dev libwebp-dev \
    libxslt-dev \
    libffi-dev \
    cairo pango py3-cffi py3-pillow \
    zlib zlib-dev

# Create working directory
WORKDIR /code

# Copy and install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /code/requirements.txt

# Add application code
COPY . /code/

# Crear la carpeta donde estará el archivo de configuración
RUN mkdir -p /code/config/gunicorn

COPY config/gunicorn/conf.py /code/config/gunicorn/conf.py

# Set up Django user
RUN adduser --disabled-password --no-create-home django

# Crear directorio de logs antes de cambiar al usuario 'django'
WORKDIR /code/logs && chown -R django:django /code/logs 

# Set permissions and switch user
RUN chown -R django:django /code
USER django

# Expose the port Gunicorn will use
EXPOSE 8082

# Run Gunicorn server
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8082", "--chdir", "siam", "siam.wsgi:application"]
