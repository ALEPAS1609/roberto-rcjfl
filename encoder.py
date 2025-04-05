import time
import numpy as np
from gpiozero import RotaryEncoder
import asyncio

class Encoder:
    def __init__(self):
        self.ppr = 11
        self.gear_ratio = 27
        self.tsample = 0.02
        self.tdisp = 0.5
        self.weel_diameter = 68 #mm

        self.encoder_lx = RotaryEncoder(16, 26, max_steps=0)
        self.encoder_rx = RotaryEncoder(5, 6, max_steps=0)

        self.distance = 0
        self.distop = False

    async def Distance(self):
        step_start = (self.encoder_lx.steps + (self.encoder_rx.steps * -1) / 2)
        while (self.distop):
           step = (self.encoder_lx.steps + (self.encoder_rx.steps * -1) / 2)
           self.distance = (((step - step_start) / self.ppr) / self.gear_ratio) * self.weel_diameter #mm weel diameter

    def getDistance(self, reset):
        if (reset):
            self.distop = True
            self.distop = False
        return self.distance

    def print(self):    
        print(f"lx: {self.encoder_lx.steps} rx: {self.encoder_rx.steps}")
        

    def cleanup(self):
        self.encoder_lx.close()
        self.encoder_rx.close()