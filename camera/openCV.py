import cv2
import imutils
import time
import numpy as np
import pickle

# Load the cascade
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

time.sleep(1)

avg = None
text = "Nothing"

# Facial recognition
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"Person_name": 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}
# To capture video from webcam.
cap = cv2.VideoCapture(0)


def facial_recognition():
    # Facial detection and recognition
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        # print(x, y, w, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        # Print name of face
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(img, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_color)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


while True:
    # Get array of image
    success, img = cap.read()

    # openCV stuff
    # frame = imutils.resize(img, width=500)

    frame = img.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Get first frame if not inited
    if avg is None:
        print("Starting background model")
        avg = gray.copy().astype("float")
        continue

    # openCv stuff
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 5000:
            text = "Nothing"
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Motion Detected"

    print(text)

    # Facial detection and recognition
    facial_recognition()

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
