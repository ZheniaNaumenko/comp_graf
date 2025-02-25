import numpy as np
from PIL import Image, ImageOps
import time


def open_v(obj):
    vertices = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(x) for x in line.split(' ')[1:]]
                vertices.append(vertex)
    return vertices


object = open_v("model_1.obj")
obj_image_matrix = np.full((1000, 1000, 3), 200, dtype=np.uint8)
image = Image.fromarray(obj_image_matrix, 'RGB')
pixels = image.load()
color = (0, 0, 0)

for i in range(0, len(object) - 1):
    x = int(object[i][0] * 5000 - 450)
    y = int(object[i][1] * 5000 + 250)
    pixels[y, x] = color

image = image.rotate(90)
image.show()
