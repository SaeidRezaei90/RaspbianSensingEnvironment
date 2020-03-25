import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sense_emu import SenseHat
import time
from time import asctime

sense = SenseHat()

fromaddr = "saeid69.rezaei@gmail.com"
toaddr = "saeid70.rezaei@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Temp Raspbian"

temp = round(sense.get_temperature())
humidity = round(sense.get_humidity())
pressure = round(sense.get_pressure())
message = 'T=%dC, H=%d, P=%d' %(temp,humidity,pressure)
print(message)
msg.attach(MIMEText(message,'plain'))

server = smtplib.SMTP('smtp.gmail.com',25)
server.starttls()
server.login(fromaddr,'Pass')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()