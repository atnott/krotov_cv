import numpy as np
from skimage.measure import label
from matplotlib import pyplot as plt

def count_corners(image):
    external = 0
    internal = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            block = image[y: y + 2, x: x + 2]
            sum_pixels = block.sum()
            if sum_pixels == 1:
                external += 1
            elif sum_pixels == 3:
                internal += 1
    return external, internal

def cropping(image):
    cords = np.argwhere(image > 0)
    y_min, x_min = cords.min(axis=0)
    y_max, x_max = cords.max(axis=0)
    return image[max(y_min - 1, 0): y_max + 2, max(x_min - 1, 0): x_max + 2]

d = dict()

labeled = label(np.load('stars.npy'))
for i in range(1, labeled.max() + 1):
    image = labeled == i
    cropped = cropping(image)
    answer = count_corners(cropped)

    '''вывод крестика, лежащего на границе'''
    # if answer == (16, 0):
    #     plt.imshow(cropped)
    #     plt.show()

    if answer not in d:
        d[answer] = 0
    d[answer] += 1

# один крестик лежит на координате Х = 0
print(d, f'''
плюсиков: {d[(8, 4)]}
крестиков: {d[(20, 0)] + d[16, 0]} 
прямоугольников: {d[(4, 0)]}
ответ: {sum(d.values()) - d[(4, 0)]}''')