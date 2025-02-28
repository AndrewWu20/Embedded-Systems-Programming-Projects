from neopixel import NeoPixel
from machine import Pin
from time import sleep

led = Pin(0, Pin.OUT)

led_power = Pin(2, Pin.OUT)
led_power.value(1)

neopixel = NeoPixel(led, 1)

button = Pin(38, Pin.IN)
times_pressed = 0

while times_pressed < 5:
    pressed = button()
    if pressed == False:
        times_pressed += 1
        neopixel[0] = (0, 255, 0)
        neopixel.write()
        sleep(1)
    else:
        neopixel[0] = (255, 0, 0)
        neopixel.write()

neopixel[0] = (0, 0, 0)
neopixel.write()
print('You have successfully implemented LAB1!')