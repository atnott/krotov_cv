import cv2
import mss
import pyautogui
import numpy as np

pyautogui.PAUSE = 0

monitor = {"top": 285, "left": 520, "width": 30, "height": 35}

with mss.mss() as sct:
     while True:

        img = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if np.mean(gray) < 127:
            gray = cv2.bitwise_not(gray)

        height, width = gray.shape
        bottom_half = gray[height // 2:, :]
        top_half = gray[:height // 2, :]

        if np.mean(bottom_half) < 247:
            pyautogui.press('space')
            # pyautogui.press('down')

        elif np.mean(top_half) < 247:
            pyautogui.keyDown('down')

        cv2.imshow("Debug", gray)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
