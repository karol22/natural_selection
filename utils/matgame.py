import matplotlib
matplotlib.use("Agg")
import pygame
from pygame.locals import *
import matplotlib.backends.backend_agg as agg
import time


import pylab

fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
ax.plot([1, 2, 4])

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()

pygame.init()
window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()
size = canvas.get_width_height()

surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (0,0))
pygame.display.flip()

crashed = False
x = 1
y = 2
z = 3
while not crashed:
	time.sleep(1)
	x = x + 1
	y = y + 1
	z = z + 1
	print("here")
	ax.plot([x, y, z])
	canvas.draw()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True