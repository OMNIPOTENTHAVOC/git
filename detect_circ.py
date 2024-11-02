import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('cir2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to the image to reduce noise
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Use HoughCircles to detect circles
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,                # Inverse ratio of the accumulator resolution to the image resolution
    minDist=150,         # Minimum distance between detected centers
    param1=70,          # Upper threshold for the Canny edge detector
    param2=60,          # Threshold for center detection
    minRadius=0,        # Minimum circle radius
    maxRadius=0         # Maximum circle radius
)

# If some circles are detected, draw them on the image
if circles is not None:
    circles = np.uint16(np.around(circles))  # Convert to integer
    for i in circles[0, :]:
        # Draw the outer circle
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Draw the center of the circle
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

# Display the output
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axis
plt.show()
