import RPi.GPIO as GPIO
import time

PIR_PIN = 17
RED_LED_PIN = 27
MOVEMENT_DURATION_THRESHOLD = 3.0
MIN_DURATION_BETWEEN_PHOTOS = 60.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

GPIO.output(RED_LED_PIN, GPIO.LOW)

movement_start = time.time()
time_last_photo_taken = 0
pir_previous_state = GPIO.input(PIR_PIN)

try:
  while True:
    time.sleep(0.01)

    if GPIO.input(PIR_PIN) == GPIO.HIGH:            
      if pir_previous_state == GPIO.LOW:
        GPIO.output(RED_LED_PIN, GPIO.HIGH)
        movement_start = time.time()
        movement_already_detected = True
      elif time.time() > movement_start + MOVEMENT_DURATION_THRESHOLD:
        if time.time() > time_last_photo_taken + MIN_DURATION_BETWEEN_PHOTOS:
          time_last_photo_taken = time.time()
          print("Photo is being taken. It will be sent via email")
    else:
      GPIO.output(RED_LED_PIN, GPIO.LOW)

    pir_previous_state = GPIO.input(PIR_PIN)
except KeyboardInterrupt:
  print("\nGracefully Shutting Down...")
  GPIO.cleanup()