import speech_recognition as sr
from pyterminal.pyterminal import *
import yaml
import os

CURRENT_VERSION = "0.0.1"

def CalibrateAmbietNoise():
    # Inizializza il riconoscitore
    r = sr.Recognizer()
    print("Test Microfono e Lingua")
    print("Per favore, parla in italiano...")
    print("Stai in silenzio per tutta la durata del test")
    input("Quando sei pronto, premi INVIO...")

    try:
        with sr.Microphone() as source:
            print("Calibrazione rumore di fondo... (stai in silenzio 3 sec)")
            r.adjust_for_ambient_noise(source, duration=3)
            print(f"Soglia rumore impostata a: {r.energy_threshold}")
            
            print("\nPronto. Parla ora! (es. 'prova uno due tre')")
            
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            
            print("Audio ricevuto. Trascrizione...")
            testo = r.recognize_google(audio, language="it-IT")
            
            print(f"\nRISULTATO: '{testo}'")

    except sr.WaitTimeoutError:
        print("\nERRORE: Timeout. Non ho sentito nulla.")
    except sr.UnknownValueError:
        print("\nERRORE: Google non ha capito l'audio. Prova a parlare più forte o più chiaro.")
    except sr.RequestError as e:
        print(f"\nERRORE: Impossibile contattare i servizi Google. Verifica la connessione. {e}")

    print("--- Test terminato ---")
    
def DisplayHelp():
    print(cyan(f"Emmet versione {CURRENT_VERSION}"))
    print("__________________________")
    print()
    print(cyan("Opzioni:"))
    print(yellow("-h | --help") + "        Mostra Questo messaggio")
    print(yellow("-c | --calibrate") + "   Avvia Calibrazione rumore di fondo")
    print(yellow("-v | --version") + "     Mostra versione corrente")
    print(yellow("-u | --update") + "      Controlla aggiornamenti")
    print()
    print(cyan("Impostazioni:"))
    print(yellow("-s | --set") + " <SECTION> <KEY> <VALUE>     Imposta un valore nel file di configurazione")
    print(cyan("Struttura file di configurazione:"))
    print(" " + yellow("- picovoice") + ":")
    print("    - access-key")
    print("    - wake-up-word-file")
    print("    - model-file")
    print(" " + yellow("- homeassistant"))
    print("    - url")
    
def DisplayVersion():
    print(f"Emmet versione {CURRENT_VERSION}")

def CheckForUpdates():
    print(cyan("Controllo aggiornamenti..."))
    #still to be implemented
    

def SetConfigValue(section, key, value):
    print(cyan(f"Impostazione del valore di configurazione:"))
    print(f"{section}")
    print(f" - {key}: {value}")
    
    with open("configuration.yaml", "r") as cfg:
        currentConfiguration = yaml.safe_load(cfg)
    
    if(not(section in currentConfiguration)):
        currentConfiguration.update({section: {}})
    currentConfiguration[section][key] = value
    
    with open("configuration.yaml", "w") as cfg:
        yaml.dump(currentConfiguration, cfg, sort_keys=False)
        
    print(bold(bright_green("[INFO]")) + " Configurazione salvata.")
    
def GetConfigValue(section, key):
    print(cyan(f"Recupero del valore di configurazione:"))
    print(f"{section}")
    print(f" - {key}: ", end="")
    
    with open("configuration.yaml", "r") as cfg:
        currentConfiguration = yaml.safe_load(cfg)
    
    try:
        value = currentConfiguration[section][key]
        print(bright_green(f"{value}"))
    except KeyError:
        print(bold(red("[ERRORE]")) + " Sezione o chiave non trovata nella configurazione.")
        
def ClearLogFiles():
    """Clears the logs directory contents"""
    logdir_path = "logs"
    print(cyan("Cancellazione file di log ..."))
    try:
        for logfile in os.listdir(logdir_path):
            if logfile.endswith(".log"):
                os.remove(os.path.join(logdir_path, logfile))
        print(bold(bright_green("[INFO]")) + " File di log cancellati con successo.")
    except Exception as e:
        print(bold(red("[ERRORE]")) + f" Impossibile cancellare il file di log. Dettagli: {e}")
    