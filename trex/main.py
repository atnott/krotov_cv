import cv2
import mss
import pyautogui
import numpy as np
import time

pyautogui.PAUSE = 0

JUMP_DURATION = 0.20
DUCK_DURATION = 0.20

MIN_JUMP = 0.05
MIN_DUCK = 0.06

start_time = time.time()
last_speed_up_time = start_time

cnt = 0

monitor = {"top": 285, "left": 508, "width": 30, "height": 35}

with mss.mss() as sct:
     while True:
        current_time = time.time()

        if current_time - last_speed_up_time >= 30.0:
            if JUMP_DURATION > MIN_JUMP:
                JUMP_DURATION = max(MIN_JUMP, JUMP_DURATION - 0.015)
            if DUCK_DURATION > MIN_DUCK:
                DUCK_DURATION = max(MIN_DUCK, DUCK_DURATION - 0.015)

            last_speed_up_time = current_time
            cnt += 1

        if cnt % 2 == 0 and cnt > 0:
            monitor['width'] += 5

        img = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if np.mean(gray) < 127:
            gray = cv2.bitwise_not(gray)

        height, width = gray.shape
        bottom_half = gray[height // 2:, :]
        top_half = gray[:height // 2, :]

        if np.mean(bottom_half) < 247:
            pyautogui.press('space')
            time.sleep(JUMP_DURATION)
            pyautogui.keyDown('down')
            time.sleep(0.05)
            pyautogui.keyUp('down')

        elif np.mean(top_half) < 247:
            pyautogui.keyDown('down')
            time.sleep(DUCK_DURATION)
            pyautogui.keyUp('down')

        cv2.imshow("game", gray)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
