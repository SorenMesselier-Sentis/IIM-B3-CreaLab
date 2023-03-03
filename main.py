import network   #import des fonction lier au wifi
import urequests    #import des fonction lier au requetes http
import utime    #import des fonction lier au temps
import ujson    #import des fonction lier aà la convertion en Json
import ssd1306
from machine import Pin, PWM, freq, I2C
import machine
import scanplayer
from picodfplayer import DFPlayer
from utime import sleep_ms, sleep
# import framebuf

#Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE=0
TX_PIN = 16
RX_PIN=17
BUSY_PIN=2

player=DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)


# Configuration de la LED RGB
ledR = PWM(Pin(22, mode=Pin.OUT))
ledG = PWM(Pin(21, mode=Pin.OUT))
ledB = PWM(Pin(20, mode=Pin.OUT))

# Configuration de l'écran OLED
i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.text("Bienvenue !", 0,0)
oled.show()
utime.sleep(2)



# Dictionnaire des couleurs
colors = {
    "Normal": (255, 255, 255),  # Blanc
    "Feu": (255, 0, 0),        # Rouge
    "Eau": (0, 0, 255),        # Bleu
    "Plante": (0, 255, 0),     # Vert
    "Insecte": (139, 69, 19),  # Marron
    "Vol": (255, 255, 255),    # Blanc
    "Électrik": (255, 255, 0),  # Jaune
    "Sol": (255, 165, 0),      # Orange
    "Roche": (128, 128, 128),  # Gris foncé
    "Combat": (139, 0, 0),     # Rouge foncé
    "Psy": (128, 0, 128),      # Violet
    "Spectre": (128, 0, 128),  # Violet foncé
    "Glace": (255, 255, 255),  # Blanc
    "Dragon": (75, 0, 130),    # Violet foncé
    "Tenebres": (0, 0, 0),     # Noir
    "Acier": (192, 192, 192),  # Gris métallique
    "Fee": (255, 192, 203)     # Rose
}

wlan = network.WLAN(network.STA_IF) # met la raspi en mode client wifi
wlan.active(True) # active le mode client wifi

ssid = 'IIM_Private'
password = 'Creatvive_Lab_2023'
wlan.connect(ssid, password) # connecte la raspi au réseau



while not wlan.isconnected():
    print("att")
    oled.fill(0)
    # Affichage du nom du Pokémon en blanc
    oled.text("Patientez...", 0, 0, 1)
    # Mise à jour de l'écran
    oled.show()
    utime.sleep(1)
    
oled.fill(0)
# Affichage du nom du Pokémon en blanc
oled.text("Pokemon ?", 0, 0, 1)
# Mise à jour 
oled.show()

# Fonction pour afficher le nom du Pokémon sur l'écran OLED
def display_pokemon_name(name):
    # Effacement de l'écran
    oled.fill(0)
    # Affichage du nom du Pokémon en blanc
    oled.text(name, 0, 0, 1)
    # Mise à jour de l'écran
    oled.show()
    
def display_pokemon_sprite(sprite_data):
    # Effacement de l'écran
    oled.fill(0)
    # Dessin du sprite du Pokémon
    for i, row in enumerate(sprite_data):
        for j, pixel in enumerate(row):
            if pixel == 1:
                oled.pixel(j, i, 1)
    # Mise à jour de l'écran
    oled.show()
    

try:
    pokemon_name = input("choisis ton pokemon : ") # input("Entrez le nom d'un Pokémon : ")
    response = urequests.get("https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + pokemon_name) # lance une requete sur l'url

    if response.status_code == 200:
        print("GET")
        print(response.json()["types"][0]['name']) # traite sa reponse en Json
        pokemon_type = response.json()["types"][0]['name']

        display_pokemon_name(pokemon_name)
    

        color = colors.get(pokemon_type, (0, 0, 0))
        ledR.freq(1000)  # Fréquence de 1 kHz 
        ledG.freq(1000)  # Fréquence de 1 kHz 
        ledB.freq(1000)  # Fréquence de 1 kHz 
        ledR.duty_u16(color[0] * 256)  # Rouge
        ledG.duty_u16(color[1] * 256)  # Vert
        ledB.duty_u16(color[2] * 256)  # Bleu
        # sprite : print(response.json()["sprites"]["regular"])
        # id :
        # sound : https://pokemoncries.com/cries/pokemonId.mp3
        print(response.json()["pokedexId"])
        id = response.json()["pokedexId"]
        
        player.setVolume(15)
        player.playTrack(1,id)
        print(id)
        if id <= 250:
            player.playTrack(1,id)
        if id > 250 and id <= 500:
            id = id-250
            player.playTrack(2,id)
        if id > 500 and id <= 750:
            id = id-500
            player.playTrack(3,id)
        if id > 750 and id <= 1000:
            id = id-750
            player.playTrack(4,id)
        sleep(5)
        
        # uart = machine.UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
        # Envoi de la commande de configuration
        # uart.write(bytearray([0x7E, 0xFF, 0x06, 0x0F, 0x00, 0x00, 0x01, 0xFE, 0xEF]))
        
        # Attendre que le module soit prêt
        # while uart.any() == 0:
        #     utime.sleep_ms(1)

        # response = uart.read(10)
        
        # if response == bytearray(b'\x7e\xff\x06\x0f\x00\x01\x01\xfe\xee\xef'):
        #    print("Module MP3-TF-16P V3.0 prêt")
            
        # Envoi de la commande pour initialiser la carte SD
        # uart.write(bytearray([0x7E, 0xFF, 0x06, 0x09, 0x00, 0x00, 0x00, 0xFE, 0xEF]))
        
        # Attendre que la carte SD soit initialisée
        # while uart.any() == 0:
        #     utime.sleep_ms(1)

        # response = uart.read(10)
        
        # if response == bytearray(b'\x7e\xff\x06\x09\x00\x01\x01\xfe\xec\xef'):
        #     print("Carte SD initialisée")
            
        # Envoi de la commande pour jouer le fichier audio
        # file_id = 1 # Remplacer 1 par l'ID du fichier audio que vous souhaitez lire

        # uart.write(bytearray([0x7E, 0xFF, 0x06, 0x0F, 0x00, 0x00, file_id, 0xFE, 0xEF]))
        
        # Attendre que le module commence à jouer le fichier audio
        # while uart.any() == 0:
        #     utime.sleep_ms(1)
            
        # response = uart.read(10)

        # if response == bytearray(b'\x7e\xff\x06\x0f\x00\x01\x01\xfe\xee\xef'):
        #     print("Lecture du fichier audio commencée")

                
        response.close() # ferme la demande    
        utime.sleep(1)
except Exception as e:
    print("erreur : " )
    print(e)

