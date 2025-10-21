import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import yaml
import sys
from pyterminal.pyterminal import * 

from commands import *
from utilities import *
from logo import LOGO

class Emmet():
    def __init__(self):
        print(LOGO)
        self.LoadSettings()
        self.Setup()
    
    def LoadSettings(self):
        #Configuration
        with open('configuration.yaml', 'r') as file:
            self.currentSettings = yaml.safe_load(file)
        
        print(blue("[BOOT]") + " Loading settings...", end="")   
        self.PICOVOICE_ACCESS_KEY = self.currentSettings["picovoice"]["access-key"]
        self.WAKE_WORD_FILE = self.currentSettings["picovoice"]["wake-up-word-file"]
        self.MODEL_FILE_IT = self.currentSettings["picovoice"]["model-file"]
        self.HASS_URL = self.currentSettings["homeassistant"]["server-url"]
        self.HASS_TOKEN = self.currentSettings["homeassistant"]["access-token"]
        print(bright_green("Done!"))

        self.recognizer = sr.Recognizer()

    def Setup(self):
        pass 

    def Start(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.PICOVOICE_ACCESS_KEY,
                keyword_paths=[self.WAKE_WORD_FILE],
                model_path=self.MODEL_FILE_IT
            )

            self.pa = pyaudio.PyAudio()
            
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print(blue("[INFO]") + " Pronto. In ascolto per 'Hey Doc!'...")

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
                    print(blue("[INFO]") + " Listening for command...")

                    # --- Ora usa SpeechRecognition per capire il comando ---
                    with sr.Microphone() as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        
                        try:
                            audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            
                            self.commandText = self.recognizer.recognize_google(audio_data, language="it-IT")
                            print(blue("[INFO]") + f" Comando ricevuto: '{self.commandText}'")

                            shutdown = self.PerformAction()
                            if shutdown:
                                break

                        except sr.WaitTimeoutError:
                            print(blue("[INFO]") + " Nessun comando ricevuto, torno in ascolto...")
                        except sr.UnknownValueError:
                            print(blue("[INFO]") + " Non ho capito il comando, torno in ascolto...")
                        except sr.RequestError as e:
                            print(red("[ERRORE]") + f" Errore API Google; {e}")
                        except KeyboardInterrupt:
                            self.ExitEmmet()

                    print("---------------------------------")
                    print(blue("[INFO]") + f" Listening for 'Hey Doc!'...")

                    self.audio_stream.start_stream()

        except pvporcupine.PorcupineError as e:
            print(red("[ERRORE]") + f" Errore Porcupine: {e}")
        except Exception as e:
            print(red("[ERRORE]") + f" Errore generico: {e}")
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