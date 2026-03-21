import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

def area(labeled, label = 1) -> int:
    return (labeled == label).sum()

image = np.load('stars.npy')
labeled = label(image)
array = [area(labeled, i) for i in range(1, labeled.max() + 1)]
answer = [(k, array.count(k)) for k in set(array)]
print(*answer, sep = '\n')

plt.imshow(image)
plt.show()