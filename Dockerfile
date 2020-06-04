FROM ubuntu:20.04

LABEL name="BonjourMadame API Server" \
      maintainer="Djerfy <djerfy@gmail.com>" \
      repository="https://github.com/djerfy/bonjourmadame-api-server.git" \
      version="1.9.0"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install flask requests

ADD src /app

RUN chmod +x /app/bm-api-server.py
    
ENTRYPOINT ["/usr/bin/python3", "/app/bm-api-server.py"]
