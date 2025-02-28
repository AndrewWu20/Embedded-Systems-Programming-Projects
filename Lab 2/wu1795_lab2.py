from machine import Pin, Timer, ADC, PWM, RTC

def get_date_and_time():
    year = int(input("Year? "))
    month = int(input("Month? "))
    day = int(input("Day? "))
    weekday = int(input("Weekday? "))
    hour = int(input("Hour? "))
    minute = int(input("Minute? "))
    second = int(input("Second? "))
    microsecond = int(input("Microsecond? "))
    rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))
    return rtc

def display_time(timer):
    current_time = rtc.datetime()
    print(str(current_time[1]) + "/" + str(current_time[2]) + "/" + str(current_time[0]))
    print(str(current_time[4]) + ":" + str(current_time[5]) + ":" + str(current_time[6]) + ":" + str(current_time[7]))

def button_switch(pinRead):
    global control_mode
    global button_pressed
    button_pressed = True
    control_mode = not control_mode

def mode(timer):
    value = pot.read()/4095
    if(button_pressed):
        if(control_mode):
            led.freq(int(value * 30) + 1)
        else:
            led.duty(int(1023 * value))

if __name__ == "__main__":
    rtc = RTC()
    timer_1 = Timer(0)
    timer_2 = Timer(1)
    pot = ADC(Pin(34))
    pot.atten(pot.ATTN_11DB)
    led = PWM(Pin(8))
    led.freq(10)
    led.duty(512)    
    control_mode = False
    button_pressed = False
    button = Pin(38, Pin.IN)
    
    button.irq(trigger=Pin.IRQ_RISING, handler=button_switch)
    timer_2.init(mode=Timer.PERIODIC, period=100, callback=mode)
    rtc = get_date_and_time()
    timer_1.init(mode=Timer.PERIODIC, period=30000, callback=display_time)
    while True:
        pass