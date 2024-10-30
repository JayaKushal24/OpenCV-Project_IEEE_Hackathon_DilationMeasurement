#code to identify the sshape and for finding the area



import cv2
import numpy as np

framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)

def empty(a):
    pass

cv2.namedWindow("parameters")
cv2.resizeWindow("parameters", 640, 240)
cv2.createTrackbar("threshold", "parameters", 63, 255, empty)
cv2.createTrackbar("threshold2", "parameters", 21, 255, empty)

# Conversion factor from pixels to cm (adjust this based on calibration)
pixel_to_cm_ratio = 0.1  # Example: 10 pixels = 1 cm

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0][0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getcontours(img, imgcontour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                  
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgcontour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            x, y, w, h = cv2.boundingRect(approx)

            # Convert area from pixels to cm²
            area_cm2 = (area * (pixel_to_cm_ratio ** 2))

            # Display the area inside the contour in cm²
            cv2.putText(imgcontour, "Area: {:.2f} cm^2".format(area_cm2), (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

            # Shape identification based on number of corners
            if len(approx) == 3:
                shape_type = "Triangle"
            elif len(approx) == 4:
                aspect_ratio = float(w) / h
                if 0.95 < aspect_ratio < 1.05:
                    shape_type = "Square"
                else:
                    shape_type = "Rectangle"
            elif len(approx) > 4:
                shape_type = "Circle"
            else:
                shape_type = "Unknown"
            
            # Display the shape name
            cv2.putText(imgcontour, shape_type, (x + (w // 2) - 20, y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


while True:
    success, img = cap.read()
    imgcontour = img.copy()
    
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("threshold", "parameters")
    threshold2 = cv2.getTrackbarPos("threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getcontours(imgDil, imgcontour)
    imgStack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgcontour, img]))

    cv2.imshow("result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)

def empty(a):
    pass

cv2.namedWindow("parameters")
cv2.resizeWindow("parameters", 640, 240)
cv2.createTrackbar("threshold", "parameters", 63, 255, empty)
cv2.createTrackbar("threshold2", "parameters", 21, 255, empty)

# Conversion factor from pixels to cm (adjust this based on calibration)
pixel_to_cm_ratio = 0.1  # Example: 10 pixels = 1 cm

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0][0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getcontours(img, imgcontour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                  
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgcontour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            x, y, w, h = cv2.boundingRect(approx)

            # Convert area from pixels to cm²
            area_cm2 = (area * (pixel_to_cm_ratio ** 2))

            # Display the area inside the contour in cm²
            cv2.putText(imgcontour, "Area: {:.2f} cm^2".format(area_cm2), (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

            # Shape identification based on number of corners
            if len(approx) == 3:
                shape_type = "Triangle"
            elif len(approx) == 4:
                aspect_ratio = float(w) / h
                if 0.95 < aspect_ratio < 1.05:
                    shape_type = "Square"
                else:
                    shape_type = "Rectangle"
            elif len(approx) > 4:
                shape_type = "Circle"
            else:
                shape_type = "Unknown"
            
            # Display the shape name
            cv2.putText(imgcontour, shape_type, (x + (w // 2) - 20, y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


while True:
    success, img = cap.read()
    imgcontour = img.copy()
    
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("threshold", "parameters")
    threshold2 = cv2.getTrackbarPos("threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getcontours(imgDil, imgcontour)
    imgStack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgcontour, img]))

    cv2.imshow("result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
