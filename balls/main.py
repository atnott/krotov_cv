import cv2
import numpy as np
import json
import random
from pathlib import Path

SAVE_PATH = Path(__file__).parent
CONFIG_PATH = SAVE_PATH / 'config_balls.json'

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

clicked_pos = None
is_clicked = False
calibrated_colors = []
names_array = [str(i) for i in range(4)]

def on_click(event, x, y, flags, param):
    global clicked_pos, is_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_pos = (x, y)
        is_clicked = True

cv2.setMouseCallback("Image", on_click)

if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, 'r') as file:
            data = json.load(file)
            for temp in data:
                calibrated_colors.append({
                    'name': temp['name'],
                    'lower': np.array(temp['lower'], dtype='u1'),
                    'upper': np.array(temp['upper'], dtype='u1')
                })
    except Exception as e:
        print(e)

capture = cv2.VideoCapture(0)

game_array = []
game_start = False
won = False

while True:
    _, frame = capture.read()
    frame = cv2.flip(frame, 1)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        break

    if key == ord('s'):
        if len(calibrated_colors) >= 3:
            serializable_data = []
            for ball in calibrated_colors:
                serializable_data.append({
                    "name": ball["name"],
                    "lower": ball["lower"].tolist(),
                    "upper": ball["upper"].tolist()
                })
            with open(CONFIG_PATH, 'w') as file:
                json.dump(serializable_data, file)

            all_names = [x['name'] for x in calibrated_colors]
            game_array = all_names.copy()
            random.shuffle(game_array)

            game_start = True
            won = False

    if is_clicked:
        is_clicked = False
        if len(calibrated_colors) < 4:
            name = names_array[len(calibrated_colors)]
            color = hsv[clicked_pos[1], clicked_pos[0]]
            lower = np.clip(color * 0.9, 0, 255).astype("u1")
            upper = np.clip(color * 1.1, 0, 255).astype("u1")
            upper[1] = 255
            upper[2] = 255
            calibrated_colors.append({
                "name": name,
                "lower": lower,
                "upper": upper
            })

    detected_balls = []
    for ball in calibrated_colors:
        mask = cv2.inRange(hsv, ball["lower"], ball["upper"])
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), dtype='u1'))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                detected_balls.append((int(x), int(y), ball["name"]))
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 4)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

    current_user_sequence = []
    if len(detected_balls) == len(calibrated_colors) and len(calibrated_colors) >= 3:
        if len(calibrated_colors) == 3:
            detected_balls.sort(key=lambda b: b[0])
            current_user_sequence = [b[2] for b in detected_balls]

        elif len(calibrated_colors) == 4:
            detected_balls.sort(key=lambda b: b[1])
            top_row = detected_balls[:2]
            bottom_row = detected_balls[2:]

            top_row.sort(key=lambda b: b[0])
            bottom_row.sort(key=lambda b: b[0])

            current_user_sequence = [top_row[0][2], top_row[1][2], bottom_row[0][2], bottom_row[1][2]]

    if game_start:
        cv2.putText(frame, f"TASK: {' -> '.join(map(str, game_array))}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        if current_user_sequence:
            cv2.putText(frame, f"YOU:  {' -> '.join(current_user_sequence)}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
            if current_user_sequence == game_array:
                won = True
        else:
            cv2.putText(frame, "Show all balls to camera!", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if won:
        cv2.putText(frame, "YOU WIN!", (frame.shape[1] // 3, frame.shape[0] // 2),
                    cv2.FONT_HERSHEY_TRIPLEX, 2.0, (0, 255, 0), 5)

    status_str = f"Calibrated colors: {len(calibrated_colors)}/4. Game Started: {game_start}"
    cv2.putText(frame, status_str, (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 0), 5)

    cv2.imshow("Image", frame)

capture.release()
cv2.destroyAllWindows()
