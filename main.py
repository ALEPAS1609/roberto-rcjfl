from drivebase import DriveBase
from gpiozero import DistanceSensor
import numpy as np
import time
import asyncio

drive = DriveBase()
distance1=DistanceSensor(17, 22)
distance2=DistanceSensor(17, 27)
axel_track = 183 # mm

def obstacle():    
    drive.stop()
    
    asyncio.run(drive.straight(30, -1*(axel_track /2)))
    drive.stop()
    asyncio.run(drive.turn(30, 90))
    while distance2.distance() < 0.05:
        drive.run(30, 0)
    drive.stop()
    asyncio.run(drive.turn(30, -90))
    while distance2.distance() < 0.05:
        drive.run(30, 0)
    drive.stop()
    asyncio.run(drive.turn(30, -90))
    drive.stop()
    while distance2.distance() > 0.05:
        drive.run(30, 0)
    drive.stop()
    drive.turn(30,90)
    drive.stop()

try:
    

    while True:
        if distance1.distance() < 0.05:
            obstacle()
        else:
            drive.run(70, 0)

        



except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping motors...")


finally:
    drive.stop()       # Stop motors
    drive.cleanup()    # Clean up GPIO
    print("GPIO cleanup complete. Exiting program.")        
