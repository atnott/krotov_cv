import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import opening

image = np.load('data/wires5.npy')

processed = opening(image, footprint=np.ones((3, 1)))
labeled = label(image)
for n in range(1, labeled.max() + 1):
    wire = labeled == n
    wire = opening(wire, footprint=np.ones((3, 1)))
    print(f'wire = {n}, parts = {label(wire).max()}')

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(processed)
plt.show()