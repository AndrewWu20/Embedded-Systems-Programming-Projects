import network
import esp32
import socket
from machine import Timer

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
    
def Sensor_data(Timer):
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print(temp)
    print(hall)
    
    sock = socket.socket()
    address = socket.getaddrinfo("api.thingspeak.com", 80)[0][-1]
    host = "api.thingspeak.com"
    sock.connect(address)
    path = "api_key=GDM2DD9BF23JN4PC&field1=" + str(temp) + "&field2=" + str(hall)
    sock.send(bytes("GET /update?%s HTTP/1.0\r\nHost: %r\r\n\r\n" %(path, host), "utf8"))
    sock.close()
    
    

if __name__ == "__main__":
    Connect_to_internet()
    timer_0 = Timer(0)
    timer_0.init(period=30000, mode=Timer.PERIODIC, callback=Sensor_data)
    
    while(True):
        pass