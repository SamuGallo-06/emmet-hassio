# Emmet Voice Assistant - Home Assistant Add-on

Assistente vocale italiano per Home Assistant con riconoscimento della wake word "Hey Doc!" e integrazione con Home Assistant Assist.

## Caratteristiche

- 🎤 **Wake Word Detection**: Utilizza Porcupine per rilevare "Hey Doc!"
- 🗣️ **Riconoscimento Vocale**: Google Speech Recognition per comandi in italiano
- 🏠 **Integrazione Home Assistant**: Comunica con Home Assistant Assist per eseguire comandi
- 🌐 **Interfaccia Web**: Dashboard web per monitoraggio e configurazione
- 📊 **Monitoring**: Monitor risorse di sistema (CPU, RAM, temperatura)
- 📝 **Logging**: Sistema di log dettagliato

## Installazione

### Metodo 1: Repository Add-on (Consigliato)

1. Vai su **Impostazioni** → **Add-on** → **Archivio Add-on**
2. Clicca sui tre puntini in alto a destra → **Repository**
3. Aggiungi questo URL: `https://github.com/SamuGallo-06/emmet-hassio`
4. Clicca su **Emmet Voice Assistant** e poi **Installa**

### Metodo 2: Installazione Locale

1. Copia la cartella `emmet` nella directory `/addons` di Home Assistant
2. Riavvia il Supervisor
3. L'add-on apparirà nella lista degli add-on locali

## Configurazione

### Requisiti Preliminari

1. **Picovoice Access Key**: Ottieni una chiave gratuita su [Picovoice Console](https://console.picovoice.ai/)
2. **Home Assistant Long-Lived Token**: 
   - Vai su Profilo → Sicurezza → Token di accesso di lunga durata
   - Crea un nuovo token e copialo

### Opzioni di Configurazione

```yaml
wake_word_file: models/Hey-Doc_it_linux_v3_0_0.ppn
model_file: models/porcupine_params_it.pv
picovoice_access_key: "LA_TUA_CHIAVE_PICOVOICE"
hass_url: "http://supervisor/core"
hass_token: "IL_TUO_TOKEN_HA"
webui_enable: true
log_level: INFO
audio_device: default
calibrate_on_start: false
```

#### Descrizione Opzioni

- **wake_word_file**: Percorso al file del modello wake word (.ppn)
- **model_file**: Percorso al modello linguistico Porcupine (.pv)
- **picovoice_access_key**: La tua chiave API di Picovoice (obbligatoria)
- **hass_url**: URL di Home Assistant (usa `http://supervisor/core` per add-on)
- **hass_token**: Token di accesso a Home Assistant (obbligatorio)
- **webui_enable**: Abilita/disabilita l'interfaccia web
- **log_level**: Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **audio_device**: Device audio ALSA (default, hw:0,0, etc.)
- **calibrate_on_start**: Esegui calibrazione rumore all'avvio

## Utilizzo

1. **Avvia l'add-on**: Clicca su "Start"
2. **Accedi all'interfaccia web**: Clicca su "Open Web UI" (se ingress è abilitato)
3. **Pronuncia la wake word**: Dì "Hey Doc!" vicino al microfono
4. **Dai un comando**: Dopo il rilevamento, pronuncia il comando in italiano

### Esempi di Comandi

- "Che ore sono?"
- "Che giorno è oggi?"
- "Accendi la luce del salotto" (tramite Home Assistant Assist)
- "Imposta la temperatura a 22 gradi"
- "Arrivederci" (per spegnere l'assistente)

## Risoluzione Problemi

### Il microfono non viene rilevato

1. Verifica che il dispositivo audio sia collegato
2. Controlla i log dell'add-on
3. Prova a cambiare `audio_device` in `hw:1,0` o `hw:0,0`
4. Esegui la calibrazione con `calibrate_on_start: true`

### Errore Picovoice

- Verifica che la chiave API sia corretta e valida
- Controlla che i file del modello wake word esistano nella cartella `models/`

### Errore Home Assistant API

- Verifica che il token sia valido
- Controlla che l'URL sia corretto (`http://supervisor/core` per add-on)

### Comandi non riconosciuti

- Parla chiaramente e vicino al microfono
- Attiva la calibrazione del rumore ambientale
- Aumenta il log level a DEBUG per vedere i dettagli

## Hardware Consigliato

- **Raspberry Pi 4** (2GB+ RAM)
- **Microfono USB** di buona qualità
- **Dissipatore** o ventola (consigliato per uso 24/7)

## Supporto

- 🐛 Segnala bug: [GitHub Issues](https://github.com/SamuGallo-06/emmet-hassio/issues)
- 💬 Discussioni: [GitHub Discussions](https://github.com/SamuGallo-06/emmet-hassio/discussions)

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## Crediti

- Sviluppato da [SamuGallo-06](https://github.com/SamuGallo-06)
- Wake word detection: [Picovoice Porcupine](https://picovoice.ai/)
- Speech recognition: [Google Speech Recognition](https://cloud.google.com/speech-to-text)
