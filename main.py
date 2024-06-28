import cv2
import mediapipe as mp
import math
import numpy as np
from serial import Serial
import time

def map_value(x, in_min, in_max, out_min, out_max):
    """
    Mapeia um valor de um intervalo para outro.
    """
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def detect_face_landmarks(cap, width, height):
    """
    Detecta os marcos faciais na imagem.
    """
    with mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0].landmark
                return image, face_landmarks
    return None, None

def calculate_eye_ratios(face_landmarks, width, height):
    """
    Calcula as razões das distâncias entre os olhos.
    """
    cord1 = _normalized_to_pixel_coordinates(
        face_landmarks[159].x, face_landmarks[159].y, width, height
    )
    cord2 = _normalized_to_pixel_coordinates(
        face_landmarks[145].x, face_landmarks[145].y, width, height
    )
    cord3 = _normalized_to_pixel_coordinates(
        face_landmarks[33].x, face_landmarks[33].y, width, height
    )
    cord4 = _normalized_to_pixel_coordinates(
        face_landmarks[133].x, face_landmarks[133].y, width, height
    )

    dist = math.sqrt((cord1[0] - cord2[0]) ** 2 + (cord1[1] - cord2[1]) ** 2)
    dist2 = math.sqrt((cord4[0] - cord3[0]) ** 2 + (cord4[1] - cord3[1]) ** 2)

    ratio = dist2 / (dist + 0.001)
    return ratio

def draw_eye_lines(image, face_landmarks, width, height):
    """
    Desenha linhas entre os olhos na imagem.
    """
    cord1 = _normalized_to_pixel_coordinates(
        face_landmarks[159].x, face_landmarks[159].y, width, height
    )
    cord2 = _normalized_to_pixel_coordinates(
        face_landmarks[145].x, face_landmarks[145].y, width, height
    )
    cord3 = _normalized_to_pixel_coordinates(
        face_landmarks[33].x, face_landmarks[33].y, width, height
    )
    cord4 = _normalized_to_pixel_coordinates(
        face_landmarks[133].x, face_landmarks[133].y, width, height
    )

    cv2.line(image, cord1, cord2, (255, 0, 0), 4)
    cv2.line(image, cord3, cord4, (0, 0, 255), 4)

def draw_face_coordinates(image, face_landmarks, width):
    """
    Desenha as coordenadas x e y do rosto na imagem.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    x_coord = int(face_landmarks[0].x * width)
    y_coord = int(face_landmarks[0].y * width)
    cv2.putText(image, f'X: {x_coord}, Y: {y_coord}', (50, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

# def turn_servo_horizontal(arduino, face_landmarks, initial_x):
#     """
#     Gira o servo motor horizontalmente com base na posição do rosto.
#     """
#     x_coord = face_landmarks[0].x

#     if x_coord < initial_x:
#         # Mover servo para a esquerda
#         arduino.write(b"L")
#     elif x_coord > initial_x:
#         # Mover servo para a direita
#         arduino.write(b"R")

def _normalized_to_pixel_coordinates(
    normalized_x, normalized_y, image_width, image_height
):
    """
    Converte coordenadas normalizadas para coordenadas de pixel.
    """
    # Normalized coordinates range from 0 to 1, so multiply by image dimensions.
    pixel_x = min(int(normalized_x * image_width), image_width - 1)
    pixel_y = min(int(normalized_y * image_height), image_height - 1)
    return pixel_x, pixel_y

mpface_mesh = mp.solutions.face_mesh
face_mesh = mpface_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5)

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 25.0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    mid_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
    mid_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2
    
    _, image = cap.read()
    h, w, c = image.shape

    ratios = []
    initial_eye_position = [0, 0]
    calibrated = False

    openedEyes = 500
    closedEyes = 0
    blinkMap = 0
    blinking = False
    blinkCount = 0
    calibrating = True

    # arduino = Serial("COM11", 9600)

    closed_eye_start_time = None
    eye_closed_duration = 0.8
    
    font = cv2.FONT_HERSHEY_DUPLEX


    while True:
        image, face_landmarks = detect_face_landmarks(cap, width, height)

        if image is not None and face_landmarks is not None:
            ratio = calculate_eye_ratios(face_landmarks, width, height)
            ratios.append(ratio)

            if len(ratios) == 5:
                ratios.pop(0)

            mediaRatio = np.mean(ratios)
            ratioMapped = map_value(mediaRatio, 0, 40, 40, 0)
            draw_eye_lines(image, face_landmarks, width, height)
            draw_face_coordinates(image, face_landmarks, width)

            if calibrating:
                if ratioMapped < openedEyes and not blinking:
                    blinkCount += 1
                    openedEyes = ratioMapped
                    blinking = True

                if ratioMapped >= closedEyes and blinking:
                    closedEyes = ratioMapped
                    blinking = False

                if blinkCount >= 5:
                    blinkMap = closedEyes + (openedEyes - closedEyes) / 2
                    calibrating = False
                    blinkCount = 0
                    
                cv2.putText(
                    image,
                    "Pisque para calibrar o dispositivo",
                    (50, 50),
                    font,
                    1,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )
                
            else:    
                framergb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result = face_mesh.process(framergb)
                face_landmarks = result.multi_face_landmarks
                if face_landmarks:
                    for faceLMs in face_landmarks:
                        x_max = 0
                        y_max = 0
                        x_min = w
                        y_min = h
                        for lm in faceLMs.landmark:
                            x, y = int(lm.x * w), int(lm.y * h)
                            if x > x_max:
                                x_max = x
                            if x < x_min:
                                x_min = x
                            if y > y_max:
                                y_max = y
                            if y < y_min:
                                y_min = y
                                
                            # if x > mid_x:
                            #     arduino.write(b'L')
                            # elif x < mid_x:
                            #     arduino.write(b'R')
                            
                            # if y > mid_y:
                            #     arduino.write(b'U')
                            # elif y < mid_y:
                            #     arduino.write(b'D')
                                
                            # print(arduino.read())
                                
                            
                        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        print("x = ", x)
                        print("y = ", y)
                        print("mid x = ", cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
                        print("mid y = ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
                        
                # if not calibrated:
                #     initial_eye_position[0] = face_landmarks[0].x
                #     initial_eye_position[1] = face_landmarks[0].y
                #     calibrated = True
                    
                if ratioMapped < blinkMap and not blinking:
                    blinking = True
                    closed_eye_start_time = time.time()

                if ratioMapped >= blinkMap + 1 and blinking:
                    blinking = False
                    closed_eye_start_time = None

                if (
                    blinking
                    and closed_eye_start_time is not None
                    and (time.time() - closed_eye_start_time) >= eye_closed_duration
                ):
                    blinkCount += 1
                    blinking = False
                    closed_eye_start_time = None
                    # arduino.write(b"1")    
                
                cv2.putText(
                    image,
                    f"{blinkCount}",
                    (50, 50),
                    font,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("Wake Drive", image)

            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()

if __name__ == "__main__":
    main()
