import cv2
import mss
import pyautogui
import numpy as np

pyautogui.PAUSE = 0

monitor = {"top": 530, "left": 330, "width": 37, "height": 15}

with mss.mss() as sct:
    while True:

        img = np.array(sct.grab(monitor))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if np.mean(gray) < 127:
            gray = cv2.bitwise_not(gray)

        if np.mean(gray) < 245:
            pyautogui.press('space')
            print("Прыжок!")

        monitor['width'] += 0.005
        cv2.imshow("Debug", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break