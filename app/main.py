import os
import OPi.GPIO as GPIO
from time import sleep          # this lets us have a time delay

GPIO.setboard(GPIO.ZERO)        # Orange Pi Zero board
GPIO.setmode(GPIO.SOC)          # set up SOC numbering

button = GPIO.PA+10             # button  is on PA10
led_button = GPIO.PA+14
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # set PA10 as an output (Status led of board)
GPIO.setup(led_button, GPIO.OUT)

try:
  GPIO.output(led_button, 1)
  while True:
     if GPIO.input(button):      # if pin button == 1
        GPIO.output(led_button, 0)
        print "Button is 1/HIGH/True"
        os.system('fswebcam -r 1280x720 --png 9 --no-banner --no-timestamp --no-shadow --no-info --no-underlay --no-overlay -D 1 -S 5 fswebcam.png')
        os.system('lp -o fit-to-page fswebcam.png')
        for x in range(0, 33):
            GPIO.output(led_button, 1)        # set port/pin value to 1/HIGH/True
            sleep(0.1)
            GPIO.output(led_button, 0)        # set port/pin value to 0/LOW/False
            sleep(0.1)
            GPIO.output(led_button, 1)        # set port/pin value to 1/HIGH/True
            sleep(0.1)
            GPIO.output(led_button, 0)        # set port/pin value to 0/LOW/False
            sleep(0.5)
            GPIO.output(led_button, 1)
     else:
        # print "Button is 0/LOW/False"
        sleep(0.1)              # wait 0.1 seconds

except KeyboardInterrupt:
  GPIO.output(led_button, 0)
  GPIO.cleanup()                # clean up after yourself
  print ("Bye.")
