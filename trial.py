import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Tkinter setup
root = tk.Tk()
root.title("Circle Radius Detector")

framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)

# Conversion factor (adjust this based on your calibration)
conversion_factor = 0.02  # Example: 1 cm = 50 pixels => 0.02 cm/pixel
detected_circle = False  # To keep track of circle detection

def empty(a):
    pass

cv2.namedWindow("parameters")
cv2.resizeWindow("parameters", 640, 240)
cv2.createTrackbar("threshold", "parameters", 63, 255, empty)
cv2.createTrackbar("threshold2", "parameters", 21, 255, empty)

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img, imgContour):
    global detected_circle
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    detected_circle = False  # Reset detection flag

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # Circle detection using minEnclosingCircle
            if len(approx) > 4:
                (x_center, y_center), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x_center), int(y_center))
                radius = int(radius)

                # Convert radius to centimeters
                radius_cm = radius * conversion_factor

                # Draw the center point (Red dot)
                cv2.circle(imgContour, center, 5, (0, 0, 255), -1)

                # Display the radius in cm near the circle
                cv2.putText(imgContour, f"Radius: {radius_cm:.2f} cm", (center[0] - 50, center[1] - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                detected_circle = True  # Circle detected

# Function to handle button click
def radius_button_clicked():
    if detected_circle:
        messagebox.showinfo("Circle Detected", "A circle has been detected!")
    else:
        messagebox.showwarning("No Circle", "No circle detected. Please try again.")

# Create a button that will call the function to show the radius when clicked
radius_button = tk.Button(root, text="Check Radius", command=radius_button_clicked)
radius_button.pack(pady=20)

# Hide button initially
radius_button.config(state=tk.DISABLED)

while True:
    success, img = cap.read()
    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("threshold", "parameters")
    threshold2 = cv2.getTrackbarPos("threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)
    imgStack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgContour]))

    # Update the button state based on circle detection
    if detected_circle:
        radius_button.config(state=tk.NORMAL)
    else:
        radius_button.config(state=tk.DISABLED)

    cv2.imshow("result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
root.mainloop()
