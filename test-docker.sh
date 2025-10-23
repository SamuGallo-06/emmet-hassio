#!/bin/bash
# Script per testare l'add-on localmente con Docker

echo "Building Emmet Docker image..."

# Build per l'architettura corrente
docker build -t local/emmet:latest \
  --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18" \
  .

echo ""
echo "Starting Emmet container..."
echo "Press Ctrl+C to stop"
echo ""

# Esegui il container con accesso audio
docker run -it --rm \
  --name emmet-test \
  --device /dev/snd:/dev/snd \
  -p 5000:5000 \
  -v "$(pwd)/configuration.yaml:/app/configuration.yaml" \
  -v "$(pwd)/logs:/app/logs" \
  -e PICOVOICE_ACCESS_KEY="${PICOVOICE_ACCESS_KEY}" \
  -e HASS_TOKEN="${HASS_TOKEN}" \
  local/emmet:latest

# Note: 
# Assicurati di impostare le variabili d'ambiente prima di eseguire:
# export PICOVOICE_ACCESS_KEY="your_key"
# export HASS_TOKEN="your_token"
