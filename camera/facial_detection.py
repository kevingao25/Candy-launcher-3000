import cv2
import numpy as np
import pickle

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"Person_name": 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k, v in og_labels.items()}
# To capture video from webcam.
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    # Face recognition
    for (x, y, w, h) in faces:
        #print(x, y, w, h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Print name of face
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_color)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the VideoCapture object
cap.release()