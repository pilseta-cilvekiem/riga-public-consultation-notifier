FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY src src
ENV SECRET_DIR=/run/secrets
CMD [ "python", "-m", "src" ]
