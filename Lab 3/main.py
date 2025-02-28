import network
import time
import neopixel
import ntptime
import machine
import esp32
from machine import RTC, Timer, Pin
import utime

def Connect_to_internet():
    SSID = 'Lab3'
    PASSWORD = 'ECE40862'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('connecting to network...')
        station.connect(SSID, PASSWORD)
        while not station.isconnected():
            pass

    print('network config:', station.ifconfig()[0])


def Display_NTP(timer):
    TZ_Offset = 3600 * -4
    ntptime.host = "pool.ntp.org"
    ntptime.settime()
    
    time_utc = utime.time()
    time_local = time_utc + TZ_Offset
    current_time = utime.localtime(time_local)
    print(str(current_time[1]) + "/" + str(current_time[2]) + "/" + str(current_time[0]))
    print(str(current_time[3]) + ":" + str(current_time[4]) + ":" + str(current_time[5]) + " HRS")    


def Check_touch(timer):
    if touch.read() < 500:
        np[0] = (0, 100, 0)
    else:
        np[0] = (0, 0, 0)
    np.write()


def Deep_sleep(timer):
    print("I am going to sleep for 1 minute.")
    led.value(0)
    machine.deepsleep(60000)


def check_wake_up():
    if machine.reset_cause() != machine.DEEPSLEEP_RESET:
        return
    wake_reason = machine.wake_reason()
    if wake_reason == machine.TIMER_WAKE:
        print("Woke up due to TIMER wake-up.")
    elif wake_reason == machine.EXT0_WAKE:
        print("Woke up due to EXT0 wake-up (switch press).")
        

if __name__ == "__main__":
    check_wake_up()
    
    touch = machine.TouchPad(Pin(4))
    
    led = Pin(13, Pin.OUT)
    led.on()
    
    switch = Pin(14, Pin.IN)
    
    led_np = Pin(0, Pin.OUT)
    led_power = Pin(2, Pin.OUT)
    led_power.value(1)
    np = neopixel.NeoPixel(led_np, 1)
    
    Connect_to_internet()
    rtc = RTC()
    
    timer_0 = Timer(0)
    timer_0.init(period=15000, mode=Timer.PERIODIC, callback=Display_NTP)
    
    timer_1 = Timer(1)
    timer_1.init(period=50, mode=Timer.PERIODIC, callback=Check_touch)
    
    timer_2 = Timer(2)
    timer_2.init(period=30000, mode=Timer.PERIODIC, callback=Deep_sleep)

    esp32.wake_on_ext0(pin=switch, level=esp32.WAKEUP_ANY_HIGH)    
    
    while True:
        pass