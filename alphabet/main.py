import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def count_lines(region):
    shape = region.image.shape
    image = region.image
    v_lines = (np.sum(image, 0) / shape[0] == 1).sum()
    h_lines = (np.sum(image, 1) / shape[1] == 1).sum()
    return v_lines, h_lines

def symmetry(region, traspose = False):
    image = region.image
    if traspose:
        image = image.T
    shape = image.shape
    top = image[:shape[0] // 2]
    if shape[0] % 2 != 0:
        bottom = image[shape[0] // 2 + 1:]
    else:
        bottom = image[shape[0] // 2:]
    bottom = bottom[::-1]
    result = bottom == top
    return result.sum() / result.size

def classificator(region):
    holes = count_holes(region)
    if holes == 2: # B 8
        v, _ = count_lines(region)
        v /= region.image.shape[1]
        sym = symmetry(region, traspose = True)
        if v > 0.1 and sym < 0.9:
            return 'B'
        return '8'
    elif holes == 1: # A O P D
        eccentricity = region.eccentricity
        sym = symmetry(region)
        sym2 = symmetry(region, traspose = True)
        if sym > 0.989 and (eccentricity > 0.7 or eccentricity < 0.6): return 'D'
        if sym < 0.6 and sym2 > 0.7: return 'A'
        sym2 = symmetry(region, True)
        if sym2 > 0.8 and sym > 0.8: return 'O'
        return 'P'
    elif holes == 0:
        eccentricity = region.eccentricity
        if eccentricity < 0.5: return '*'
        v, _ = count_lines(region)
        sym = symmetry(region)
        sym2 = symmetry(region, True)
        if v < 0.1 and sym > 0.7:
            return 'X'
        elif v < 0.1 and sym < 0.7 and sym2 < 0.7:
            return '/'
        elif v > 1 and sym < 1:
            return '1'
        elif v > 1 and sym > 0.95:
            return '-'
        elif sym2 >= 0.7:
            return 'W'
    return '?'

image = imread('symbols.png')
binary = image.mean(2) > 0
labeled = label(binary)

props = regionprops(labeled)
result = dict()
image_path = save_path / 'out'
image_path.mkdir(exist_ok=True)

plt.figure(figsize=(5, 7))
for region in props:
    symbol = classificator(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f'class - "{symbol}"')
    plt.imshow(region.image)
    plt.savefig(image_path / f'image_{region.label}.png')

print(result)