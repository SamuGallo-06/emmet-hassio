import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import yaml
import sys
from pyterminal.pyterminal import * 
import logging
import datetime

from commands import *
from utilities import *
from logo import LOGO

class Emmet():
    def __init__(self):
        print(LOGO)
        self.CreateLogFile()
        self.LoadSettings()
        self.Setup()
        
    def CreateLogFile(self):
        print(blue("[BOOT]") + " Creating log file...", end="")
        currentDateTime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")  
        logging.basicConfig(filename=f"emmet-{currentDateTime}.log", filemode="w", format="[%(asctime)s][%(levelname)s] %(message)s")
        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler('logs.log')
        self.logger.addHandler(file_handler)
        print(bright_green("Done!"))
    
    def LoadSettings(self):
        #Configuration
        with open('configuration.yaml', 'r') as file:
            self.currentSettings = yaml.safe_load(file)
        
        print(blue("[BOOT]") + " Loading settings...", end="")
        self.logger.info("Loading Settings...")   
        self.PICOVOICE_ACCESS_KEY = self.currentSettings["picovoice"]["access-key"]
        self.WAKE_WORD_FILE = self.currentSettings["picovoice"]["wake-up-word-file"]
        self.MODEL_FILE_IT = self.currentSettings["picovoice"]["model-file"]
        self.HASS_URL = self.currentSettings["homeassistant"]["server-url"]
        self.HASS_TOKEN = self.currentSettings["homeassistant"]["access-token"]
        print(bright_green("Done!"))
        self.logger.info("Done!")

    def Setup(self):
        self.recognizer = sr.Recognizer()
        
        try:
            self.logger.info("Setting Up Porcupine")
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
            self.logger.info("Listening for 'Hey Doc!'")
            print(blue("[INFO]") + " Pronto. In ascolto per 'Hey Doc!'...")
            
        except pvporcupine.PorcupineError as e:
            print(red("[ERROR]") + f" Porcupine error has occurred: {e}")
            self.logger.critical(f" Porcupine error has occurred: {e}")
        except Exception as e:
            print(red("[ERROR]") + f" A generic error has occurred: {e}")
            self.logger.critical(f" A generic error has occurred: {e}")
        except KeyboardInterrupt:
            self.ExitEmmet()

    def Start(self):
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
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        
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
        if 'porcupine' in locals() and self.porcupine is not None:
            self.porcupine.delete()
        if 'audio_stream' in locals() and self.audio_stream is not None:
            self.audio_stream.close()
        if 'pa' in locals() and self.pa is not None:
            self.pa.terminate()
        print(bright_green("Done!"))
        print(blue("[INFO]") + " Leaving...")    
        sys.exit(0)
                
    def PerformAction(self) -> bool:
        
        cmd = self.commandText.lower()
        
        #Still not be implemented, testing only Assist in Home assistant
        
        #if(("che ore sono" in cmd) or ("ore" in cmd)):
            #DisplayHour()
            
        #elif(("che giorno è" in cmd) or ("giorno" in cmd) or ("oggi è il" in cmd)):
            #DisplayDate() 
                                       
        #elif("arrivederci" in cmd):
            #print(magenta("AZIONE") + ": Spegnimento...")
            #return True
        
        #else:
            #Ask assist
            #print(magenta("AZIONE") + ": Contatto Assist")
            #result = AskAssist(self.HASS_URL, self.HASS_TOKEN, self.commandText)
            
            #print("Azione eseguita con successo") if result else print("Si è verificato un errore")
        
        result = AskAssist(self.HASS_URL, self.HASS_TOKEN, self.commandText)
        print("Azione eseguita con successo") if result else print("Si è verificato un errore")
        self.logger.info(f"Command run successfully") if result else self.logger.critical(f"Failed running command")
        
        return False
    
if __name__ == "__main__":
    if(len(sys.argv) > 1):
        arg = sys.argv[1]

        if arg == "--help" or arg == "-h":
            DisplayHelp()
        elif arg == "--calibrate" or arg == "-c":
            CalibrateAmbietNoise()
        elif arg == "--version" or arg == "-v":
            DisplayVersion()  
        elif arg == "--update" or arg == "-u":
            CheckForUpdates()   
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
                DisplayHelp()
        else:
            print(bold(red("[ERRORE]")) + f" Opzione non riconosciuta '{arg}'")
            print("Usa -h o --help per vedere le opzioni disponibili.")
    else:
        emmet = Emmet() 
        emmet.Start()