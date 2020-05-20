import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox 
import matplotlib.image as mpimg

# generate some data
x = np.arange(0, 10, 0.2)
y = np.sin(x)

# plot it
f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
a0.set_xlim(0, 100)
a0.set_ylim(0, 100)
a0.plot(x, y)
img = plt.imread("grass.png")
a0.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    labelleft=False,
    labelbottom=False)
a0.imshow(img)
arr_lena = mpimg.imread('bunny.png')
imagebox = OffsetImage(arr_lena, zoom=0.2)
ab = AnnotationBbox(imagebox, (50, 50))
a0.add_artist(ab)
a1.plot(y, x)

plt.show()