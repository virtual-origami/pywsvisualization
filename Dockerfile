FROM python:3.8.3-slim-buster AS base

# Dedicated Workdir for App
WORKDIR /pywsvisualization

# Do not run as root
RUN useradd -m -r pywsvisualization && \
    chown pywsvisualization /pywsvisualization

COPY requirements.txt /pywsvisualization
RUN pip3 install -r requirements.txt

FROM base AS src
COPY . /pywsvisualization
# install pywsvisualization here as a python package
RUN pip3 install .

USER pywsvisualization

COPY scripts/docker-entrypoint.sh /entrypoint.sh

# Use the `ws-visualization` binary as Application
FROM src AS prod
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["ws-visualization", "-c", "config.yaml"]
