import network
import time
import neopixel
import machine
import esp32
from machine import RTC, Timer, Pin, SoftI2C, I2C
import urequests as requests
import ujson as json

class MPU:
    # Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81 - 0.4622388
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81 - 0.00479004
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81 + (9.81 - 7.721543) / 2

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)
    
    def gyro(self):
        return self.pitch, self.roll, self.yaw

    def __init_gyro(self):
        # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.yaw_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 131 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 131 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 131 * 0.1

        return gyro_x, gyro_y, gyro_z
    
    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050.')

    # Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)


def calibration():        
    cal_x, cal_y, cal_z = mpu.acceleration()
#     print(cal_x)
#     print(cal_y)
#     print(cal_z)

    print('Calibration complete')
    return (cal_x, cal_y, cal_z)

def Connect_to_internet():
    SSID = 'Lab5'
    PASSWORD = 'ECE40862'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('connecting to network...')
        station.connect(SSID, PASSWORD)
        while not station.isconnected():
            pass

    print('network config:', station.ifconfig()[0])
    
def read_data(timer):
    global motion
    global previous_message
    global on
    global notification
    global timeout

    message = requests.get("http://api.thingspeak.com/channels/2753824/feeds.json?api_key=HW1T7DRENEO9X0AS&results=2")
    data = json.loads(message.content)
    request = int(data["channel"]["last_entry_id"])
    
    if previous_message < request:
        previous_message = request      
        on = not on    
        if(on):
            np[0] = (0, 10, 0)
            notification = 1
            LED.off()
            timeout = time.time()
        else:
            np[0] = (0, 0, 0)
            LED.off()
            notification = 0
        np.write()
    motion = 0

def notifications(timer):
    global motion
    global notification
    global timeout
    
    x, y, z = mpu.acceleration()
    LED.off()
    
    if(time.time() - timeout > 60):
        np[0] = (0, 0, 0)
        notification = 0
        LED.off()
        np.write()
    if(((x + offset_x > 3) or (x + offset_x < -3) or (y + offset_y > 3) or (y + offset_y < -3) or (z + offset_z > 13) or (z + offset_z < 6)) and notification):
        motion = 1
        LED.on()
        message = requests.get("http://maker.ifttt.com/trigger/motion_sensor/with/key/dJCHPB48I3_fiNFuNzUNT2")

if __name__ == "__main__":    
    LED = Pin(13, Pin.OUT)
    LED.off()

    led_np = Pin(0, Pin.OUT)
    led_power = Pin(2, Pin.OUT)
    led_power.value(1)
    np = neopixel.NeoPixel(led_np, 1)
    
    Connect_to_internet()
    
    i2c = SoftI2C(sda=Pin(22), scl=Pin(14))
    mpu = MPU(i2c)
    
    offset_x, offset_y, offset_z = calibration()
    
    previous_message = 0
    on = False
    notification = 0
    timeout = 0
    motion = 0

    timer_0 = Timer(0)
    timer_0.init(period=30000, mode=Timer.PERIODIC, callback=read_data)
    
    timer_1 = Timer(1)
    timer_1.init(period=10, mode=Timer.PERIODIC, callback=notifications)
    
    while(True):
        pass
    