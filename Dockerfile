FROM python:3
ARG EXTRA_PIP_INSTALL_ARGS
RUN timedatectl set-timezone '${TIME_ZONE}'
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt $EXTRA_PIP_INSTALL_ARGS
COPY src src
CMD [ "python", "-m", "src" ]
