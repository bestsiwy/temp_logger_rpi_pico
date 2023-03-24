import onewire, ds18x20, time
from gpio_lcd import GpioLcd
from machine import Pin


x = 2  # sleep time [s] between measures
y = 4  # cycles of measure
# measure time = x*y

SensorPin = Pin(26, Pin.IN)  # define sensor inputs pin
alert = Pin(15, Pin.OUT)
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))  # define sensors
roms = sensor.scan()  # lots of sensors by i2c, scan for detect all

lcd = GpioLcd(rs_pin=Pin(16),
                enable_pin=Pin(17),
                d4_pin=Pin(18),
                d5_pin=Pin(19),
                d6_pin=Pin(20),
                d7_pin=Pin(21),
                num_lines=2, num_columns=16)  # define LDC connection using library

temp_list = []  # empty list for temp log
date_list = []  # empty list for date log

with open('output.txt', "w") as file:  # create file to log data
    pass

lcd.putstr('Temp logger')
time.sleep(1.5)

a=0
while True:
    #licznik do testow
    a=a+1
    
    sensor.convert_temp()
    time.sleep(x)
    for rom in roms:
        temperature = round(sensor.read_temp(rom),1)
        lcd.clear()
        lcd.putstr(f'{temperature} Celcius')
        print(temperature,"C")
        temp_list.append(temperature)
        data = "%4d-%02d-%02d %02d:%02d:%02d" % time.localtime()[:6]
        date_list.append(data)
        print(temp_list)
        print(date_list)
    if a==y:
        break

with open('output.txt', "a") as file:
    for i in range(len(temp_list)):
        file.write(date_list[i] + ' ' + str(temp_list[i]) + ' Celcius' + '\n')

lcd.clear()
lcd.putstr('Logging done.')
