import cv2
import mediapipe as mp
import math
import numpy as np
from serial import Serial
import time

# Inicializa MediaPipe Face Detection e Drawing utils
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

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

def process_static_images(image_files, output_dir='/tmp'):
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        for idx, file in enumerate(image_files):
            image = cv2.imread(file)
            # Converte a imagem de BGR para RGB e processa com MediaPipe Face Detection
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Desenha as detecções de cada rosto
            if not results.detections:
                continue
            annotated_image = image.copy()
            for detection in results.detections:
                print('Nose tip:')
                print(mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
                mp_drawing.draw_detection(annotated_image, detection)
            cv2.imwrite(f'{output_dir}/annotated_image{idx}.png', annotated_image)

def process_webcam_input():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # Se estiver carregando um vídeo, use 'break' em vez de 'continue'.
                continue

            # Para melhorar o desempenho, opcionalmente marque a imagem como não gravável para
            # passar por referência.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            # Desenha as anotações de detecção de rosto na imagem.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
            # Inverte a imagem horizontalmente para uma exibição tipo selfie.
            cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

mphands = mp.solutions.face_mesh
hands = mphands.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

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
    piscando = False
    blinkCount = 0
    calibrating = True

    arduino = Serial("COM11", 9600)

    closed_eye_start_time = None
    eye_closed_duration = 0.8

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
                if ratioMapped < openedEyes and piscando == False:
                    blinkCount += 1
                    openedEyes = ratioMapped
                    piscando = True

                if ratioMapped >= closedEyes and piscando == True:
                    closedEyes = ratioMapped
                    piscando = False

                if blinkCount >= 5:
                    blinkMap = closedEyes + (openedEyes - closedEyes) / 2
                    calibrating = False
                    blinkCount = 0
            else:    
                framergb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                                
                            
                        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        print("x = ", x)
                        print("y = ", y)
                        print("mid x = ", cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
                        print("mid y = ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
                if not calibrated:
                    initial_eye_position[0] = face_landmarks[0].x
                    initial_eye_position[1] = face_landmarks[0].y
                    calibrated = True
                    
                if ratioMapped < blinkMap and piscando == False:
                    piscando = True
                    closed_eye_start_time = time.time()

                if ratioMapped >= blinkMap + 1 and piscando == True:
                    piscando = False
                    closed_eye_start_time = None

                if (
                    piscando
                    and closed_eye_start_time is not None
                    and (time.time() - closed_eye_start_time) >= eye_closed_duration
                ):
                    blinkCount += 1
                    piscando = False
                    closed_eye_start_time = None
                    arduino.write(b"1")    
                    
                # while initial_eye_position[0] != face_landmarks[0].x:
                #     turn_servo_horizontal(arduino, face_landmarks, initial_eye_position[0]) 
                
                
            font = cv2.FONT_HERSHEY_SIMPLEX

            if calibrating:
                cv2.putText(
                    image,
                    "Pisque para calibrar o dispositivo",
                    (50, 50),
                    font,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
            else:
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

            cv2.imshow("MediaPipe Face Mesh", image)

            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

    cap.release()


if __name__ == "__main__":
    main()
    # Lista de arquivos de imagem para processar
    IMAGE_FILES = []
    process_static_images(IMAGE_FILES)
    process_webcam_input()
