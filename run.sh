#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Emmet Voice Assistant
# Reads configuration from add-on options and starts Emmet
# ==============================================================================

bashio::log.info "Starting Emmet Voice Assistant..."

# Leggi le opzioni dall'add-on
WAKE_WORD_FILE=$(bashio::config 'wake_word_file')
MODEL_FILE=$(bashio::config 'model_file')
PICOVOICE_KEY=$(bashio::config 'picovoice_access_key')
HASS_URL=$(bashio::config 'hass_url')
HASS_TOKEN=$(bashio::config 'hass_token')
WEBUI_ENABLE=$(bashio::config 'webui_enable')
LOG_LEVEL=$(bashio::config 'log_level')
AUDIO_DEVICE=$(bashio::config 'audio_device')
CALIBRATE=$(bashio::config 'calibrate_on_start')

# Verifica che le chiavi obbligatorie siano presenti
if [ -z "$PICOVOICE_KEY" ]; then
    bashio::log.warning "Picovoice access key non configurata!"
fi

if [ -z "$HASS_TOKEN" ]; then
    bashio::log.warning "Home Assistant token non configurato!"
fi

# Crea/aggiorna il file di configurazione
bashio::log.info "Updating configuration.yaml..."

cat > /app/configuration.yaml <<EOF
picovoice:
  access-key: "${PICOVOICE_KEY}"
  wake-up-word-file: "${WAKE_WORD_FILE}"
  model-file: "${MODEL_FILE}"

homeassistant:
  server-url: "${HASS_URL}"
  access-token: "${HASS_TOKEN}"

logging:
  level: ${LOG_LEVEL}
  path: "logs/"

webui:
  enabled: ${WEBUI_ENABLE}
  port: 5000

audio:
  device: "${AUDIO_DEVICE}"
  calibrate_on_start: ${CALIBRATE}
EOF

# Esegui calibrazione se richiesta
if [ "$CALIBRATE" = "true" ]; then
    bashio::log.info "Running audio calibration..."
    python3 /app/main.py --calibrate
fi

# Determina il path ingress (se disponibile)
INGRESS_PATH=""
if bashio::config.has_value 'ingress_entry'; then
    INGRESS_PATH=$(bashio::addon.ingress_entry)
    bashio::log.info "Ingress enabled at: ${INGRESS_PATH}"
    export INGRESS_PATH
fi

# Avvia Emmet
bashio::log.info "Starting Emmet main application..."
cd /app
exec python3 /app/main.py
