import network   #import des fonction lier au wifi
import urequests    #import des fonction lier au requetes http
import utime    #import des fonction lier au temps
import ujson    #import des fonction lier aà la convertion en Json
import ssd1306
from machine import Pin, PWM, freq, I2C
import framebuf



# Configuration de la LED RGB
ledR = PWM(Pin(22, mode=Pin.OUT))
ledG = PWM(Pin(21, mode=Pin.OUT))
ledB = PWM(Pin(20, mode=Pin.OUT))

# Configuration de l'écran OLED
i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.text("heyyy", 0,0)
oled.show()


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
    utime.sleep(1)


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
        
        display_pokemon_sprite(response.json()["sprites"]["regular"])
                
        response.close() # ferme la demande    
        utime.sleep(1)
except Exception as e:
    print("erreur : " )
    print(e)

