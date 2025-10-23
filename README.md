# Emmet Voice Assistant for Home Assistant

> "Wait a minute, Doc. Are you telling me you built a voice assistant... for Home Assistant?"

**Emmet** è un assistente vocale self-hosted, scritto in Python, progettato per integrarsi direttamente con [Home Assistant](https://www.home-assistant.io/) come **add-on**.

Utilizza la wake-word personalizzata **"Hey Doc!"** per attivarsi e poi ascolta i tuoi comandi in italiano. È costruito per essere leggero, rispettoso della privacy e tematico.

## 🎯 Caratteristiche Principali

* 🎤 **Wake-Word Offline**: Usa [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) per rilevare "Hey Doc!" in modo efficiente e completamente offline
* 🏠 **Integrazione Home Assistant**: Invia comandi direttamente ad Home Assistant Assist
* 🌐 **Interfaccia Web**: Dashboard integrata per monitoraggio e configurazione
* 📊 **Monitoring**: Monitor risorse di sistema (CPU, RAM, temperatura su Raspberry Pi)
* 🔐 **Privacy-First**: La tua voce non lascia la rete locale (tranne per il riconoscimento via Google Speech-to-Text)
* 🐳 **Docker Ready**: Supporto multi-architettura (armhf, armv7, aarch64, amd64, i386)
* 🇮🇹 **Italiano**: Comandi e riconoscimento vocale in italiano

## 📋 Requisiti

* Home Assistant OS o Supervised
* Raspberry Pi 4 (2GB+ RAM consigliato) o altro hardware compatibile
* Microfono USB di buona qualità
* Picovoice Access Key (gratuita per uso personale)
* Home Assistant Long-Lived Token

## 🚀 Installazione Rapida

### Come Add-on Home Assistant (Consigliato)

1. Aggiungi questo repository agli add-on di Home Assistant:
   - Vai su **Impostazioni** → **Add-on** → **Archivio add-on**
   - Click sui tre puntini → **Repository**
   - Aggiungi: `https://github.com/SamuGallo-06/emmet-hassio`

2. Installa l'add-on **Emmet Voice Assistant**

3. Configura le opzioni (vedi sotto)

4. Avvia l'add-on

5. Accedi alla Web UI tramite ingress

### Configurazione Base

```yaml
picovoice_access_key: "YOUR_PICOVOICE_KEY"
hass_token: "YOUR_HA_LONG_LIVED_TOKEN"
wake_word_file: "models/Hey-Doc_it_linux_v3_0_0.ppn"
model_file: "models/porcupine_params_it.pv"
hass_url: "http://supervisor/core"
webui_enable: true
log_level: "INFO"
audio_device: "default"
calibrate_on_start: false
```

📖 **Documentazione completa**: Vedi [DOCS.md](DOCS.md) per istruzioni dettagliate

🚀 **Guida Deploy**: Vedi [DEPLOY.md](DEPLOY.md) per istruzioni di deployment

## 💬 Esempi di Comandi

* "Hey Doc! Che ore sono?"
* "Hey Doc! Che giorno è oggi?"
* "Hey Doc! Accendi la luce del salotto"
* "Hey Doc! Imposta la temperatura a 22 gradi"
* "Hey Doc! Grande Giove!" (easter egg)
* "Hey Doc! Arrivederci" (spegne l'assistente)

## 🏗️ Architettura

```
┌─────────────────────────────────────┐
│   Home Assistant Add-on (Docker)    │
│  ┌───────────────────────────────┐  │
│  │   Emmet Voice Assistant       │  │
│  │  ┌─────────┐  ┌────────────┐ │  │
│  │  │Porcupine│  │ Web UI     │ │  │
│  │  │Wake Word│  │ (Flask)    │ │  │
│  │  └────┬────┘  └─────┬──────┘ │  │
│  │       │             │        │  │
│  │  ┌────▼─────────────▼──────┐ │  │
│  │  │  Speech Recognition     │ │  │
│  │  │  (Google STT)           │ │  │
│  │  └────┬────────────────────┘ │  │
│  │       │                      │  │
│  │  ┌────▼──────────────────┐  │  │
│  │  │  Home Assistant       │  │  │
│  │  │  Assist Integration   │  │  │
│  │  └───────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## 🛠️ Sviluppo e Test Locale

### Installazione Standalone

```bash
# Clone del repository
git clone https://github.com/SamuGallo-06/emmet-hassio.git
cd emmet-hassio

# Installa dipendenze
pip install -r requirements.txt

# Configura configuration.yaml

# Avvia
python3 main.py
```

### Test con Docker

```bash
# Imposta variabili d'ambiente
export PICOVOICE_ACCESS_KEY="your_key"
export HASS_TOKEN="your_token"

# Build e run
./test-docker.sh
```

## 📦 File del Progetto

```
emmet/
├── main.py              # Entry point principale
├── webui.py            # Interfaccia web Flask con ingress
├── commands.py         # Comandi vocali
├── utilities.py        # Utility functions
├── logo.py             # ASCII art logo
├── Dockerfile          # Container definition
├── config.json         # Configurazione add-on HA
├── build.json          # Build multi-arch
├── run.sh              # Script di avvio add-on
├── requirements.txt    # Dipendenze Python
├── models/             # Modelli Porcupine
├── templates/          # Template HTML
├── static/             # CSS/JS per UI
└── logs/               # Directory log
```

## 🤝 Contributi

Contributi, issues e feature requests sono benvenuti!

1. Fork del progetto
2. Crea il tuo branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Changelog

Vedi [CHANGELOG.md](CHANGELOG.md) per la lista delle modifiche.


## License

The source code of **Emmett** is released under the [MIT License](LICENSE).

Please note that this project depends on Picovoice Porcupine, which is governed by the [Apache 2.0 License](https://github.com/Picovoice/porcupine/blob/master/LICENSE). Wake-word models ...
