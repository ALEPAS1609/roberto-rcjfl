import RPi.GPIO as GPIO
from encoder import Encoder
import time
import asyncio

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

    async def straight(self, speed, distance):
        start = ((encoder.lx() + encoder.rx()) / 2)
        print(start)
        while(encoder.getDistance(start)<distance):
            self.run(speed, 0)
        print(encoder.getDistance(start))
        self.stop()
        self.print()

    async def turn(self, speed, angle):
        start_l = encoder.rx()
        start_r = encoder.rx()
        if angle > 0:
            while(encoder.getAngle_turn(start_l, start_r) < angle):
                self.run(speed, 180)
        else:
            while(encoder.getAngle_turn(start_l, start_r) > angle):
                self.run(speed, -180)
        self.stop()

    async def steer(self, speed, angle):
        start_l = encoder.rx()
        start_r = encoder.rx()
        if(angle >0):
            while(encoder.getAngle_steer(start_l, start_r) < angle):
                self.run(speed, 90)
        else:
            while(encoder.getAngle_steer(start_l, start_r) > angle):
                self.run(speed, -90)
        self.stop()

    def print(self):
        encoder.print()

    async def test(self):
        while(encoder.lx()<11):
            self.run(50, 0)
        self.stop()
        

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

