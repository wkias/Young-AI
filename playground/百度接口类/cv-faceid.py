import cv2
import matplotlib.pyplot as plt
cap = cv2.VideoCapture(0)
dect = cv2.CascadeClassifier(cv2.data.haarcascades +
                             'haarcascade_frontalface_default.xml')
ret, frame = cap.read()

# while True:
#     ret, frame = cap.read()
#     faces = dect.detectMultiScale(frame)
#     for (x, y, w, h) in faces:
#         frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
#     cv2.imshow('img', frame)
cv2.imshow('img', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
