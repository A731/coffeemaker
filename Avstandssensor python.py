import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_PUMP = 17
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_PUMP, GPIO.OUT)
def distance():
    # Trigger high
    GPIO.output(GPIO_TRIGGER, True)
 
    # 0.01ms = low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTid = time.time()
    StoppTid = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTid = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StoppTid = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StoppTid - StartTid
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 

if distance()>=5: #5 example value
	GPIO.output(GPIO_PUMP, True)
	time.wait(5)

#if __name__ == '__main__':
#    try:
#        while True:
#            dist = distance()
#            print ("Measured Distance = %.1f cm" % dist)
#            time.sleep(1)
# 
#        # Reset by pressing CTRL + C
#    except KeyboardInterrupt:
#        print("Measurement stopped by User")
#        GPIO.cleanup()
