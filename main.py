import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import yaml
from commands import *

#Configuration
with open('configuration.yaml', 'r') as file:
    currentSettings = yaml.safe_load(file)

PICOVOICE_ACCESS_KEY = currentSettings["picovoice"]["access-key"]
print(currentSettings["picovoice"]["access-key"])

# Metti qui il percorso al file .ppn che hai scaricato
# Se è nella stessa cartella, basta il nome del file
WAKE_WORD_FILE = currentSettings["picovoice"]["wake-up-word-file"]
print(currentSettings["picovoice"]["wake-up-word-file"])

# Inizializza il riconoscitore di Google (per i comandi DOPO la wake-word)
recognizer = sr.Recognizer()

# --- INIZIALIZZAZIONE ---
MODEL_FILE_IT = currentSettings["picovoice"]["model-file"]

try:
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_ACCESS_KEY,
        keyword_paths=[WAKE_WORD_FILE],
        model_path=MODEL_FILE_IT  # <--- Questa riga ora troverà il file
    )

    # Inizializza PyAudio per lo stream del microfono
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Pronto. In ascolto per 'Hey Doc!'...")

    # --- LOOP PRINCIPALE ---
    while True:
        # Leggi un "frame" di audio dal microfono
        pcm = audio_stream.read(porcupine.frame_length)
        # Converte il buffer audio in una lista di interi (come richiesto da Porcupine)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        # Processa l'audio con Porcupine
        # 'keyword_index' sarà 0 se rileva la tua prima (e unica) wake-word
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            # RILEVATO "HEY DOC!"
            print("---------------------------------")
            print("Wake-word 'Hey Doc!' rilevata!")
            
            # Metti in pausa lo stream di Porcupine
            audio_stream.stop_stream() 
            print("Stream Porcupine in PAUSA.")
            
            print("Ora ascolto il tuo comando...")

            # --- Ora usa SpeechRecognition per capire il comando ---
            with sr.Microphone() as source:
                # Regola per il rumore ambientale
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    # Ascolta il comando
                    audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Trascrivi il comando usando Google
                    testo_comando = recognizer.recognize_google(audio_data, language="it-IT")
                    print(f"Comando ricevuto: '{testo_comando}'")

                    # --- QUI ESEGUI L'AZIONE ---
                    if "che ore sono" in testo_comando.lower():
                        print("AZIONE: Mostra l'ora")
                    elif "spegniti" in testo_comando.lower():
                        print("AZIONE: Spegnimento...")
                        break # Esce dal loop
                    else:
                        print("AZIONE: Comando non riconosciuto.")

                except sr.WaitTimeoutError:
                    print("Nessun comando ricevuto, torno in ascolto...")
                except sr.UnknownValueError:
                    print("Non ho capito il comando, torno in ascolto...")
                except sr.RequestError as e:
                    print(f"Errore API Google; {e}")

            print("---------------------------------")
            print("Torno in ascolto per 'Hey Doc!'...")
            
            # Riattiva lo stream di Porcupine
            audio_stream.start_stream()
            print("Stream Porcupine RIATTIVATO.")


except pvporcupine.PorcupineError as e:
    print(f"Errore Porcupine: {e}")
except Exception as e:
    print(f"Errore generico: {e}")
finally:
    # Pulizia finale
    if 'porcupine' in locals() and porcupine is not None:
        porcupine.delete()
    if 'audio_stream' in locals() and audio_stream is not None:
        audio_stream.close()
    if 'pa' in locals() and pa is not None:
        pa.terminate()