import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import yaml
import sys
from pyterminal import * 
import logging
import datetime
import re
import os
import threading

from commands import *
from utilities import *
from logo import LOGO
from webui import *

class Emmet():
    def __init__(self):
        print(LOGO)
        self.CreateLogFile()
        self.LoadSettings()
        self.Setup()
        
    def CreateLogFile(self):
        if(not os.path.exists("logs")):
            print(blue("[BOOT]") + " Logs directory not found.")
            print(blue("[BOOT]") + " Creating logs directory...", end="")
            os.makedirs("logs")
            print(bright_green("Done!"))
        
        print(blue("[BOOT]") + " Creating log file...", end="")
        currentDateTime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")  
        logging.basicConfig(filename=f"logs/emmet-{currentDateTime}.log", filemode="w", format="[%(asctime)s][%(levelname)s] %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(f'logs/emmet-{currentDateTime}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(file_handler)
        print(bright_green("Done!"))
    
    def LoadSettings(self):
        #Configuration
        with open('configuration.yaml', 'r') as file:
            self.currentSettings = yaml.safe_load(file)
        
        print(blue("[BOOT]") + " Loading settings...", end="")
        
        #Settigs
        self.logger.info("Loading Settings...")   
        self.PICOVOICE_ACCESS_KEY = self.currentSettings["picovoice"]["access-key"]
        self.WAKE_WORD_FILE = self.currentSettings["picovoice"]["wake-up-word-file"]
        self.MODEL_FILE_IT = self.currentSettings["picovoice"]["model-file"]
        self.HASS_URL = self.currentSettings["homeassistant"]["server-url"]
        self.HASS_TOKEN = self.currentSettings["homeassistant"]["access-token"]
        self.LOGLEVEL = self.currentSettings["logging"]["level"]
        self.WEBUI_ENABLED = self.currentSettings["webui"]["enabled"]
        self.WEBUI_PORT = self.currentSettings["webui"]["port"]
        self.AUDIO_DEVICE = self.currentSettings["audio"]["device"]
        self.AUDIO_CALIBRATE_ON_START = self.currentSettings["audio"]["calibrate_on_start"]
        
        print(bright_green("Done!"))
        self.logger.info("Done!")

    def Setup(self):
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        self.recognizer = sr.Recognizer()
        
        try:
            self.logger.info("Setting Up Porcupine...")
            self.porcupine = pvporcupine.create(
                access_key=self.PICOVOICE_ACCESS_KEY,
                keyword_paths=[self.WAKE_WORD_FILE],
                model_path=self.MODEL_FILE_IT
            )
            self.logger.info("Done!")
            

            self.pa = pyaudio.PyAudio()
            
            self.logger.info("Configuring Audio Stream")
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            self.logger.info("Done!")
            self.logger.info("Setup completed")
            print(blue("[INFO]") + " Pronto!")
            
        except pvporcupine.PorcupineError as e:
            print(red("[ERROR]") + f" Porcupine error has occurred: {e}")
            self.logger.critical(f" Porcupine error has occurred: {e}")
        except Exception as e:
            print(red("[ERROR]") + f" A generic error has occurred: {e}")
            self.logger.critical(f" A generic error has occurred: {e}")
        except KeyboardInterrupt:
            self.ExitEmmet()

    def Start(self):
        print(blue("[INFO]") + " Listening for 'Hey Doc!'...")
        self.logger.info("Listening for 'Hey Doc!'")
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                # 'keyword_index' will be 0 if the keyword is detected
                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    #Hey Doc! Detected
                    print("---------------------------------")
                    print(blue("[INFO]") + " Wake-word 'Hey Doc!' rilevata!")
                    self.audio_stream.stop_stream() 
                    self.logger.info("Stopping audio stream")
                    self.logger.info("Keyword detected")
                    self.logger.info("Listening for command...")
                    print(blue("[INFO]") + " Listening for command...")

                    with sr.Microphone() as source:
                        if(self.AUDIO_CALIBRATE_ON_START):
                            print(blue("[INFO]") + " Calibrating ambient noise, please stay silent...", end="")
                            self.recognizer.adjust_for_ambient_noise(source, duration=3)
                            print(bright_green("Done!"))
                            print(blue("[INFO]") + f" Energy threshold set to: {self.recognizer.energy_threshold}")
                            self.logger.info(f"Ambient noise calibrated, energy threshold set to: {self.recognizer.energy_threshold}")
                        
                        try:
                            audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            
                            self.commandText = self.recognizer.recognize_google(audio_data, language="it-IT")
                            print(blue("[INFO]") + f" Comando ricevuto: '{self.commandText}'")
                            self.logger.info(f"Command recieved: {self.commandText}")

                            shutdown = self.PerformAction()
                            if shutdown:
                                break

                        except sr.WaitTimeoutError:
                            print(blue("[INFO]") + " Nessun comando ricevuto, torno in ascolto...")
                            self.logger.info("No command recieved, listening for wakeup word")
                        except sr.UnknownValueError:
                            print(blue("[INFO]") + " Non ho capito il comando, torno in ascolto...")
                            self.logger.info("Command unrecognized")
                        except sr.RequestError as e:
                            print(red("[ERRORE]") + f" Errore API Google; {e}")
                            self.logger.critical(f"An error occurred while communicating with Google services\nDetails:\n{e}")
                        except KeyboardInterrupt:
                            self.ExitEmmet()

                    print("---------------------------------")
                    print(blue("[INFO]") + f" Listening for 'Hey Doc!'...")
                    self.logger.info("Listening for 'Hey Doc!'...")

                    self.audio_stream.start_stream()
                    self.logger.info("Starting audio stream...")

        except pvporcupine.PorcupineError as e:
            print(red("[ERRORE]") + f" Errore Porcupine: {e}")
            self.logger.critical(f" Porcupine error has occurred: {e}")
        except Exception as e:
            print(red("[ERRORE]") + f" Errore generico: {e}")
            self.logger.critical(f" A generic error has occurred: {e}")
        except KeyboardInterrupt:
            self.ExitEmmet()
        finally:
            self.ExitEmmet()
            
    def ExitEmmet(self):
        print(blue("[INFO]") + " Cleaning up...", end="")
        self.logger.info("Exiting Emmet")
        if 'porcupine' in locals() and self.porcupine is not None:
            self.porcupine.delete()
        if 'audio_stream' in locals() and self.audio_stream is not None:
            self.audio_stream.close()
        if 'pa' in locals() and self.pa is not None:
            self.pa.terminate()
        print(bright_green("Done!"))
        print(blue("[INFO]") + " Leaving...")    
        self.logger.info("Cleanup completed")
        sys.exit(0)
                
    def PerformAction(self) -> bool:
        
        cmd = self.commandText.lower()
        
        #Still not be implemented, testing only Assist in Home assistant
        
        if(("che ore sono" in cmd) or ("ore" in cmd)):
            DisplayHour()
            
        elif(("che giorno è" in cmd) or ("giorno" in cmd) or ("oggi è il" in cmd)):
            DisplayDate() 
        
        elif("sei un coglione" in cmd):
            print("Doc: Lo Sarai tu, piuttosto.") 
            
        elif("incredibile" in cmd or "impossibile" in cmd or "che casino" in cmd):
            msg = magenta("AZIONE") + ": GRANDE GIOVE!"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            
        elif("quanta energia" in cmd or "gigawatt" in cmd or "fulmine" in cmd):
            msg = magenta("AZIONE") + ": 1.21 GIGAWATT! Come ho potuto essere così sbadato!"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            
        elif("flusso canalizzatore" in cmd):
            msg = magenta("AZIONE") + ": È quello che rende possibile il viaggio nel tempo! La mia più grande invenzione!"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            
        elif("strade" in cmd or "dove andiamo" in cmd):
            msg = magenta("AZIONE") + ": Strade? Dove stiamo andando noi... non servono strade!"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))

        elif("delorean" in cmd or "macchina del tempo" in cmd):
            msg = magenta("AZIONE") + ": Se proprio devi costruire una macchina del tempo... perché non farla con un po' di STILE?"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            
        elif("come faccio" in cmd or "non lo so" in cmd or "un consiglio" in cmd):
            msg = magenta("AZIONE") + ": Devi pensare quadrimensionalmente! Ignora le tre dimensioni!"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            
        elif("arrivederci" in cmd or "spegniti" in cmd):
            msg = magenta("AZIONE") + ": Ci vediamo... nel futuro! (Spegnimento...)"
            print(msg)
            self.logger.info(self.ansi_escape.sub('', msg))
            return True # Ritorna True per spegnere
        
        else:
            #Ask assist
            print(magenta("AZIONE") + ": Contatto Assist")
            result = AskAssist(self.HASS_URL, self.HASS_TOKEN, self.commandText, self.logger)
            
            print("Azione eseguita con successo") if result else print("Si è verificato un errore")
        
        # result = AskAssist(self.HASS_URL, self.HASS_TOKEN, self.commandText)
        # print("Azione eseguita con successo") if result else print("Si è verificato un errore")
        # self.logger.info(f"Command run successfully") if result else self.logger.critical(f"Failed running command")
        
        # return False

