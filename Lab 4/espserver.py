import network
import time
import neopixel
import ntptime
import machine
import esp32
from machine import RTC, Timer, Pin
import utime
import socket


# Global variables
temp = 0  # measure temperature sensor data
hall = 0  # measure hall sensor data
red_led_state = '' # string, check state of red led, ON or OFF


def Connect_to_internet():
    SSID = 'Lab4'
    PASSWORD = 'ECE40862'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('connecting to network...')
        station.connect(SSID, PASSWORD)
        while not station.isconnected():
            pass

    print('network config:', station.ifconfig()[0])
    

def Data():
    global temp
    global hall
    global red_led_state
    
    LED = Pin(13, Pin.OUT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',30))
    sock.listen(5)
    
    while(True):
        conn, addr = sock.accept()
        LED_state = conn.recv(1024)
        LED_state = str(LED_state)
        if(LED_state.find('/?red_led=on') == 6):
            red_led_state = "ON"
            LED.value(1)
        elif(LED_state.find('/?red_led=off') == 6):
            red_led_state = "OFF"
            LED.value(0)
            
        temp = esp32.raw_temperature()
        hall = esp32.hall_sensor()
        
        sensor_data = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.send(sensor_data)
        conn.close()
    

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage


if __name__ == "__main__":
    Connect_to_internet()
    Data()
    
    