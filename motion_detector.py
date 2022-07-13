import RPi.GPIO as GPIO
import time
from picamera import PiCamera

PIR_PIN = 17
YELLOW_LED_PIN = 27
RED_LED_PIN = 22
MOVEMENT_DURATION_THRESHOLD = 3.0
MIN_DURATION_BETWEEN_PHOTOS = 60.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
GPIO.output(RED_LED_PIN, GPIO.LOW)

camera = PiCamera()
camera.resolution = (1280, 720)
camera.rotation = 180
time.sleep(2) # adjust to environment
print("Camera ready...")

movement_start = time.time()
time_last_photo_taken = 0
pir_previous_state = GPIO.input(PIR_PIN)
picture_filename = f"/home/joesharpe/dev/security_system/{int(time.time())}.jpg"

try:
  print("Here we go!\n")
  while True:
    time.sleep(0.01)

    if GPIO.input(PIR_PIN) == GPIO.HIGH:            
      if pir_previous_state == GPIO.LOW:
        GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
        print("Motion Detected!")
        movement_start = time.time()
        movement_already_detected = True
      elif time.time() > movement_start + MOVEMENT_DURATION_THRESHOLD:
        if time.time() > time_last_photo_taken + MIN_DURATION_BETWEEN_PHOTOS:
          GPIO.output(RED_LED_PIN, GPIO.HIGH)
          time_last_photo_taken = time.time()
          print("Photo is being taken...")
          camera.capture(picture_filename)
          GPIO.output(RED_LED_PIN, GPIO.LOW)
    else:
      GPIO.output(YELLOW_LED_PIN, GPIO.LOW)

    pir_previous_state = GPIO.input(PIR_PIN)
except KeyboardInterrupt:
  print("\nGracefully shutting down...")
  GPIO.cleanup()