FROM python:3
ARG EXTRA_PIP_INSTALL_ARGS
RUN RUN ln --symbolic '/usr/share/zoneinfo/${TIME_ZONE}' /etc/localtime && echo '${TIME_ZONE}' > /etc/timezone
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt $EXTRA_PIP_INSTALL_ARGS
COPY src src
CMD [ "python", "-m", "src" ]
