import pycurl
import json
from stringIO import stringIO
import RPi.GPIO as GPIO
from sense_emu import SenseHat
import time
from time import asctime

sense = SenseHat()
sense.clear()

hot = 40
cold = 37
pushMessage = ""

######################################
#Code for display numbers
Offset_Left = 1
Offset_Top = 2

Num=[1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0,   #0
     0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,   #1
     1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1,   #2
     1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,   #3
     1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1,   #4
     1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0,   #5
     1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,   #6
     1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1,   #7
     1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,   #8
     1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, ]  #9

#Display a single diget
def Show_Digit(val,  xd, yd, r, g, b):
    offset = val*15
    for p in range(offset, offset+15):
        xt = p % 3
        yt =(p-offset) // 3
        sense.set_pixel(xt+xd, yt+yd, r*NUM[p], g*NUM[p], b*NUM[p])
        
#Display a two-digits positive number 0-99
def Show_Number(val, r, g, b):
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    if(abs_val > 9): Show_Digit(tens, Offset_Left, Offset_Top, r, g, b)
    Show_Digit(units, Offset_Left+4, Offset_Top, r, g, b)

#########################################
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_humidity()
    message = 'T=%dC,  H=%d,  P=%d' %(temp, humidity, pressure)
    
    #Setup InstaPush variables to send notification for mobile
    #add your instaPush ApplicationID
    appID = "";
    
    #add your instaPush SecretID
    appSecretID = "";
    pushMessage="TempNotify"
    
    #use curl to post to the instapush API
    c = pycurl.Curl()
    
    #set API URL
    c.setopt(c.URL,  'https://api.instapush.im/v1/post')
    
    #setup custom headers for authentication variables and content type
    c.setopt(c.HTTPHEADER, ['x-instapush-appid: '+appID, 
                           'x-instapush-appsecret: ' +appSecretID,  
                           'Content-Type: application/json'])
  
  #use this to capture the response from the push API call
    buffer = stringIO()
    #####################################################3
    #define a function to pass the message
    def p(pushMessage):
        #create a dic struct for the JSON data to post
        json_fields = {}
        
        #setup JSON values
        json_fields['event'] = pushEvent
        json_fields['trackers'] = {}
        json_fields['trackers']['message'] = pushMessage
        postfields = json.dumps(json_fields) #make a json file
        
        #make sure to send the JSON with post
        c.setopt(c.POSTFIELDS,  postfields)
        
        #set this so we can capture the response in the buffer
        c.setopt(c.WRITEFUNCTION, buffer.write)
        
        #uncomment to see the post sent
        c.setopt(c.VERBOSE,  True)
        
    #setup an indefinite loop that looks for temp
        while True:
            temp = round(sense.get_temperature())
            humidity = round(sense.get_humidity())
            pressure = round(sense.get_humidity())
            message = 'T=%dC,  H=%d,  P=%d' %(temp, humidity, pressure)
            time.sleep(3)
            log = open('result', "a")
            now = str(asctime)
            log.write(now + ' ' + message + '\n')
            print(message)
            temp = int(temp)
            Show_Number(temp, 200, 0, 60)
            log.close()
            time.sleep(4)
            
            if temp >=hot:
               pushMessage = "It's hot: " + message
               p(pushMessage)
               c.perform()
               #capture the response from the server
               body = buffer.getvalue()
               pushMessage = ""
               
            elif temp <= cold:
                pushMessage = "It's cold: " + message
                p(pushMessage)
                c.perform()
                #capture the response from the server
                body = buffer.getvalue()
                pushMessage = ""
               
        #reset the buffer
            buffer.truncate(0)
            buffer.seek(0)
            
        #clean
        c.clean()
        GPIO.cleanup()
        
        
            
