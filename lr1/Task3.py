import numpy as np
from PIL import Image, ImageOps


def open_v(obj):
    vertices = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(x) for x in line.split(' ')[1:]]
                vertices.append(vertex)
    return vertices


object = open_v("model_1.obj")
print(object)
