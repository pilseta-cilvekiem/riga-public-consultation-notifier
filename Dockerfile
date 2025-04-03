FROM python:3
ARG EXTRA_PIP_INSTALL_ARGS
WORKDIR /app
COPY requirements.txt .
RUN ln --force --symbolic "/usr/share/zoneinfo/$TIME_ZONE" /etc/localtime && echo "$TIME_ZONE" > /etc/timezone
RUN pip install --no-cache-dir --requirement requirements.txt $EXTRA_PIP_INSTALL_ARGS
COPY src src
CMD [ "python", "-m", "src" ]
