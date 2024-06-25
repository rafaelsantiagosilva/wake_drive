import cv2
import mediapipe as mp
from serial import Serial
from time import sleep

mphands = mp.solutions.face_mesh
hands = mphands.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

mid_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
mid_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2

arduino = Serial("COM11", 9600, timeout=0.01)

_, frame = cap.read()

h, w, c = frame.shape

while True:
    _, frame = cap.read()
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_face_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLMs.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                    
                if x > mid_x:
                    arduino.write(b'L')
                elif x < mid_x:
                    arduino.write(b'R')
                
                if y > mid_y:
                    arduino.write(b'U')
                elif y < mid_y:
                    arduino.write(b'D')
                    
                # print(arduino.read())
                    
                
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            mp_drawing.draw_landmarks(frame, handLMs, mphands.FACEMESH_FACE_OVAL)
            print("x = ", x)
            print("y = ", y)
            print("mid x = ", cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
            print("mid y = ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
    cv2.imshow("Frame", frame)
    # sleep(0.3)

    cv2.waitKey(1)