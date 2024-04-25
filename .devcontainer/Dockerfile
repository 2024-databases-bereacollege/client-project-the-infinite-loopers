FROM mcr.microsoft.com/devcontainers/universal:2

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends postgresql-client

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
COPY flaskapp/requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp



