import pickle
import cv2
import mediapipe as mp
import numpy as np
import time

def mode(model_path='./mode_training/model.p', video_source=0):
    # Load the model
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']

    # Initialize video capture
    cap = cv2.VideoCapture(video_source)

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
    predicted_character = None

    # Variables for tracking stability
    start_time = 0
    stable_character = None
    output = None

    # Labels dictionary
    labels_dict = {0: 'B', 1: 'C', 2: 'L', 3: 'S', 4: 'Y', 5: '1'}

    while True:
        # Initialize variables
        data_aux = []
        x_ = []
        y_ = []

        # Read frame from video source
        ret, frame = cap.read()
        if not ret:
            break

        # Get frame dimensions
        H, W, _ = frame.shape

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            right_hands_count = 0
            for hand_landmarks in results.multi_hand_landmarks:
                # Check if it's the right hand
                is_right_hand = False
                for i, landmark in enumerate(hand_landmarks.landmark):
                    if i == 5:  # Index finger tip
                        if landmark.x * W > hand_landmarks.landmark[17].x * W:
                            is_right_hand = True
                            break
                if is_right_hand:
                    right_hands_count += 1
                    # print(right_hands_count)
                    if right_hands_count != 1:
                       continue 
                    else:
                    # Draw hand landmarks and connections
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                        # Collect hand landmark data
                        for landmark in hand_landmarks.landmark:
                            x = landmark.x
                            y = landmark.y
                            x_.append(x)
                            y_.append(y)
                        for landmark in hand_landmarks.landmark:
                            x = landmark.x
                            y = landmark.y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                        # Compute bounding box coordinates
                        x1 = int(min(x_) * W) - 10
                        y1 = int(min(y_) * H) - 10
                        x2 = int(max(x_) * W) - 10
                        y2 = int(max(y_) * H) - 10

                        # Make prediction using the model
                        prediction = model.predict([np.asarray(data_aux)])
                        predicted_character = labels_dict[int(prediction[0])]

                        # Draw bounding box and predicted character
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                    cv2.LINE_AA)
                        # print(predicted_character)
                        if predicted_character == stable_character:
                            if start_time is None:
                                start_time = time.time()
                            elif time.time() - start_time >= 2:
                                yield predicted_character
                        else:
                            start_time = None
                            stable_character = predicted_character

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start hand gesture detection
for output in mode():
    print(output)