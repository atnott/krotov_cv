import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from skimage.color import rgb2hsv

def get_near_shade(shade, shades, delta = 0.05):
    for temp in shades:
        if abs(temp - shade) < delta:
            return temp
    return shade

image = imread('balls_and_rects.png')
hsv = rgb2hsv(image)
h = hsv[:, :, 0]

circles = {}
rects = {}

binary = np.sum(image, axis = 2) > 0
labeled = label(binary)
for region in regionprops(labeled):
    mask = labeled == region.label
    avg_color = np.mean(h[mask])

    if region.extent > 0.95:
        color = get_near_shade(avg_color, rects.keys())
        if color not in rects.keys():
            rects[color] = 0
        rects[color] += 1
    else:
        color = get_near_shade(avg_color, circles.keys())
        if color not in circles.keys():
            circles[color] = 0
        circles[color] += 1

print('Всего фируг')
print(sum(circles.values()) + sum(rects.values()))

print('\nПрямоугольники')
for color, count in rects.items():
    print(f'Оттенок {round(color, 3)}: {count}')

print("\nКруги")
for color, count in circles.items():
    print(f'Оттенок {round(color, 3)}: {count}')

plt.imshow(h)
plt.show()