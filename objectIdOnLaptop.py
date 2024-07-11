import cv2
import roboflow
from roboflow import Roboflow
import numpy as np

# Load the model from Roboflow
rf = Roboflow(api_key="UKEVAtw2aKclIfdxx2kA")
project = rf.workspace().project("electrical-grid-maintainance")
model = project.version(2).model

# Optionally, change the confidence and overlap thresholds
# Values are percentages
model.confidence = 30
model.overlap = 25

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame was successfully captured
    if not ret:
        print("Error: Could not read frame from the webcam.")
        break

    # Convert the frame to a numpy array with the correct data type (uint8)
    frame_np = np.array(frame, dtype=np.uint8)

    # Predict on the frame
    prediction = model.predict(frame_np)

    # Iterate over each prediction and draw a rectangle around the detected object
    for pred in prediction:
        x, y, w, h = int(pred['x']), int(pred['y']), int(pred['width']), int(pred['height'])
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
