import time
import numpy as np
import math
from gpiozero import RotaryEncoder
import asyncio

class Encoder:
    def __init__(self):
        self.ppr = 11
        self.gear_ratio = 27
        self.tsample = 0.02
        self.tdisp = 0.5
        self.weel_diameter = 68 #mm
        self.axel_track = 183 # mm

        self.encoder_lx = RotaryEncoder(6, 5, max_steps=0)
        self.encoder_rx = RotaryEncoder(16, 26, max_steps=0)

    
    def Distance(self, start, actual):
        distance = (((actual - start) / self.ppr) / self.gear_ratio) * math.pi * self.weel_diameter #mm weel diameter
        return distance
    
    def lx(self):
        return self.encoder_lx.steps
    
    def rx(self):
        return self.encoder_rx.steps
    
    def print(self):
        print(f"lx: {self.encoder_lx.steps} rx: {self.encoder_rx.steps}")
            
    def cleanup(self):
        self.encoder_lx.close()
        self.encoder_rx.close()