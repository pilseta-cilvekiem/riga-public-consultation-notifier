FROM python:3

RUN apt-get update && apt-get install --no-install-recommends -y sudo
RUN pip install --no-cache-dir \
    beautifulsoup4 \
    requests \
    slack-sdk \
    SQLAlchemy

RUN useradd -m -s /bin/bash notifier
COPY --chmod=440 <<EOF /etc/sudoers.d/99-local
notifier ALL=(ALL) NOPASSWD: ALL
EOF

USER notifier
ENV PATH="/workspaces/riga-public-consultation-notifier/scripts:$PATH"
ENV TZ=Europe/Riga
RUN echo "alias ll='ls -alF'" >> /home/notifier/.bash_aliases

USER root
