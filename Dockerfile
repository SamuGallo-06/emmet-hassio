ARG BUILD_FROM
FROM $BUILD_FROM

# Installa dipendenze di sistema necessarie per audio e Python
RUN apk add --no-cache \
    python3 \
    py3-pip \
    alsa-lib \
    alsa-lib-dev \
    portaudio \
    portaudio-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    linux-headers \
    musl-dev \
    git

# Crea directory di lavoro
WORKDIR /app

# Copia i file dell'applicazione
COPY . /app/

# Installa le dipendenze Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Crea directory per logs se non esiste
RUN mkdir -p /app/logs

# Copia script di avvio
COPY run.sh /
RUN chmod a+x /run.sh

# Esponi porta per web UI (opzionale se usi ingress)
EXPOSE 5000

# Comando di avvio
CMD [ "/run.sh" ]
