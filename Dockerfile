FROM jazzdd/alpine-flash:python3

LABEL name="BonjourMadame API Server" \
      maintainer="Djerfy <djerfy@gmail.com>" \
      repository="https://github.com/djerfy/bonjourmadame-api-server.git" \
      version="1.6.0"

ADD src /app

RUN set -xe && \
    chmod +x /app/server.py

HEALTHCHECK --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD pgrep -f "uwsgi" || exit 1

