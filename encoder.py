import time
import numpy as np
import math
from gpiozero import RotaryEncoder
import asyncio

class Encoder:
    def __init__(self):
        self.ppr = 11
        self.gear_ratio = 27
        self.weel_diameter = 68 #mm
        self.axel_track = 183 # mm

        self.encoder_lx = RotaryEncoder(6, 5, max_steps=0)
        self.encoder_rx = RotaryEncoder(16, 26, max_steps=0)


    def dis(self, start, actual):
        distance = (((actual - start) / self.ppr) / self.gear_ratio) * math.pi * self.weel_diameter #mm weel diameter
        return distance

    def getDistance(self, start):
        return self.dis(start, ((self.lx() + self.rx()) / 2))
    
    def getAngle_turn(self, start_lx, start_rx):
        return ((self.dis(start_rx, self.rx()) + self.dis(start_lx, self.lx())) / self.axel_track) * (180 / math.pi)
            
    def getAngle_steer(self, start_lx, start_rx):
        return ((self.dis(start_lx, self.lx()) - self.dis(start_rx, self.rx())) / self.axel_track) * (180 / math.pi)
    
    def lx(self):
        return self.encoder_lx.steps
    
    def rx(self):
        return self.encoder_rx.steps
    
    def print(self):
        print(f"lx: {self.encoder_lx.steps} rx: {self.encoder_rx.steps}")
            
    def cleanup(self):
        self.encoder_lx.close()
        self.encoder_rx.close()