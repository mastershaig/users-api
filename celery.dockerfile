FROM python:3.7-buster

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code
ENV DEBUG False

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# create working directory
RUN mkdir /code;

# make a working directory
WORKDIR ${APP_ROOT}

## Copy in your requirements file
RUN mkdir /config
## Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
ADD requirements.txt /config/
## Install all dependencies to python virtualenviroment
RUN python -m venv /venv
RUN /venv/bin/pip install -U pip
RUN /venv/bin/pip install --no-cache-dir -r /config/requirements.txt

# Copy all staf to working directory
ADD . ${APP_ROOT}
