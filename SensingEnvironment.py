from sense_emu import SenseHat
import time
from time import asctime

sense = SenseHat()

while True:
    temp = round(sense.get_temperature())
    humidity = round(sense.get_humidity())
    pressure = round(sense.get_pressure())
    message = 'T=%dC, H=%d, P=%d' %(temp,humidity,pressure)
    sense.show_message(message,scroll_speed=(.1),text_colour=[200,240,200])
    time.sleep(2)
    log = open('SensingResult.txt',"a")
    now = str(asctime())
    log.write(now+' '+message+'\n')
    print(message)
    log.close()
    time.sleep(1)

