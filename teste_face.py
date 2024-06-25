import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    # x = cap.get()
    # y = cap.get(cv2.CAP_PROP_GIGA_FRAME_OFFSET_Y)
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # print(f'X: {x}')
    # print(f'Y: {y}')
    # print(f'Width: {width}')
    # print(f'Height: {height}')

    success, image = cap.read()
    face_detection_results = face_detection.process(image[:,:,::-1])

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    
    if face_detection_results.detections:
    
      # Iterate over the found faces.
      for face_no, face in enumerate(face_detection_results.detections):
          
          # Display the face number upon which we are iterating upon.
          print(f'FACE NUMBER: {face_no+1}')
          print('---------------------------------')
          
          # Display the face confidence.
          print(f'FACE CONFIDENCE: {round(face.score[0], 2)}')
          
          # Get the face bounding box and face key points coordinates.
          face_data = face.location_data
          
          # Display the face bounding box coordinates.
          print(f'\nFACE BOUNDING BOX:\n{face_data.relative_bounding_box}')
          
          # Iterate two times as we only want to display first two key points of each detected face.
          for i in range(2):
  
              # Display the found normalized key points.
              print(f'{mp_face_detection.FaceKeyPoint(i).name}:')
              print(f'{face_data.relative_keypoints[mp_face_detection.FaceKeyPoint(i).value]}')
          
          print('\n\n\n')

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()