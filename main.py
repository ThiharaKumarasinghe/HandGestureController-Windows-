from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui
import time
import keyboardInput
import numpy as np


# Output video dimensions (increased)
output_width = 1024
output_height = 768

# Calculate the dimensions of the squares
square_width = int(output_width / 3)
square_height = output_height

# Initialize video capture
cap = cv2.VideoCapture(0)

# Hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (output_width, output_height))
    height, width, channel = frame.shape

    # Create an overlay
    overlay = np.zeros_like(frame, dtype=np.uint8)

    # Draw squares on the overlay
    cv2.rectangle(overlay, (0, 0), (square_width, square_height), (255, 255, 255), -1)  # Left square
    cv2.rectangle(overlay, (2 * square_width, 0), (output_width, square_height), (255, 255, 255), -1)  # Right square

    # Combine the frame and overlay with opacity
    opacity = 0.2
    cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

    # Flip the frame horizontally to fix mirroring
    frame = cv2.flip(frame, 1)

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # hands
    hands, frame = detector.findHands(frame)

    data =[]
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        # print(lmList)
        for lm in lmList:
            data.extend([lm[0], 720 - lm[1], lm[2]])

        print(f'width : {width}')
        print(f'height : {height}')

        # Check if hand is open or closed
        if data[12*3+1] > data[4*3+1]:  # Hand open
            cv2.putText(frame, "Forward", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            keyboardInput.press_key('w')
            keyboardInput.release_key('s')
            if data[9 * 3] < square_width:  # Hand left
                cv2.putText(frame, "Left", (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                keyboardInput.press_key('a')
            else:
                keyboardInput.release_key('a')

            if data[9 * 3] > square_width*2:  # Hand right
                cv2.putText(frame, "Right", (800, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                keyboardInput.press_key('d')
            else:
                keyboardInput.release_key('d')
        else:  # Hand closed
            cv2.putText(frame, "Backward", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            keyboardInput.press_key('s')
            keyboardInput.release_key('w')
            if data[9 * 3] < square_width:  # Hand left
                cv2.putText(frame, "Left", (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                keyboardInput.press_key('a')
            else:
                keyboardInput.release_key('a')

            if data[9 * 3] > square_width * 2:  # Hand right
                cv2.putText(frame, "Right", (800, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                keyboardInput.press_key('d')
            else:
                keyboardInput.release_key('d')


    else:
        print('Show your hand to camera')
        cv2.putText(frame, "No hand detected!", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        keyboardInput.release_key('w')
        keyboardInput.release_key('s')
        keyboardInput.release_key('a')
        keyboardInput.release_key('d')

    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
