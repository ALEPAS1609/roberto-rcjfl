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

        self.encoder_lx = RotaryEncoder(24, 25, max_steps=0)
        self.encoder_rx = RotaryEncoder(24, 25, max_steps=0)

        self.angle = 0

    async def rpm(self):
        pass

    def cleanup(self):
        encoder.close()