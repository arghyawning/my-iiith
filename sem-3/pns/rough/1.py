import numpy as np
import matplotlib.pyplot as plt
uni_samples = np.random.uniform(0, 1, 5000)#vector of 5000 realisations of uniform random variable U
plt.hist(uni_samples, bins=10, density=True)
plt.show()
