import cv2
import numpy as np
from gui_buttons import Buttons

# OpenCV DNN
net = cv2.dnn.readNet("dnn_model\yolov4-tiny.weights", "dnn_model\yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)

# Load Class Name
classes = []
with open("dnn_model\classes.txt", "r") as file_object:
    for className in file_object.readlines():
        class_name = className.strip()
        classes.append(class_name)

# Get Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# FULL HD 1920 X 1080
# HD 1280 x 720

# button_person = False
button = Buttons()
button.add_button("person", 20, 20)
button.add_button("cell phone", 20, 100)
button.add_button("remote", 20, 180)
def clickButton(event, x, y, flags, params):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x, y)
        # polygon = np.array([[(20, 20), (150, 20), (150, 70), (20, 70)]])
        # is_inside = cv2.pointPolygonTest(polygon, (x, y), False)
        # if is_inside > 0:
        #     if not button_person:
        #         button_person = True
        #     else:
        #         button_person = False


# Creating window
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", clickButton)

while True:
    # Initialize frames
    ret, frame = cap.read()

    # Get active buttons
    active_buttons = button.active_buttons_list()

    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]
        if class_name in active_buttons:
            cv2.putText(frame, class_name, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 30), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (200, 0, 30), 3)
        elif (len(active_buttons) == 0):
            cv2.putText(frame, class_name, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 30), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (200, 0, 30), 3)

    # Creating Buttons
    # cv2.rectangle(frame, (20, 20), (150, 70), (0, 0, 100), -1)
    # polygon = np.array([[(20, 20), (150, 20), (150, 70), (20, 70)]])
    # cv2.fillPoly(frame, polygon, (0,0,100))
    # cv2.putText(frame, "Person", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    button.display_buttons(frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()