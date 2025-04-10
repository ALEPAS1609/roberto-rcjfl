from drive_base import DriveBase
import cv
import numpy as np

def main():
    camera = cv.VideoCapture(0)  # 0 is the default camera (usually the first USB camera)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, 360)



    # Variables to store the last detected position
    x_last = 320
    y_last = 180
    
    lower_black= np.array([0,0,0])
    higher_black= np.array([60,60,60])
    lower_silver= np.array([110,110,110])
    higher_silver= np.array([180,180,180])
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    lower_red = np.array([0, 65, 75]) #hsv
    upper_red = np.array([20, 100, 100]) #hsv

    try:
        while True:
            ret, image = camera.read()
            if not ret:
                break

            redpiece = cv.inRange(image, (190, 0, 0), (255, 90, 90))
            if np.count_nonzero(redpiece)>4000:
                arena()

            # detect the black line 
            blackline = cv.inRange(image, lower_black, higher_black)

            #clean up the detected line
            kernel = np.ones((3, 3), np.uint8)
            blackline = cv.erode(blackline, kernel, iterations=5)
            blackline = cv.dilate(blackline, kernel, iterations=9)

            # Find contours in the thresholded image
            contours_blk, _ = cv.findContours(blackline.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # Process the detected contours
            if contours_blk:
                if len(contours_blk) == 1:
                    blackbox = cv.minAreaRect(contours_blk[0])
                else:
                    candidates = []
                    off_bottom = 0
                    for con_num in range(len(contours_blk)): # 4 every figure (contour) detected
                        blackbox = cv.minAreaRect(contours_blk[con_num])
                        (x_min, y_min), (w_min, h_min), _ = blackbox  # Angle is no longer used --> apici del rettangolo che delimita
                        box = cv.boxPoints(blackbox)
                        (x_box, y_box) = box[0]
                        if y_box > 358:                    ##########################   CHANGE    ##########################
                            off_bottom += 1  # 4 every shape too high, increase
                        candidates.append((y_box, con_num, x_min, y_min))
                    candidates = sorted(candidates)  #order from the nearest to the further on y
                    if off_bottom > 1:
                        candidates_off_bottom = []
                        for con_num in range((len(contours_blk) - off_bottom), len(contours_blk)): # 4 every useful shape
                            (y_highest, con_highest, x_min, y_min) = candidates[con_num]
                            total_distance = (abs(x_min - x_last) ** 2 + abs(y_min - y_last) ** 2) ** 0.5
                            candidates_off_bottom.append((total_distance, con_highest)) 
                        candidates_off_bottom = sorted(candidates_off_bottom) #order from the nearest to the further on y AND x
                        (total_distance, con_highest) = candidates_off_bottom[0]
                        blackbox = cv.minAreaRect(contours_blk[con_highest])
                    else:
                        (y_highest, con_highest, x_min, y_min) = candidates[-1]
                        blackbox = cv.minAreaRect(contours_blk[con_highest])

                # Extract information from the bounding box
                (x_min, y_min), (w_min, h_min), _ = blackbox  # Angle is no longer used
                x_last = x_min
                y_last = y_min

                # Calculate the error (deviation from the center)
                setpoint = 320  # Center of the frame (640 / 2)
                error = int(x_min - setpoint)

                # Draw the bounding box on the image
                box = cv.boxPoints(blackbox)
                box = np.int32(box)  # Use np.int32 instead of np.int0
                cv.drawContours(image, [box], 0, (0, 0, 255), 3)

                # Draw the center line of the frame (green vertical line)
                cv.line(image, (setpoint, 0), (setpoint, 360), (0, 255, 0), 2)

                # Draw the center line of the black line (yellow vertical line)
                cv.line(image, (int(x_min), 0), (int(x_min), 360), (0, 255, 255), 2)

                # Draw the error line (blue horizontal line indicating the deviation)
                cv.line(image, (setpoint, int(y_min)), (int(x_min), int(y_min)), (255, 0, 0), 2)

                # Display the error on the image
                cv.putText(image, f"Error: {error}", (10, 320), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Display the processed image
            cv.imshow("Original with Line", image)


            pi_controller = PIController(kp=1.8, ki=0.01)

            # Convert to HSV for better green detection
            image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

            
            
            # Divide image into left and right sectors
            height, width = image_hsv.shape[:2]
            left_hsv = image_hsv[0:height, 0:width//2]
            right_hsv = image_hsv[0:height, width//2:width]

            # Create masks for green color
            left_mask = cv.inRange(left_hsv, lower_green, upper_green)
            right_mask = cv.inRange(right_hsv, lower_green, upper_green)

            gmask = cv.inRange(image_hsv, lower_green, upper_green)
            # Calculate the amount of green pixels in each sector
            left_green_pixels = cv.countNonZero(left_mask)
            right_green_pixels = cv.countNonZero(right_mask)

            # Trova i contorni nell'immagine filtrata
            contours, _ = cv.findContours(gmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            print(contours)
            # Itera sui contorni trovati
            squarecenter=[]
            for contour in contours:
                # Approssima la forma del contorno
                approx = cv.approxPolyDP(contour, 0.04 * cv.arcLength(contour, True), True)
                # Se il contorno ha 4 lati, è un quadrato o simile
                if len(approx) == 4:
                    # Disegna un rettangolo intorno al quadrato trovato
                    x, y, w, h = cv.boundingRect(approx)
                    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), -1)
    
            # Determine rotation direction based on green detection
            if left_green_pixels+50 > right_green_pixels:
                rotation = -30  # Rotate left
            elif right_green_pixels+50 > left_green_pixels:
                rotation = 30   # Rotate right
            else:
                rotation = 0    # No rotation

            #if rotation != 0:
                #drive_base.set_speed(speed_cm_s=0, steering_deg_s=rotation*-0.3)
            #else:
                #drive_base.set_speed(speed_cm_s=14, steering_deg_s=error*-0.3)
            print(error)



    except KeyboardInterrupt:
        # Handle Ctrl+C from the terminal
        print("Ctrl+C pressed. Exiting...")

    finally:
        # Release the camera and close all OpenCV windows
        camera.release()
        cv.destroyAllWindows()
        
        '''
        # Stop the drive base and clean up GPIO
        drive_base.stop()
        drive_base.cleanup()
        '''




    # Release the camera and close all OpenCV windows
    camera.release()
    cv.destroyAllWindows()
'''
if __name__ == "__main__":
    drive_base  DriveBase(wheel_diameter_mm=68, axle_track_mm=183, left_pwm_pin=12, left_dir_pin=13, right_pwm_pin=18, right_dir_pin=19)
    main()
'''
"""
# Initialize drive base in one line
drive_base = DriveBase(wheel_diameter_mm=60, axle_track_mm=120, left_pwm_pin=17, left_dir_pin=18, right_pwm_pin=22, right_dir_pin=23)

# Set speed and steering angle in one line
drive_base.set_speed(speed_cm_s=10, steering_deg_s=10)  # Move forward at 10 cm/s with a left turn

# Stop the drive base
drive_base.stop()

# Clean up GPIO when done
drive_base.cleanup()"
"""
def arena():
    camera = cv.VideoCapture(0)  # 0 is the default camera (usually the first USB camera)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, 360)



    # Variables to store the last detected position
    x_last = 320
    y_last = 180
    
    lower_black= np.array([0,0,0])
    higher_black= np.array([60,60,60])
    lower_silver= np.array([110,110,110])
    higher_silver= np.array([180,180,180])
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    lower_red = np.array([0, 65, 75]) #hsv
    upper_red = np.array([20, 100, 100]) #hsv

    try:
        while True:
            ret, image = camera.read()
            if not ret:
                break

        frame=cv.imread(' ')

        '''
        lower_black= np.array([0,0,0])
        higher_black= np.array([40,40,40])
        lower_silver= np.array([110,110,110])
        higher_silver= np.array([180,180,180])
        '''

        frameblur=cv.bilateralFilter(frame, 15, 1, 20)
        cv.imshow('frameblur', frameblur)

        xtot=500
        ytot=380
        frameless=cv.resize(frameblur,(xtot, ytot))                  #500 380
        cv.imshow('frameless', frameless)

        ##################### PROBLEMI CON L'ARGENTO ######################
        ntot=64
        rang= 256 // ntot
        framechannels= (frameless // rang) * rang
        cv.imshow("framechannels", framechannels)

        #SE NON FA ANCORA CONTATTO
        circles= cv.HoughCircles(                                  #circles(x,y,raggio)
            framechannels, cv.HOUGH_GRADIENT, dp=1, minDist=100,    #1.2
            param1=30, param2=30, minRadius=20, maxRadius=200
        )
        if circles is None:
            #RITORNA 73
            print("73")
        else:
            circles=np.uint(np.around(circles))
            x, y, r = circles[0,0]
            bgr= framechannels[y,x]

            if (bgr[0]>lower_black[0])and (bgr[0]<higher_black[0])and (bgr[1]>lower_black[1])and (bgr[1]<higher_black[1])and (bgr[2]>lower_black[2])and (bgr[2]<higher_black[2]):
                tint=np.array([0,0,0])
                colore='nero'
            elif (bgr[0]>lower_silver[0])and (bgr[0]<higher_silver[0])and (bgr[1]>lower_silver[1])and (bgr[1]<higher_silver[1])and (bgr[2]>lower_silver[2])and (bgr[2]<higher_silver[2]):
                tint=np.array([255,255,255])
                colore='argento'
            value=y-(xtot/2)
            #RITORNA value
            #deve finire il giro prima di chiedere di nuovo 
            #if value < 2  --> vai avanti     RITORNA 0
            #quando la distanza è minore di tot TROVA RETTANGOLO STESSO COLORE


        #SE FA CONTATTO CON LA PALLA TRAMITE SENSORE rbg
        if colore=='nero':
            lower_red = np.array([0,0,230])
            upper_red = np.array([40,40,255])
            mask = cv.inRange(framechannels, lower_red, upper_red)

            # Trova i contorni
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Se ci sono contorni
            if contours:
                # Trova il contorno con l'area maggiore
                largest_contour = max(contours, key=cv.contourArea)

                # Calcola il momento per trovare il centroide
                M = cv.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])  # Coordinata X del centro
                    cy = int(M["m01"] / M["m00"])  # Coordinata Y del centro

                    # Disegna il centro sull'immagine
                    cv.circle(framechannels, (cx, cy), 5, (0, 255, 0), -1)  # Punto verde
                    value=cy-(xtot/2)

        elif colore== 'argento':
            lower_green = np.array([0,230,0])
            upper_green = np.array([40,255,40])
            mask = cv.inRange(framechannels, lower_green, upper_green)

            # Trova i contorni
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Se ci sono contorni
            if contours:
                # Trova il contorno con l'area maggiore
                largest_contour = max(contours, key=cv.contourArea)

                # Calcola il momento per trovare il centroide
                M = cv.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])  # Coordinata X del centro
                    cy = int(M["m01"] / M["m00"])  # Coordinata Y del centro

                    # Disegna il centro sull'immagine
                    cv.circle(framechannels, (cx, cy), 5, (0, 0, 255), -1)  # Punto rosso
                    value=cy-(xtot/2)
    except KeyboardInterrupt:
        # Handle Ctrl+C from the terminal
        print("Ctrl+C pressed. Exiting...")

