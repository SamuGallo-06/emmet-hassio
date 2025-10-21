from datetime import datetime as dt

def DisplayHour():
    currentTime = dt.now().strftime("%H:%M:%S")
    print(f"Doc: Sono le {currentTime}")
    
def DisplayDate():
    currentDate = dt.now().strftime("%d/%m/%Y")
    print(f"Doc: Oggi è il {currentDate}")