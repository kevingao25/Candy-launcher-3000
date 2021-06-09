import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

blockerServo = GPIO.PWM(11,50)
tensionServo = GPIO.PWM(13, 50)

blockerServo.start(0)
tensionServo.start(0)

time.sleep(0.1)

# rotate to starting position.

tensionServo.ChangeDutyCycle(12)
blockerServo.ChangeDutyCycle(12)


# TODO: comment movement code back in once we know where the starting positions are(we might not want to start at duty 2), adjust waiting times if too slow or too fast

# rotate blocker 90, duty 7
blockerServo.ChangeDutyCycle(8)
time.sleep(0.4)
blockerServo.ChangeDutyCycle(0)

# rotate tension 180, duty 2
tensionServo.ChangeDutyCycle(2)
time.sleep(0.7)

# rotate blocker back to original position, duty 12
blockerServo.ChangeDutyCycle(12)
time.sleep(0.4)
blockerServo.ChangeDutyCycle(0)

# CANDY GO FLING

# rotate tension servo back to original position, duty 12
tensionServo.ChangeDutyCycle(12)
time.sleep(0.7)

# stop the servos

tensionServo.stop()
blockerServo.stop()
GPIO.cleanup()
print("Catapult.py finished!")
