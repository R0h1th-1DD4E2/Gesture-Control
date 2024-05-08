import cv2
import mediapipe as mp
import math
import socket
import keyboard
import connect_bot
import popup_box
from dotenv import load_dotenv
import os

load_dotenv()

def bot_command(move: str, pwm: int) -> None:
    msg4robot = ','.join([move,f'{pwm},{pwm},{pwm},{pwm}'])
    print(msg4robot)
    bytesToSend = str.encode(msg4robot)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, robotAddressPort)


def pwm_map(pinch_distance: int) -> int:
    if pinch_distance < 50:
        return 50
    elif pinch_distance > 255:
        return 255
    else:
        return pinch_distance

# Connecting to bot
bot_mac = os.getenv("BOT_MAC")
bot_address = connect_bot.find_device_ip(bot_mac)
if bot_address is None:
    print("Bot was not found. Exiting ....")
    exit()

# Address to communicate
robotAddressPort = (bot_address, 8080)

# Variables for hand tracking
threshold = 250
pwm = 100
Camera_index = 0

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# A popup to the user 
popup_box.popup()

# Initialize VideoCapture
cap = cv2.VideoCapture(Camera_index) # Change the parameter for multiple cameras
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

# Set the desired window size
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.resizeWindow('Hand Tracking', 1280, 720)  # Set the window size to 1280x720

while cap.isOpened():
    global turn
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally (mirror image)
    frame = cv2.flip(frame, 1)
    
    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe Hands
    results = hands.process(image)
    
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
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Left hand gestures
            if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:

                # Check if the index and middle fingers are close together and the pinky and ring fingers are closed
                if  (distance_index_middle < 30) and (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist > threshold):
                    # Combine the distances for pinch zoom control
                    pinch_distance = int((distance_thumb_index + distance_thumb_middle)/2)
                    # print(pinch_distance) # map this to PWM vaule of enable pin
                    pwm = pwm_map(pinch_distance)

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist > threshold):
                    # print('Right')
                    bot_command("RT",pwm)

                if (distance_pinky_wrist > threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    # print('Left')
                    bot_command("LT", pwm)

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    # print('Stop')
                    bot_command("STP", 0)

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist < threshold):
                    # print('Backward')
                    bot_command("BWD", pwm)
                
                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist < threshold):
                    # print('Forward')
                    bot_command("FWD", pwm)
                
                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    pass


            # Right hand gestures
            elif hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
                # print("Right Hand")
                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist > threshold):
                    bot_command("DWRT",pwm)

                if (distance_pinky_wrist > threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    bot_command("DWLT", pwm)

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist > threshold):
                    bot_command("DFRT", 0)

                if (distance_pinky_wrist > threshold) and (distance_ring_wrist > threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    bot_command("DFLT", pwm)

    # Display the output
    cv2.imshow('Hand Tracking', frame)
    
    # Check for key press events
    cv2.waitKey(1)
                
    if keyboard.is_pressed('q'):
        break
    elif keyboard.is_pressed('w') and keyboard.is_pressed('d'):
        bot_command('DFRT', pwm)  # Forward Right
    elif keyboard.is_pressed('w') and keyboard.is_pressed('a'):
        bot_command('DFLT', pwm)  # Forward Left
    elif keyboard.is_pressed('s') and keyboard.is_pressed('d'):
        bot_command('DWRT', pwm)  # Backward Right
    elif keyboard.is_pressed('s') and keyboard.is_pressed('a'):
        bot_command('DWLT', pwm)  # Backward Left
    elif keyboard.is_pressed('w'):
        bot_command('FWD', pwm)  # Forward
    elif keyboard.is_pressed('s'):
        bot_command('BWD', pwm)  # Backward
    elif keyboard.is_pressed('a'):
        bot_command('LT', pwm)   # Left
    elif keyboard.is_pressed('d'):
        bot_command('RT', pwm)   # Right
    elif keyboard.is_pressed(' '):
        bot_command('STP', 0)   # Stop

# Release resources
cap.release()
cv2.destroyAllWindows()
