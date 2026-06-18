FROM python:3
WORKDIR /app

ARG EXTRA_PIP_INSTALL_ARGS
RUN pip install --no-cache-dir \
    beautifulsoup4 \
    requests \
    slack-sdk \
    SQLAlchemy \
    $EXTRA_PIP_INSTALL_ARGS

COPY src src

ENV TZ=Europe/Riga

CMD [ "python", "-m", "src" ]
