import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from math import dist

files = sorted([file for file in os.listdir('out/')], key = lambda f: int(f.split('_')[1].split('.')[0]))

def centroid(labeled, label_id: int = 1) -> tuple:
    ys, xs = np.where(labeled == label_id)
    return np.mean(xs), np.mean(ys)

def get_points(file_name: str) -> list[tuple]:
    image = np.load(f'out/{file_name}')
    labeled = label(image)
    return [centroid(labeled, idx) for idx in range(1, labeled.max() + 1)]

array = list()
last_points = list()

for file in files:
    now_points = get_points(file)

    if not array:
        array = [list() for _ in range(len(now_points))]
        last_points = now_points

    else:
        new_points = list()
        for point in last_points:
            temp = min(now_points, key = lambda p: dist(p, point))
            new_points.append(temp)
            now_points.remove(temp)
        last_points = new_points

    for i in range(len(last_points)):
        array[i].append(last_points[i])

for temp in [el for el in array if len(el) > 0]:
    x, y = [x for x, y in temp], [y for x, y in temp]
    plt.plot(x, y)

plt.show()