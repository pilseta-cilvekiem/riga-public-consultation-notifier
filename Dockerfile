FROM python:3
ARG EXTRA_PIP_INSTALL_ARGS
ENV TIME_ZONE=Europe/Riga
WORKDIR /app
COPY requirements.txt .
RUN ln --force --symbolic "/usr/share/zoneinfo/$TIME_ZONE" /etc/localtime && echo "$TIME_ZONE" > /etc/timezone
RUN pip install --no-cache-dir --requirement requirements.txt
RUN if [ -n "$EXTRA_PIP_INSTALL_ARGS" ]; then pip install --no-cache-dir $EXTRA_PIP_INSTALL_ARGS; fi
COPY src src
CMD [ "python", "-m", "src" ]
