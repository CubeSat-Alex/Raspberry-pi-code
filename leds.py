import RPi.GPIO as GPIO
import enum


class Leds(enum.Enum):
   GREEN = 18
   RED = 23
   BLUE = 24
   YELLOW = 25


class ModesLed:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Leds.GREEN.value , GPIO.OUT)
        GPIO.setup(Leds.RED.value , GPIO.OUT)
        GPIO.setup(Leds.BLUE.value , GPIO.OUT)
        GPIO.setup(Leds.YELLOW.value , GPIO.OUT)
        
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
leds.allOn()

            
        
        