def CheckArgs():
    arg = sys.argv[1]

    if arg == "--help" or arg == "-h":
        DisplayHelp()
    elif arg == "--calibrate" or arg == "-c":
        CalibrateAmbietNoise()
    elif arg == "--version" or arg == "-v":
        DisplayVersion()  
    elif arg == "--update" or arg == "-u":
        CheckForUpdates()
    elif arg == "--get" or arg == "-g":
        if len(sys.argv) == 4:
            section = sys.argv[2]
            key = sys.argv[3]
            GetConfigValue(section, key)
        else:
            print(bold(red("[ERRORE]")) + "L'opzione --get richiede 2 argomenti: <SECTION> <KEY>")
            print("Esempio: python emmet.py --get " + blue("homeassistant") + bright_green("homeassistant"))
            print()
    elif arg == "--clear-logs" or arg == "-cl":
        ClearLogFiles()
    elif arg == "--set" or arg == "-s":
        if len(sys.argv) == 5:
            section = sys.argv[2]
            key = sys.argv[3]
            value = sys.argv[4]
            SetConfigValue(section, key, value)
        else:
            print(bold(red("[ERRORE]")) + "L'opzione --set richiede 3 argomenti: <SECTION> <KEY> <VALUE>")
            print("Esempio: python emmet.py --set " + blue("homeassistant") + bright_green("homeassistant") + yellow("http://192.168.1.10:8123"))
            print()
    else:
        print(bold(red("[ERRORE]")) + f" Opzione non riconosciuta '{arg}'")
        print("Usa -h o --help per vedere le opzioni disponibili.")
    
if __name__ == "__main__":
    if(len(sys.argv) > 1):
        CheckArgs()
    else:
        emmet = Emmet()
        
        # Read Ingress Path from environment variable (for Home Assistant add-on)
        ingress_path = os.environ.get('INGRESS_PATH', '')
        
        if(emmet.WEBUI_ENABLED):
            # Start the Web UI in a separate thread
            emmet_webui = EmmetWebUI(emmet, emmet.logger, ingress_path=ingress_path)
            webui_thread = threading.Thread(target=emmet_webui.Run, daemon=True)
            webui_thread.start()

        # Start the voice assistant in the main thread
        emmet.Start()