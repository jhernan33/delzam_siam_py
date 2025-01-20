# Base image with GDAL and PostGIS support
FROM osgeo/gdal:ubuntu-small-3.6.2 as base

# Install Python and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-wheel python3-setuptools \
    libgdal-dev libpq-dev \
    libjpeg-dev libpng-dev libwebp-dev \
    libxslt1-dev libffi-dev \
    libcairo2-dev libpango1.0-dev \
    zlib1g-dev gcc g++ make \
    build-essential && \
    python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure psycopg2 binary works properly
ENV PIP_NO_BINARY=:none:
ENV PIP_DEFAULT_TIMEOUT=100

# Create working directory
WORKDIR /code

# Copy and install Python dependencies
COPY requirements.txt /code/
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r /code/requirements.txt

# Add application code
COPY . /code/

# Set up Django user
RUN useradd -m django

# Set permissions and switch user
RUN chown -R django:django /code
USER django

# Expose the port Gunicorn will use
EXPOSE 8082

# Run Gunicorn server
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8082", "--chdir", "siam", "siam.wsgi:application"]