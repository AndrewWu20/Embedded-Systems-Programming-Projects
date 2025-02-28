Hardware connections:
	ESP32 and MPU6050 3V connected via wire
	ESP32 and MPU6050 GND connected via wire (and via ground rail)
	ESP32 Pin 14 and MPU6050 SCL connected via wire
	ESP32 SDA pin and MPU6050 SDA connected via wire

Limitations:
	My program only seems to work when you start it. If you stop executing and restart the program, 
the acceleration in the z direction becomes extremely large. If you test all of the requirements the first 
time you execute my program, it should work fine. The solution I found was unplugging my usb from my laptop
and waiting a few seconds for the board to fully reset itself before executing again.


https://www.youtube.com/watch?v=2TftW6od1zk