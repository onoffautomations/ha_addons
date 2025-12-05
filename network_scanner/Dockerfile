ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG=C.UTF-8

RUN apk add --no-cache \
    python3 \
    py3-pip \
    nmap \
    nmap-scripts \
    arp-scan \
    net-tools \
    iputils \
    bash

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

# Create cache directory for MAC vendor lookup
RUN mkdir -p /root/.cache && chmod -R 777 /root/.cache

COPY run.sh /
COPY scanner.py /app/
COPY server.py /app/
COPY web/ /app/web/

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
