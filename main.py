from drivebase import DriveBase
import numpy as np
import time
import asyncio


try:
    drive = DriveBase()

    while True:
        asyncio.run(drive.straight(50, 100))
        drive.print()
        time.sleep(2)
        



except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping motors...")


finally:
    drive.stop()       # Stop motors
    drive.cleanup()    # Clean up GPIO
    print("GPIO cleanup complete. Exiting program.")        
