
from ultralytics import YOLO
import cv2
import roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="UKEVAtw2aKclIfdxx2kA")
project = rf.workspace().project("electrical-grid-maintainance")
model =project.version(2).model

# Load the YOLOv8 model


# optionally, change the confidence and overlap thresholds
# values are percentages
model.confidence = 30
model.overlap = 25

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Predict on the frame
    prediction = model.predict(frame)
    for pred in prediction:
        x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{pred['class']} {pred['confidence']:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Object Detection', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()