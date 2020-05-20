import matplotlib.pyplot as plt
import numpy as np
import time

x= np.array([1, 2, 3, 4, 5])
y = np.array([1, 4, 9, 16, 25])
fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
axs[0].scatter(x, y)
axs[1].scatter(x, -y)
i = 2
while True:
    plt.draw()
    plt.pause(0.2)
    x = x + [i]
    y = y + [i]
    axs[0].scatter(x, y)
    axs[1].scatter(x, -y)
    print("here")
    time.sleep(1)
