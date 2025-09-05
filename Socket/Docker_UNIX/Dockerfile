FROM debian:stable

# Evita prompt interattivi
ENV DEBIAN_FRONTEND=noninteractive

# Aggiorna il sistema e installa pacchetti base + Python
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    iproute2 \
    net-tools \
    iputils-ping \
    curl \
    vim \
    procps \
    dnsutils \
    netcat-openbsd \
    tcpdump \
    && apt clean

# Imposta la directory di lavoro
WORKDIR /workspace
