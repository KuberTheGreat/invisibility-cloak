# importing libraries
import cv2
import time
import numpy as np

# coding the format of the video, in xvid using cv2
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# storing output in variable and file of window size 640-480
output_file = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

# starts the camera and captures the video
capture = cv2.VideoCapture(0)
# stops the code from executing for 2 seconds
time.sleep(2)

bg = 0
# runs loop for 60 frames to capture the background image as soon as the camera is turned on
for i in range(60):
    # reads and stores the image in the variables
    ret, bg = capture.read()
# flips the image to invert it
bg = np.flip(bg, axis = 1)

# loop for as long as the video is being captured
while (capture.isOpened()):
    # reads and stores the image or video in the variables
    ret, img = capture.read()
    # if not able to capture then break the loop and end the program
    if not ret:
        break
    # flips the images frame by frame
    img = np.flip(img, axis = 1)

    # converts the color captured to hsv format (hue, saturation, value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # values for the range of red colors 
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 50, 255])

    # mask for whichever part is red is invisibled 
    mask1 = cv2.inRange(hsv, lower_black, upper_black)
    mask2 = cv2.inRange(hsv, lower_black, upper_black)

    # merges the 2 masks
    mask1 = mask1 + mask2

    # segments the image, adds filters and dilution to the image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(img, img, mask = mask2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)

    # final output is made and both res are added to it
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    # final output is written in the output file
    output_file.write(final_output)

    # shows the window title and the output in the window
    cv2.imshow('Invisible project', final_output)
    cv2.waitKey(1)

# releases the data and destroys all the windows
capture.release()
output.release()
cv2.destroyAllWindows()