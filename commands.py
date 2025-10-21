from datetime import datetime as dt
import requests
import json
from pyterminal.pyterminal import *

def DisplayHour():
    currentTime = dt.now().strftime("%H:%M:%S")
    print(f"Doc: Sono le {currentTime}")
    
def DisplayDate():
    currentDate = dt.now().strftime("%d/%m/%Y")
    print(f"Doc: Oggi è il {currentDate}")

def AskAssist(hass_url, access_token, message, logger) -> bool:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": message
    }
    
    url = f"{hass_url}/api/conversation/process"
    
    print(bold(blue("[INFO]")) + " Invio Rchiesta ad assist...", end="")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        print(bold(bright_green("OK")))
        print(cyan("Risposta da Assist:"))

        response_data = response.json()
        print(json.dumps(response_data, indent=2))

        try:
            speech_response = response_data['response']['speech']['plain']['speech']
            print(f"\nTesto della risposta: {speech_response}")
        except KeyError:
            print("\n"+ bold(red("[ERRORE]")) +" Impossibile estrarre il testo della risposta dal JSON.")

    except requests.exceptions.HTTPError as errh:
        print(bold(red("[ERRORE]")) +f" Errore HTTP: {errh}")
        print(f"Dettagli risposta: {response.text}")
        logger.critical(f"HTTP Error\nDetails:\n{errh}\n\nResponse:\n{response.text}")
        return False
    except requests.exceptions.ConnectionError as errc:
        print(bold(red("[ERRORE]")) +f" Errore di connessione: {errc}")
        logger.critical(f"Connection Failed\nDetails:\n{errc}")
        return False
    except requests.exceptions.Timeout as errt:
        print(bold(red("[ERRORE]")) +f" Errore di Timeout: {errt}")
        logger.critical(f"Timeout error\nDetails:\n{errt}")
        return False
    except requests.exceptions.RequestException as err:
        print(bold(red("[ERRORE]")) +f" Errore generico: {err}")
        logger.critical(f"A Generic error has occurred\nDetails:\n{err}")
        return False
    else:
        return True
    
    