import cv2
import mediapipe as mp
import pyautogui

# Capture video from webcam
cam = cv2.VideoCapture(0)

# Initialize face mesh model
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get screen size
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    # Get frame dimensions
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                # Map facial landmark coordinates to screen coordinates
                screen_x = 100
                screen_y = 100
                lx = landmark.x
                ly = landmark.y
                # print(lx," ___ " ,ly)

                n1 = 0.05
                n2 = 0.1
                
                if landmark.x < 0.5 and landmark.x > n2 :
                    screen_x = screen_w * (landmark.x-n1)
                elif landmark.x < n2 :
                    screen_x = screen_w * (landmark.x-n2)

                if landmark.y < 0.5 and landmark.y > n2:
                    screen_y = screen_h * (landmark.y-n1)
                elif landmark.y < n2 :
                    screen_y = screen_h * (landmark.y-n2)

                if landmark.x > 0.5 and landmark.x < 0.8 :
                    screen_x = screen_w * (landmark.x+n1)
                elif landmark.x > 0.8 :
                    screen_x = screen_w * (landmark.x+n2)

                if landmark.y > 0.5 and landmark.y < 0.8:
                    screen_y = screen_h * (landmark.y+n1)
                elif landmark.y > 0.8 :
                    screen_y = screen_h * (landmark.y+n2)

                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))


        distance_diff = 0.006 # 0.004
        if (left[0].y - left[1].y) < distance_diff:
            pyautogui.click()
            pyautogui.sleep(1)

    cv2.imshow('Eye Controlled Mouse', frame)

    cv2.waitKey(1)
