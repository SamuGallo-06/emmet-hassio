import speech_recognition as sr

# Inizializza il riconoscitore
r = sr.Recognizer()

print("--- Test Microfono e Lingua (Solo Google) ---")
print("Per favore, parla in italiano...")

try:
    with sr.Microphone() as source:
        # Calibra per il rumore (aumentiamo a 1 secondo)
        print("Calibrazione rumore di fondo... (stai in silenzio 1 sec)")
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"Soglia rumore impostata a: {r.energy_threshold}")
        
        print("\nPronto. Parla ora! (es. 'prova uno due tre')")
        
        # Ascolta l'audio
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        print("Audio ricevuto. Invio a Google per la trascrizione...")

        # Riconosci usando Google, specificando l'italiano
        testo = r.recognize_google(audio, language="it-IT")
        
        print(f"\nRISULTATO: Google ha capito: '{testo}'")

except sr.WaitTimeoutError:
    print("\nERRORE: Timeout. Non ho sentito nulla.")
except sr.UnknownValueError:
    print("\nERRORE: Google non ha capito l'audio. Prova a parlare più forte o più chiaro.")
except sr.RequestError as e:
    print(f"\nERRORE: Impossibile contattare i servizi Google. Verifica la connessione. {e}")

print("--- Test terminato ---")