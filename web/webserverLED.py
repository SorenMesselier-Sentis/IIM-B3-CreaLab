import network
import socket
import time
import machine

from machine import Pin

intled = machine.Pin("LED", machine.Pin.OUT)

ssid = 'ENTER YOUR SSID'
password = 'ENTER YOUR Wi-Fi PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
    <html>
        <head> <title>Pico W</title> </head>
        <body> <h1>Pico W</h1>
            <p>Hello World</p>
            <p>
            <a href='/light/on'>Turn Light On</a>
            </p>
            <p>
            <a href='/light/off'>Turn Light Off</a>
            </p>
            <br>
        </body>
    </html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

stateis = ""

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print('led on = ' + str(led_on))
        print('led off = ' + str(led_off))

        if led_on == 6:
            print("led on")
            intled.value(1)
            stateis = "LED is ON"

        if led_off == 6:
            print("led off")
            intled.value(0)
            stateis = "LED is OFF"

        response = html + stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
