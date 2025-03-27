FROM python:3
ARG EXTRA_PIP_INSTALL_ARGS
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt $EXTRA_PIP_INSTALL_ARGS
COPY src src
ENV SECRET_DIR=/run/secrets
CMD [ "python", "-m", "src" ]
