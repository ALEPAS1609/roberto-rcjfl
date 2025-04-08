import RPi.GPIO as GPIO
from encoder import Encoder
import time

encoder = Encoder()



class DriveBase:
    def __init__(self):
        # Motor LX pins
        self.IN1 = 13  # PWM pin for motor LX
        self.IN2 = 12  # PWM pin for motor LX

        # Motor RX pins
        self.IN3 = 19  # PWM pin for motor RX
        self.IN4 = 18  # PWM pin for motor RX

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        # Initialize PWM for motor LX and RX
        #self.pwm_lx = GPIO.PWM(self.IN1, 1000)  # 1000 Hz frequency
        self.pwm_lx0 = GPIO.PWM(self.IN1, 1000)
        self.pwm_lx1 = GPIO.PWM(self.IN2, 1000)
        self.pwm_rx0 = GPIO.PWM(self.IN3, 1000)
        self.pwm_rx1 = GPIO.PWM(self.IN4, 1000)
        self.pwm_lx0.start(0)    # Start with 0% duty cycle (stopped)
        self.pwm_lx1.start(0)  
        self.pwm_rx0.start(0)
        self.pwm_rx1.start(0)

    def rx(self, speed):
        if speed >=0:
            self.pwm_rx0.ChangeDutyCycle(speed)
            self.pwm_rx1.ChangeDutyCycle(0)
        
        else:
            self.pwm_rx1.ChangeDutyCycle(abs(speed))
            self.pwm_rx0.ChangeDutyCycle(0)

    def lx(self, speed):
        if speed >=0:
            self.pwm_lx0.ChangeDutyCycle(speed)
            self.pwm_lx1.ChangeDutyCycle(0)
        
        else:
            self.pwm_lx1.ChangeDutyCycle(abs(speed))
            self.pwm_lx0.ChangeDutyCycle(0)

    def run(self, speed, angle):

        speedr = speed * ((90-abs(angle))/90)
        if(angle >=0):
            self.lx(speed)
            self.rx(speedr)
        else:
            self.lx(speedr)
            self.rx(speed)

    def straight(self, speed, distance):
        self.stop()
        time.sleep(0)
        self.run(speed, 0)
        encoder.Distance()
        time.sleep(encoder.getDistance(False) < distance)
        self.stop()
        encoder.getDistance(True)



    def turn(self, speed, angle):
        self.stop()
        time.sleep(0)
        if(angle >0):
            self.run(speed, 180)
        else:
            self.run(speed, -180)
        
        encoder.Rotation_turn()
        time.sleep(encoder.getRotation(False) < angle)
        self.stop()
        encoder.getRotation(True)

    def steer(self, speed, angle):
        self.stop()
        time.sleep(0)
        if(angle >0):
            self.run(speed, 90)
        else:
            self.run(speed, -90)
        
        encoder.Rotation_steer()
        time.sleep(encoder.getRotation(False) < angle)
        self.stop()
        encoder.getRotation(True)



    def stop(self):
        """Stop both motors."""
        self.pwm_lx0.ChangeDutyCycle(0)
        self.pwm_lx1.ChangeDutyCycle(0)
        self.pwm_rx0.ChangeDutyCycle(0)
        self.pwm_rx1.ChangeDutyCycle(0)

    def cleanup(self):
        """Clean up GPIO."""
        self.pwm_lx0.stop()
        self.pwm_lx1.stop()
        self.pwm_rx0.stop()
        self.pwm_rx1.stop()
        GPIO.cleanup()
        encoder.cleanup()

