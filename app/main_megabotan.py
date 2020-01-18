# -*- coding: utf-8 -*-
print('Start')
import cv2
import os
import OPi.GPIO as GPIO
from time import sleep
import subprocess
print('Import finished')


def setup_button():
	GPIO.setboard(GPIO.ZERO)        # Orange Pi Zero board
	GPIO.setmode(GPIO.SOC)          # set up SOC numbering
	button = GPIO.PA+10             # button  is on PA10
	led_button = GPIO.PA+14
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # set PA10 as an output (Status led of board)
	GPIO.setup(led_button, GPIO.OUT)
	print('Button ready')
	return button, led_button


def get_camera_image():
	cap = cv2.VideoCapture(0)
	res, raw_image = cap.read()
	print(res)
	cap.release()
	print('Got image {}'.format(raw_image.shape))
	cv2.imwrite("1raw.png", raw_image)
	return raw_image
	

def prepear_image(raw_image):
	gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
	print('Gray image {}'.format(gray.shape))

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	equalized_gray = clahe.apply(gray)
	print('Equalized gray image {}'.format(equalized_gray.shape))

	resized = cv2.resize(equalized_gray, (384*640/480, 384))
	print('Resized image {}'.format(resized.shape))
	return resized


def print_image(prepared_image):
	cv2.imwrite("final.png", prepared_image)
	print('Saved final file')
	os.system('lp final.png')
	print('Sent to printer')


def wait_for_print_finish(led_button):
	while subprocess.check_output(['lpstat', '-R']): # print queue is not empty
		GPIO.output(led_button, 1)
		sleep(0.1)
		GPIO.output(led_button, 0)
		sleep(0.1)


def main():
	print('Main started')
	button, led_button = setup_button()
	try:
		while True:
			GPIO.output(led_button, 1)
			print('Waiting for button')
			GPIO.wait_for_edge(button, GPIO.RISING)
			GPIO.output(led_button, 0)
			raw_image = get_camera_image()
			prepared_image = prepear_image(raw_image)
			print_image(prepared_image)
			wait_for_print_finish(led_button)
	except KeyboardInterrupt:
		print('Keyboard interrupt')
		GPIO.cleanup() 
	finally:
		print('Cleanup')
		GPIO.output(led_button, 0)
		GPIO.cleanup()  # Double cleanup
		print('Finished')


if __name__ == '__main__':
	main()
