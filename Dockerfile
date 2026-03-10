FROM python:3
WORKDIR /app

ENV TIME_ZONE=Europe/Riga
RUN ln -fs "/usr/share/zoneinfo/$TIME_ZONE" /etc/localtime && echo "$TIME_ZONE" > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG EXTRA_PIP_INSTALL_ARGS
RUN if [ -n "$EXTRA_PIP_INSTALL_ARGS" ]; then pip install --no-cache-dir $EXTRA_PIP_INSTALL_ARGS; fi

COPY src src

CMD [ "python", "-m", "src" ]
