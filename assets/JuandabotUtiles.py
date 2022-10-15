import ctypes, requests
from colorama import *
from datetime import datetime

def windowsBox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def checkFNapiIO(currentUser, key='nada'):
    try:
        headers = {'Authorization': key}
        response = requests.get(f'https://fortniteapi.io/v1/lookup?username={currentUser}', headers=headers).json()["result"]
        if response:
            return True
        else:
            return False
    except:
        return False

class jdbconsole:
    def log(xyz):
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        print(Fore.LIGHTBLUE_EX + f'[LOG] {datetimeLog} >> {xyz}')

    def error(xyz):
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        print(Fore.RED + f'[ERROR] {datetimeLog} >> {xyz}')

    def warning(xyz):
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        print(Fore.YELLOW + f'[WARNING] {datetimeLog} >> {xyz}')

    def tip(xyz):
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        print(Fore.LIGHTGREEN_EX + f'[TIP] {datetimeLog} >> {xyz}')

    def errTip(discordLink):
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        print(Fore.LIGHTGREEN_EX + f'[TIP] {datetimeLog} >> Envia captura de pantalla del error al Discord de JuandaBot - {discordLink}')
    
    def exitMsg():
        ya = datetime.now(); datetimeLog = f"{ya.hour}:{ya.minute}:{ya.second}"
        input(Fore.RED + f'[TIP] {datetimeLog} >> Ya puedes cerrar el bot.')
        quit()