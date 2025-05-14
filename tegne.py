
import tensorflow as tf
import numpy as np

import pygame as pg
import math

pg.init()

SCREENSIZE = 400
gridSize = 28

model = tf.keras.models.load_model('model.keras')
pg.display.set_caption('Quick Start')
display = pg.display.set_mode((SCREENSIZE, SCREENSIZE))

# out of bounds
def oob(x):
    return x < 0 or x >= gridSize

pixelSize = SCREENSIZE / gridSize
blurSize = 4
R
while True:
    grid = [[0 for i in range(gridSize)] for j in range(gridSize)]
    lastPos = (0, 0)
    is_running = True
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False

        if pg.mouse.get_pressed()[0]:
            mx, my = pg.mouse.get_pos()
            if mx > 0 and my > 0 and mx < SCREENSIZE and my < SCREENSIZE:
                gx = math.floor(gridSize*mx/SCREENSIZE)
                gy = math.floor(gridSize*my/SCREENSIZE)

                if (gx, gy) != (lastPos):
                    grid[gy][gx] = max(grid[gy][gx], 0.8)
                    for y in range(-blurSize, blurSize):
                        for x in range(-blurSize, blurSize):
                            if oob(gx+x) or oob(gy+y) or (x == 0 and y == 0):
                                continue

                            dist = (mx-(gx+x+0.5)*pixelSize)**2 + (my-(gy+y+0.5)*pixelSize)**2
                            # grid[gy+y][gx+x] += 30 / (dist**0.8) - 0.1
                            grid[gy+y][gx+x] += 10 / ((dist*0.4)**1.1)
                            grid[gy+y][gx+x] = max(0, min(1, grid[gy+y][gx+x]))
                lastPos = (gx, gy)
        
        for y in range(gridSize):
            for x in range(gridSize):
                v = 255 * (1-grid[y][x])
                c = (v, v, v)
                p = (x*pixelSize, y*pixelSize, (x+1)*pixelSize, (y+1)*pixelSize)
                pg.draw.rect(display, c, p)

        pg.display.update()

    test = np.array(grid).reshape((1, 28, 28))
    predictions = model.predict(test)
    print(np.argmax(predictions))
