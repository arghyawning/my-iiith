import numpy as np
import matplotlib.pyplot as plt

t = 0
dice_samples = np.zeros(5000)

if u < 1/6:
    dice_sample = 1
if 1/6 < u < 2/6:
    dice_sample = 2
if 2/6 < u < 3/6:
    dice_sample = 3
if 3/6 < u < 4/6:
    dice_sample = 4
if 4/6 < u < 5/6:
    dice_sample = 5
if 5/6 < u < 6/6:
    dice_sample = 6
dice_samples[t] = dice_sample

plt.hist(dice_samples, bins=10, density=True)
plt.show()
