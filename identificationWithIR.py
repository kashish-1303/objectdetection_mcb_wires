import cv2
import serial
import numpy as np
import roboflow
from roboflow import Roboflow

# Constants for IR footage
BAUD_RATE = 962100
DATA_LENGTH = 2064
IR_IMAGE_SIZE = 32
COLOR_MAP = ["FFFEFB", "FFFCEC", "FFFAE1", "FFF8D6", "FFF7CC", "FFF5C1", "FFF3B6", "FFF2AE", "FFF0A2", "FFEE9A", "FFED90", "FFEB88", "FFEA80", "FFE97A", "FFE871", "FFE66A", "FFE562", "FFE45C", "FFE355", "FFE250", "FFE14A", "FFE045", "FFDF3F", "FFDF3A", "FFDE35", "FFDD31", "FFDC2E", "FFDC2A", "FFDB27", "FFDB23", "FFDA21", "FFDA1D", "FFD91C", "FFD91A", "FFD918", "FFD916", "FFD815", "FFD814", "FFD814", "FFD813", "FFD813", "FFD813", "FFD713", "FED613", "FED513", "FED413", "FED313", "FED213", "FDD114", "FDD014", "FDCF14", "FDCF14", "FDCE14", "FCCD14", "FCCC14", "FCCB14", "FCCA14", "FCC914", "FBC814", "FBC814", "FBC614", "FBC514", "FBC514", "FAC415", "FAC315", "FAC215", "FAC115", "F9C015", "F9BF15", "F9BE15", "F9BD15", "F9BC15", "F8BB15", "F8BB15", "F8BA15", "F8B915", "F8B815", "F7B716", "F7B616", "F7B516", "F7B416", "F7B316", "F6B216", "F6B216", "F6B016", "F6AE16", "F5AB16", "F5A916", "F5A717", "F4A517", "F4A317", "F4A017", "F39E17", "F39C17", "F39917", "F39718", "F29518", "F29318", "F29118", "F18E18", "F18C18", "F18918", "F08719", "F08519", "F08319", "F08119", "EF7E19", "EF7C19", "EF7919", "EE771A", "EE751A", "EE731A", "ED711A", "ED6E1A", "ED6C1A", "EC691A", "EC671B", "EC651B", "EC631B", "EB611B", "EB5E1B", "EB5C1B", "EA5A1B", "EA581C", "EA551C", "E9531C", "E9501C", "E94E1C", "E94C1C", "E84A1C", "E8471D", "E8461D", "E7431D", "E7411E", "E63F21", "E43D24", "E43C27", "E23A2B", "E1392E", "E03731", "DF3634", "DD3448", "DC323B", "DB313E", "DA2F41", "D92E44", "D82C48", "D72B4A", "D5294F", "D42751", "D32655", "D22458", "D1225B", "D0215F", "CE1F63", "CD1D65", "CC1C69", "CB1A6C", "CA196F", "C91772", "C71576", "C61479", "C5127C", "C41080", "C30F82", "C20D86", "C10C88", "BF0A8C", "BE0890", "BD0793", "BC0597", "BA039A", "B9029D", "B901A0", "B500A1", "B300A0", "B000A0", "AD009F", "A9009F", "A7009E", "A3009E", "A0009D", "9D009D", "9A009C", "97009C", "94009B", "91009B", "8D009A", "8B009A", "870099", "840099", "810098", "7E0098", "7B0097", "780097", "750096", "710096", "6F0095", "6C0095", "690094", "660094", "620093", "600093", "5D0092", "5A0092", "570091", "530091", "500090", "4E0090", "4A008F", "47008F", "44008E", "41008E", "3E008D", "3B008C", "390088", "380086", "370083", "35007F", "34007C", "320078", "310075", "300072", "2E006E", "2D006B", "2B0068", "2A0064", "290061", "27005D", "26005A", "240056", "230053", "220050", "20004D", "1E0049", "1D0046", "1C0042", "1A003F", "19003B", "180038", "160034", "150032", "13002E", "12002B", "100027", "0F0024", "0E0021", "0C001D", "0B001A", "090015", "080013", "060010", "05000D", "040009", "020006", "010002"]
cid_rgb = [tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) for color in COLOR_MAP]

# Serial port initialization
ser = serial.Serial("/dev/ttyS0", BAUD_RATE, timeout=0, parity=serial.PARITY_NONE, stopbits=1)

# Initialize Roboflow
rf = Roboflow(api_key="UKEVAtw2aKclIfdxx2kA")
project = rf.workspace().project("electrical-grid-maintenance")
model = project.version(2).model
model.confidence = 30
model.overlap = 25

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Resolution
desired_resolution = (640, 480)

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

    # Read IR data
    data = ser.read(DATA_LENGTH)
    if (data) == DATA_LENGTH and data[0] == 0xfe and data[1] == 0x32:
        temperatures = np.frombuffer(data[2:2050], dtype='int16') / 10.0
        max_temp = np.max(temperatures)
        min_temp = np.min(temperatures)
        temperature_range = max_temp - min_temp
        normalized_temperatures = ((temperatures - min_temp) * 255) / temperature_range
        pixel_colors = [cid_rgb[int(val)] for val in normalized_temperatures]
        ir_frame = np.array(pixel_colors).reshape(IR_IMAGE_SIZE, IR_IMAGE_SIZE, 3).astype('uint8')

        # Resize IR footage to match webcam resolution
        ir_frame = cv2.resize(ir_frame, desired_resolution, interpolation=cv2.INTER_LINEAR)

    # Display the resulting frame with object detection and IR overlay
    cv2.imshow('Combined Footage', cv2.addWeighted(frame, 0.5, ir_frame, 0.5, 0))

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()