FROM python:3

RUN apt-get update && apt-get install --no-install-recommends -y bash-completion locales sudo
RUN pip install --no-cache-dir \
    beautifulsoup4 \
    requests \
    slack-sdk \
    SQLAlchemy
RUN sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

RUN useradd -m -s /bin/bash notifier
COPY --chmod=440 <<EOF /etc/sudoers.d/99-local
notifier ALL=(ALL) NOPASSWD: ALL
EOF

USER notifier
ENV PATH="/workspaces/riga-public-consultation-notifier/scripts:$PATH"
ENV TZ=Europe/Riga
RUN echo "alias ll='ls -alF'" >> /home/notifier/.bash_aliases

USER root
