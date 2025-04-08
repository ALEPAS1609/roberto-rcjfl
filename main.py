from drivebase import DriveBase
from encoder import Encoder
import numpy as np
import time


try:
    drive = DriveBase()

    while True:
        drive.straight(50, 10)
        time.sleep(2)



except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping motors...")


finally:
    drive.stop()       # Stop motors
    drive.cleanup()    # Clean up GPIO
    Encoder.cleanup() 
    print("GPIO cleanup complete. Exiting program.")        
