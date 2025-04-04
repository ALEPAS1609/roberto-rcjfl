from drivebase import DriveBase
from encoder import Encoder
import numpy as np
import time

try:
    drive = DriveBase()
    encoder1 = Encoder(16, 26)  # Encoder 1 sui GPIO17 e GPIO18
    encoder2 = Encoder(5, 6)  # Encoder 2 sui GPIO22 e GPIO23
    while True:
        drive.run(0, 0)
        time.sleep(0.02)
        Encoder.print()
        print(f"Encoder 1 RPM: {encoder1.get_rpm():.2f} | Encoder 2 RPM: {encoder2.get_rpm():.2f}")



except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping motors...")


finally:
    drive.stop()       # Stop motors
    drive.cleanup()    # Clean up GPIO
    Encoder.cleanup()
    print("GPIO cleanup complete. Exiting program.")        
