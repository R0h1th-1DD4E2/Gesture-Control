import cv2
import mediapipe as mp
import math
import websocket


import find_ip 

# Global Variables 
Camera_index = 0

class HandTrackingController:
    def __init__(self, ws_url):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.pwm = 100
        self.threshold = 250
        self.cap = None
        self.command = "STP"
        self.ws_url = ws_url
        self.ws = websocket.WebSocket()
        self.ws.connect(ws_url)
        self.pwm = 100
    

    def send_command(self, command, pwm_values):
        message = f"{command} {' '.join(map(str, pwm_values))}"
        self.ws.send(message)


    def pwm_map(self,pinch_distance: int) -> int:
        if pinch_distance < 50:
            return 50
        elif pinch_distance > 255:
            return 255
        else:
            return pinch_distance
    

    def gesture_tracking(self, camera_index=0):
        # Initialize VideoCapture
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

        # Set the desired window size
        cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)  # Create a resizable window
        cv2.resizeWindow('Hand Tracking', 1280, 720)  # Set the window size to 1280x720


        # Font and other display settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1 
        self.font_color = (0, 0, 0)
        self.thickness = 2
        self.position = (50, 50)

        while self.cap.isOpened():
            global turn
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip the frame horizontally (mirror image)
            frame = cv2.flip(frame, 1)
            
            # Convert the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the image with MediaPipe Hands
            results = self.hands.process(image)


            # If hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    # Get the hand landmarks
                    landmarks = []
                    for landmark in hand_landmarks.landmark:
                        x, y, _ = image.shape
                        landmarks.append((int(landmark.x * y), int(landmark.y * x)))

                    # Calculate the distances between fingers
                    wrist_tip = landmarks[0]    # Wrist landmark
                    thumb_tip = landmarks[4]  # Thumb tip landmark
                    index_tip = landmarks[8]  # Index finger tip landmark
                    middle_tip = landmarks[12]  # Middle finger tip landmark
                    ring_tip = landmarks[16]    # Ring finger tip landmark
                    pinky_tip = landmarks[20]  # Pinky finger tip landmark

                    # Calculate the distances between fingers
                    distance_thumb_index = int(math.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2))
                    distance_thumb_middle = int(math.sqrt((thumb_tip[0] - middle_tip[0])**2 + (thumb_tip[1] - middle_tip[1])**2))
                    distance_index_middle = int(math.sqrt((index_tip[0] - index_tip[0])**2 + (index_tip[1] - middle_tip[1])**2))

                    distance_thumb_wrist = int(math.sqrt((thumb_tip[0] - wrist_tip[0])**2 + (thumb_tip[1] - wrist_tip[1])**2))
                    distance_index_wrist = int(math.sqrt((index_tip[0] - wrist_tip[0])**2 + (index_tip[1] - wrist_tip[1])**2))
                    distance_middle_wrist = int(math.sqrt((middle_tip[0] - wrist_tip[0])**2 + (middle_tip[1] - wrist_tip[1])**2))
                    distance_ring_wrist = int(math.sqrt((ring_tip[0] - wrist_tip[0])**2 + (ring_tip[1] - wrist_tip[1])**2))
                    distance_pinky_wrist = int(math.sqrt((pinky_tip[0] - wrist_tip[0])**2 + (pinky_tip[1] - wrist_tip[1])**2))

                    # Draw hand landmarks on the frame
                    mp_drawing = mp.solutions.drawing_utils
                    mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Left hand gestures
                    if hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x:

                        # Check if the index and middle fingers are close together and the pinky and ring fingers are closed
                        if  (distance_index_middle < 30) and (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist > self.threshold) and (distance_index_wrist > self.threshold) and (distance_thumb_wrist > self.threshold):
                            # Combine the distances for pinch zoom control
                            pinch_distance = int((distance_thumb_index + distance_thumb_middle)/2)
                            # print(pinch_distance) # map this to PWM vaule of enable pin
                            self.pwm = self.pwm_map(pinch_distance)
                            self.command = "STP"

                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist > self.threshold):
                            # print('Right')
                            self.command = "RT"

                        if (distance_pinky_wrist > self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist < self.threshold):
                            # print('Left')
                            self.command = "LT"

                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist < self.threshold):
                            # print('Stop')
                            self.command = "STP"

                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist > self.threshold) and (distance_thumb_wrist < self.threshold):
                            # print('Backward')
                            self.command = "BWD"
                        
                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist > self.threshold) and (distance_index_wrist > self.threshold) and (distance_thumb_wrist < self.threshold):
                            # print('Forward')
                            self.command = "FWD"
                        
                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist > self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist < self.threshold):
                            pass


                    # Right hand gestures
                    elif hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x:
                        # print("Right Hand")
                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist > self.threshold):
                            self.command = "DWRT"

                        if (distance_pinky_wrist > self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist < self.threshold):
                            self.command = "DWLT"

                        if (distance_pinky_wrist < self.threshold) and (distance_ring_wrist < self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist > self.threshold) and (distance_thumb_wrist > self.threshold):
                            self.command = "DFRT"

                        if (distance_pinky_wrist > self.threshold) and (distance_ring_wrist > self.threshold) and (distance_middle_wrist < self.threshold) and (distance_index_wrist < self.threshold) and (distance_thumb_wrist < self.threshold):
                            self.command = "DFLT"

                    self.send_command(self.command, [self.pwm, self.pwm, self.pwm, self.pwm])

            # Display Text
            cv2.putText(frame, f"Current Command:{self.command}", self.position, self.font, self.font_scale, self.font_color, self.thickness)
            cv2.putText(frame, f"Current PWM: {self.pwm}", (self.position[0], self.position[1] + 30), self.font, self.font_scale, self.font_color, self.thickness)

            # Display the output
            cv2.imshow('Hand Tracking', frame)

            # Check for key press events
            cv2.waitKey(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

esp_ip = find_ip.find_device_ip("bc:ff:4d:f8:02:f1")
handtrack = HandTrackingController(f"ws://{esp_ip}:8080/")
handtrack.gesture_tracking()