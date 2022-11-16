import RPi.GPIO as GPIO
import http.client 
import urllib 
import time 
import sys 
import Adafruit_DHT 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GAS=26
PIR=21
FAN=19
LAMP=13
RED=23
GREEN=25
LED = 24
BUZZER = 5
DHT = 18
key = '3A09FDC9HTSRWWAL' 


GPIO.setup(PIR,GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(GAS, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(PIR,GPIO.IN)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(LAMP,GPIO.OUT)
GPIO.setup(FAN,GPIO.OUT)




def thermometer(): 
    while True:
        h,t = Adafruit_DHT.read_retry(11,DHT) 
        params1 = urllib.parse.urlencode({'field1': t, 'key':key }) 
        params2 = urllib.parse.urlencode({'field2': h, 'key':key }) 

        headers = {"Content-typZZe": "application/x-www-form- urlencoded","Accept": "text/plain"} 
        conn = http.client.HTTPConnection("api.thingspeak.com:80") 
        try: 
            conn.request("POST", "/update", params1, headers) 
            response = conn.getresponse() 
            print ("Temperature = ", t) 
            #print (response.status, response.reason) 
            data = response.read() 
            conn.close() 

            conn.request("POST", "/update", params2, headers) 
            response = conn.getresponse() 
            print ("Humidity",h) 
            #print (response.status, response.reason) 
            data = response.read() 
            conn.close() 
        except: 
            print ("connection failed") 
        break
    
    
while True:
    print(" ")
    print(" ")
    print("Running DHT Sensor")
    thermometer()
    time.sleep(0.1)
    print(" ")
    print(" ")
    print("Running PIR")
    if (GPIO.input(PIR) == 0):
        print("No Intrueder")
        GPIO.output(LAMP, 0)
        GPIO.output(FAN, 0)
        GPIO.output(LED,0)
        time.sleep(0.5)
    elif (GPIO.input(PIR)== 1):
        print("Intruder Detected")
        GPIO.output(LAMP, 1)
        GPIO.output(BUZZER,1)
        GPIO.output(FAN, 1)
        GPIO.output(LED,1)
        time.sleep(0.5)
    
        
    print("  ")
    print("  ")
    print("Running Gas Sesor")
    if (GPIO.input(GAS) == 0): 
        print ("  Smoke Detected!")
        GPIO.output(BUZZER,1)
        GPIO.output(RED,1)
        GPIO.output(GREEN,0)
        time.sleep(1)
    else: 
        print ("No Smoke Detected!")
        GPIO.output(BUZZER,0)
        GPIO.output(RED,0)
        GPIO.output(GREEN,1)
        time.sleep(1)
        
        





