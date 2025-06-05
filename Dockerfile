FROM python:3.10-slim-bullseye

RUN python -m venv --symlinks /opt/.venv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc && \
    apt-get remove --purge -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lob/apt/lists/*

RUN mkdir -p /opt/app/src /opt/scripts

COPY pyproject.toml /opt/app
COPY ./src /opt/app/src
COPY ./scripts /opt/scripts

RUN chmod +x /opt/scripts/*
RUN /opt/scripts/setup.sh

# ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD [ "/opt/scripts/entrypoint.sh" ]
