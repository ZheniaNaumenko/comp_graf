import numpy as np
from PIL import Image, ImageOps


def bresenham_line(image, x0, y0, x1, y1, color):
    xchange = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    dy = 2 * abs(y1 - y0)
    derror = 0
    y_update = 1 if y1 > y0 else -1

    for x in range(x0, x1):
        if xchange:
            pixels[x, y] = color
        else:
            pixels[y, x] = color

        derror += dy
        if derror > (x1 - x0):
            derror -= 2 * (x1 - x0)
            y += y_update


def open_v(obj):
    vertices = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(x) for x in line.split(' ')[1:]]
                vertices.append(vertex)
    return vertices


def open_poly(obj):
    poly = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('f '):
                polygon = line.split(' ')[1:]
                p = [[int(x) for x in i.split('/')] for i in polygon]
                poly.append(p)
    return poly


def number_verc(poly):
    v = []
    for i in range(0, len(poly)):
        n = [poly[i][0][0], poly[i][1][0], poly[i][2][0]]
        v.append(n)
    return v


poly = open_poly("model_1.obj")
num = number_verc(poly)
v = open_v("model_1.obj")
obj_image_matrix = np.full((1000, 1000, 3), 200, dtype=np.uint8)
image = Image.fromarray(obj_image_matrix, 'RGB')
pixels = image.load()
color = (0, 0, 0)

for i in range(0, len(poly)):
    x0 = int(v[num[i][0] - 1][0] * 5000 + 400)
    x1 = int(v[num[i][1] - 1][0] * 5000 + 400)
    x2 = int(v[num[i][2] - 1][0] * 5000 + 400)

    y0 = int(v[num[i][0] - 1][1] * 5000 + 400)
    y1 = int(v[num[i][1] - 1][1] * 5000 + 400)
    y2 = int(v[num[i][2] - 1][1] * 5000 + 400)

    bresenham_line(image, x0, y0, x1, y1, color)
    bresenham_line(image, x1, y1, x2, y2, color)
    bresenham_line(image, x2, y2, x0, y0, color)

image = image.rotate(90)
image.show()
