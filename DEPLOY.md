# Emmet Voice Assistant - Guida Rapida per Home Assistant Add-on

## 📦 File creati per l'add-on

- ✅ `Dockerfile` - Container definition per multi-arch
- ✅ `config.json` - Configurazione add-on (opzioni, schema, ingress)
- ✅ `build.json` - Build configuration per diverse architetture
- ✅ `run.sh` - Script di avvio che legge opzioni e configura Emmet
- ✅ `webui.py` - Aggiornato con supporto ingress
- ✅ `main.py` - Aggiornato per leggere INGRESS_PATH
- ✅ `DOCS.md` - Documentazione completa per utenti
- ✅ `.dockerignore` - Ottimizzazione build Docker

## 🚀 Come testare localmente

### 1. Testa senza Docker

```bash
# Installa dipendenze
pip install -r requirements.txt

# Configura configuration.yaml con le tue chiavi

# Avvia
python3 main.py
```

### 2. Testa con Docker (simula add-on)

```bash
# Imposta le variabili d'ambiente
export PICOVOICE_ACCESS_KEY="your_picovoice_key"
export HASS_TOKEN="your_home_assistant_token"

# Esegui lo script di test
./test-docker.sh
```

## 📤 Deploy su Home Assistant

### Opzione A: Repository GitHub (Consigliato)

1. **Push su GitHub**:
   ```bash
   git add .
   git commit -m "Add Home Assistant add-on support"
   git push origin main
   ```

2. **Crea repository add-on** (se non esiste):
   - Crea un file `repository.json` nella root:
   ```json
   {
     "name": "Emmet Voice Assistant Repository",
     "url": "https://github.com/SamuGallo-06/emmet-hassio",
     "maintainer": "SamuGallo-06"
   }
   ```

3. **Aggiungi repository in Home Assistant**:
   - Vai su **Impostazioni** → **Add-on** → **Archivio add-on**
   - Click sui tre puntini → **Repository**
   - Aggiungi: `https://github.com/SamuGallo-06/emmet-hassio`

4. **Installa l'add-on** dalla lista

### Opzione B: Installazione Locale

1. **Copia i file**:
   ```bash
   # Su Home Assistant, copia la cartella del progetto in /addons
   scp -r /home/samug/Progetti/emmet root@homeassistant.local:/addons/
   ```

2. **Riavvia Supervisor**:
   - Impostazioni → Sistema → Riavvia → Supervisor

3. **Installa l'add-on** dalla lista "Add-on locali"

## ⚙️ Configurazione Add-on

### Opzioni Obbligatorie

```yaml
picovoice_access_key: "YOUR_KEY_HERE"
hass_token: "YOUR_TOKEN_HERE"
```

### Come ottenere le chiavi

**Picovoice Access Key**:
1. Vai su https://console.picovoice.ai/
2. Crea un account gratuito
3. Copia la tua Access Key

**Home Assistant Token**:
1. In Home Assistant: Profilo → Sicurezza
2. Scorri fino a "Token di accesso di lunga durata"
3. Click su "Crea token"
4. Dai un nome (es. "Emmet") e copia il token

## 🔧 Configurazione Avanzata

### Audio Device

Per trovare il tuo device audio:

```bash
# In Home Assistant Terminal add-on
aplay -l
```

Poi imposta in `audio_device`:
- `default` - device di default
- `hw:0,0` - primo device, prima scheda
- `hw:1,0` - secondo device, prima scheda

### Log Level

- `DEBUG` - Massimo dettaglio (per debugging)
- `INFO` - Informazioni normali (default)
- `WARNING` - Solo warning e errori
- `ERROR` - Solo errori
- `CRITICAL` - Solo errori critici

### Calibrazione

Attiva `calibrate_on_start: true` se:
- Il microfono rileva troppo rumore ambientale
- I comandi non vengono riconosciuti bene
- È la prima installazione

## 🌐 Accesso Web UI

### Con Ingress (Consigliato)
- Click su "Open Web UI" nella pagina dell'add-on
- L'interfaccia si apre integrata in Home Assistant

### Senza Ingress
- Accedi a `http://homeassistant.local:5000`
- (Devi esporre la porta nelle opzioni add-on)

## 📊 API Endpoints disponibili

- `GET /api/config` - Configurazione corrente
- `POST /api/config` - Aggiorna configurazione
- `GET /api/logs` - Ultimi log
- `GET /api/status` - Stato sistema
- `POST /api/command` - Invia comando testuale
- `GET /api/system` - Info sistema (CPU, RAM, temp)

## 🐛 Troubleshooting

### L'add-on non si avvia

1. Controlla i log: click su "Log" nella pagina add-on
2. Verifica che le chiavi API siano corrette
3. Controlla che il microfono sia collegato

### Audio non funziona

```bash
# Nel Terminal add-on di Home Assistant
ls -la /dev/snd
# Dovresti vedere i device audio
```

### Comandi non riconosciuti

1. Attiva `calibrate_on_start: true`
2. Parla più vicino al microfono
3. Riduci il rumore ambientale
4. Aumenta log_level a DEBUG per vedere cosa viene riconosciuto

## 🔐 Sicurezza

- ✅ Token e chiavi sono protette (type: password)
- ✅ Non loggare mai secrets nei log
- ✅ Usa `http://supervisor/core` come URL di Home Assistant
- ✅ L'add-on gira in container isolato
- ⚠️ Non esporre la porta 5000 all'esterno (usa ingress)

## 📈 Performance su Raspberry Pi 4

Risorse attese:
- **CPU**: 15-30% durante l'ascolto
- **RAM**: ~150-250 MB
- **Temperatura**: 45-60°C (con dissipatore)

Ottimizzazioni:
- Usa una microSD veloce (A2/U3)
- Usa un alimentatore ufficiale (3A)
- Aggiungi un dissipatore o ventola

## 🎯 Prossimi Passi

1. ✅ Test locale funzionante
2. 📤 Push su GitHub
3. 🏠 Deploy su Home Assistant
4. ⚙️ Configura opzioni add-on
5. 🎤 Testa con comandi vocali
6. 📝 Feedback e miglioramenti

## 📞 Supporto

- GitHub Issues: https://github.com/SamuGallo-06/emmet-hassio/issues
- Discussions: https://github.com/SamuGallo-06/emmet-hassio/discussions

---
Creato con ❤️ per Home Assistant
