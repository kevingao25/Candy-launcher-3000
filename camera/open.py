import cv2
import imutils
import time
import numpy as np
from imutils.object_detection import non_max_suppression
from imutils import paths

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

count = 0;

time.sleep(2)

while True:
    success,img = cap.read()

    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4),padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
   
    if count == 10:
        print("Candy time ")
        print("Saving image..")
        cv2.imwrite('../web/server_images/recent.jpg', img)
        print("Image saved")
        count = count + 1
    elif len(pick) >= 1:
        count = count + 1
    else:
        count = 0

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("Video", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
