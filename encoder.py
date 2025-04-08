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

        self.encoder_lx = RotaryEncoder(5, 6, max_steps=0)
        self.encoder_rx = RotaryEncoder(16, 26, max_steps=0)

        self.distance = 0
        self.distop = False

        self.rotation = 0
        self.rotstop = False

    async def Distance(self):
        step_start = (self.encoder_lx.steps + (self.encoder_rx.steps * -1) / 2)
        while (self.distop == False):
           step = (self.encoder_lx.steps + (self.encoder_rx.steps * -1) / 2)
           self.distance = (((step - step_start) / self.ppr) / self.gear_ratio) * math.pi * self.weel_diameter #mm weel diameter
           await asyncio.sleep(0)

    def getDistance(self, reset):
        if (reset):
            self.distop = True
            time.sleep(0)
            self.distop = False
        return self.distance 
    
    def dis(self, start, actual):
        distance = (((actual - start) / self.ppr) / self.gear_ratio) * math.pi * self.weel_diameter #mm weel diameter
        return distance
    def print(self):
        print(f"lx: {self.encoder_lx.steps} rx: {self.encoder_rx.steps}")

    async def Rotation_turn(self):
        step_start_lx = self.encoder_lx.steps
        step_start_rx = self.encoder_rx.steps * -1
        while (self.rotstop == False):
            step_lx = self.encoder_lx.steps
            step_rx = self.encoder_rx.steps * -1
            self.rotation = ((self.dis(step_start_lx, step_lx) - self.dis(step_start_rx, step_rx)) / self.axel_track) * (180 / math.pi)
            await asyncio.sleep(0)

    async def Rotation_steer(self):
        step_start_lx = self.encoder_lx.steps
        step_start_rx = self.encoder_rx.steps
        while (self.rotstop == False):
            step_lx = self.encoder_lx.steps
            step_rx = self.encoder_rx.steps
            self.rotation = ((self.dis(step_start_lx, step_lx) + self.dis(step_start_rx, step_rx)) / self.axel_track) * (180 / math.pi)
            await asyncio.sleep(0)

    def getRotation(self, reset):
        if (reset):
            self.distop = True
            time.sleep(0)
            self.distop = False
        return self.rotation
            
    def cleanup(self):
        self.encoder_lx.close()
        self.encoder_rx.close()