import RPi.GPIO as GPIO
import time
from picamera import PiCamera

PICTURE_FILENAME = "/home/joesharpe/dev/security_system/picture_log.jpg"
PIR_PIN = 17
YELLOW_LED_PIN = 27
RED_LED_PIN = 22
MOVEMENT_DURATION_THRESHOLD = 3.0
MIN_DURATION_BETWEEN_PHOTOS = 60.0

def set_up_GPIOs():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
  GPIO.setup(RED_LED_PIN, GPIO.OUT)

  GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
  GPIO.output(RED_LED_PIN, GPIO.LOW)

def set_up_camera():
  print("Setting up camera...")
  global camera 
  camera = PiCamera()
  camera.resolution = (1280, 720)
  camera.rotation = 180
  time.sleep(2) # adjust to environment
  print("Camera ready\n")

def take_photo():
  GPIO.output(RED_LED_PIN, GPIO.HIGH)
  print("Photo is being taken...")
  camera.capture(PICTURE_FILENAME)
  GPIO.output(RED_LED_PIN, GPIO.LOW)

set_up_GPIOs()
set_up_camera()

movement_start = time.time()
time_last_photo_taken = 0
pir_previous_state = GPIO.input(PIR_PIN)

try:
  while True:
    time.sleep(0.01)

    if GPIO.input(PIR_PIN) == GPIO.HIGH:            
      if pir_previous_state == GPIO.LOW:
        GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
        print("Motion Detected!")
        movement_start = time.time()
      elif time.time() > movement_start + MOVEMENT_DURATION_THRESHOLD:
        if time.time() > time_last_photo_taken + MIN_DURATION_BETWEEN_PHOTOS:
          take_photo()
          time_last_photo_taken = time.time()
    else:
      GPIO.output(YELLOW_LED_PIN, GPIO.LOW)

    pir_previous_state = GPIO.input(PIR_PIN)
except KeyboardInterrupt:
  print("\nGracefully shutting down...")
  GPIO.cleanup()