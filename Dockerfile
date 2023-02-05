FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
    
RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8082", "--chdir", "api", "api.wsgi:application"]