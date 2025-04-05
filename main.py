#from drivebase import DriveBase
from encoder import Encoder
import numpy as np
import time

encoder = Encoder()
try:
    #drive = DriveBase()
    
    while True:
        #drive.run(0, 0)
        time.sleep(0.02)
        encoder.print()



except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping motors...")


finally:
    #drive.stop()       # Stop motors
    #drive.cleanup()    # Clean up GPIO
    encoder.cleanup()
    print("GPIO cleanup complete. Exiting program.")        
