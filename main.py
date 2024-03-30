from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui
import time
import keyboardInput

# Initialize video capture
cap = cv2.VideoCapture(0)

# Hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

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


        print(f'X position : {data[9 * 3]}')

        # Check if hand is open or closed
        if data[12*3+1] > data[4*3+1]:  # Hand open
            keyboardInput.press_key('w')
            keyboardInput.release_key('s')
            # pyautogui.keyUp("down")
            # pyautogui.keyDown("up")
            # # press_and_hold_key_continuously('s', 0.1)
            if data[9 * 3] < 240:  # Hand left
                keyboardInput.press_key('a')
            else:
                keyboardInput.release_key('a')

            if data[9 * 3] > 480:  # Hand right
                keyboardInput.press_key('d')
            else:
                keyboardInput.release_key('d')
        else:  # Hand closed
            keyboardInput.press_key('s')
            keyboardInput.release_key('w')
            if data[9 * 3] < 240:  # Hand left
                keyboardInput.press_key('a')
            else:
                keyboardInput.release_key('a')

            if data[9 * 3] > 480:  # Hand right
                keyboardInput.press_key('d')
            else:
                keyboardInput.release_key('d')
            # pyautogui.keyUp("up")
            # pyautogui.keyDown("down")
            # # press_and_hold_key_continuously('w', 0.1)
            # if data[9*3] < 440:  # Hand left
            #     press_and_hold_key_continuously('left', 0.1)
            #
            # if data[9*3] > 800:  # Hand right
            #     press_and_hold_key_continuously('right', 0.1)




#


    else:
        print('Show your hand to camera')
        keyboardInput.release_key('w')
        keyboardInput.release_key('s')
        keyboardInput.release_key('a')
        keyboardInput.release_key('d')








    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # cv2.imshow('rgb Hand Detection', rgb_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
