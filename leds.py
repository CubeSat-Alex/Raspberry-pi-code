import RPi.GPIO as GPIO
import enum


class Leds(enum.Enum):
   Connection = 18 # connection
   Session = 23 # session 
   Download = 24 # downloading 
   Stream = 0 # streaming


class ModesLed:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Leds.Connection.value , GPIO.OUT)
        GPIO.setup(Leds.Session.value , GPIO.OUT)
        GPIO.setup(Leds.Download.value , GPIO.OUT)
        GPIO.setup(Leds.Stream.value , GPIO.OUT)
        
    def ledOn(self,led):
        GPIO.output(led.value, GPIO.HIGH)
    
    def ledOf(self,led):
        GPIO.output(led.value, GPIO.LOW)
    
    def allOn(self):
        for led in Leds :
            GPIO.output(led.value, GPIO.HIGH)
    
    def allOff(self):
        for led in Leds :
            GPIO.output(led.value, GPIO.LOW )


leds = ModesLed()
leds.allOff()