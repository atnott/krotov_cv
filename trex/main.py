import cv2
import mss
import pyautogui
import numpy as np
import time

pyautogui.PAUSE = 0

JUMP_DURATION = 0.135
DUCK_DURATION = 0.20

START_LEFT = 508
START_WIDTH = 25

current_left = START_LEFT
current_width = START_WIDTH

MAX_LEFT = 590
MAX_WIDTH = 55

monitor = {"top": 285, "left": current_left, "width": current_width, "height": 35}

start_time = time.time()
last_speed_up_time = start_time

cnt_time = 0

with mss.mss() as sct:
    while True:
        current_time = time.time()

        temp = current_time - last_speed_up_time
        if temp >= 20:
            if current_left < MAX_LEFT:
                current_left += 1

            if current_width < MAX_WIDTH:
                if cnt_time < 160:
                    current_width += 2
                else:
                    current_width += 5
            cnt_time += 20

            monitor['left'] = current_left
            monitor['width'] = current_width

            last_speed_up_time = current_time

        img = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape
        bottom_half = gray[height // 2:, :]
        top_half = gray[:height // 2, :]

        if np.mean(bottom_half) < 247:
            pyautogui.press('space')
            time.sleep(JUMP_DURATION)
            pyautogui.keyDown('down')
            if cnt_time > 160:
                time.sleep(0.03)
            pyautogui.keyUp('down')

        elif np.mean(top_half) < 247:
            pyautogui.keyDown('down')
            time.sleep(DUCK_DURATION)
            pyautogui.keyUp('down')

        # cv2.imshow('game', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()