import numpy as np
from PIL import Image, ImageOps
import random


def barcoords(x, y, x0, y0, x1, y1, x2, y2):
    x, y = int(x), int(y)
    lam0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lam1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lam2 = 1.0 - lam0 - lam1
    return lam0, lam1, lam2


def draw_triangle(pixels, x0, y0, x1, y1, x2, y2, color):
    xmin = int(min(x0, x1, x2))
    xmin = 0 if xmin < 0 else int(min(x0, x1, x2))
    xmax = int(max(x0, x1, x2) + 1.0) if int(max(x0, x1, x2) + 1.0) <= 1000 else 0
    ymin = int(min(y0, y1, y2)) if int(min(y0, y1, y2)) >= 0 else 0
    ymax = int(max(y0, y1, y2) + 1.0) if int(max(y0, y1, y2) + 1.0) <= 1000 else 0
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            lam0, lam1, lam2 = barcoords(x, y, x0, y0, x1, y1, x2, y2)
            if 0 <= lam0 and 0 <= lam1 and 0 <= lam2:
                pixels[y, x] = color

def norma(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    A = np.array([x1 - x2, y1 - y2, z1 - z2])
    B = np.array([x1 - x0, y1 - y0, z1 - z0])
    norma = np.cross(A, B)
    return norma


def pr(n, l):
    proz = np.dot(n, l) / (np.linalg.norm(n) * np.linalg.norm(l))
    return proz

def open_v(obj):
    vertices_v = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = np.array(list(map(float, line.split()[1:])))
                vertices_v.append(vertex)
    return np.array(vertices_v)

def open_poly(obj):
    p = []
    with open(obj, 'r') as file:
        for line in file:
            if line.startswith('f '):
                n = [x.split(' ') for x in line.split()[1:]]
                p.append(n)
    return np.array(p)

def number_verc(poly):
    x, n = [], []
    for i in range(len(poly)):
        xyz1 = [x.split('/') for x in poly[i][0]]
        x1 = xyz1[0][0]
        xyz2 = [x.split('/') for x in poly[i][1]]
        x2 = xyz2[0][0]
        xyz3 = [x.split('/') for x in poly[i][2]]
        x3 = xyz3[0][0]
        x.append([x1, x2, x3])
    return x

poly = open_poly("model_1.obj")
x = number_verc(poly)
v = open_v("model_1.obj")
obj_image_matrix = np.full((1000, 1000, 3), 255, dtype=np.uint8)
image = Image.fromarray(obj_image_matrix, 'RGB')
pixels = image.load()
l = np.array([0, 0, 1])


for i in range(0, len(poly)):

    x0 = v[int(x[i][0]) - 1][0] * 5000 + 400
    x1 = v[int(x[i][1]) - 1][0] * 5000 + 400
    x2 = v[int(x[i][2]) - 1][0] * 5000 + 400

    y0 = v[int(x[i][0]) - 1][1] * 5000 + 400
    y1 = v[int(x[i][1]) - 1][1] * 5000 + 400
    y2 = v[int(x[i][2]) - 1][1] * 5000 + 400

    z0 = v[int(x[i][0]) - 1][2] * 5000 + 400
    z1 = v[int(x[i][1]) - 1][2] * 5000 + 400
    z2 = v[int(x[i][2]) - 1][2] * 5000 + 400

    rand = random.randint(0, 255)
    n = norma(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    fl = pr(n, l)
    col1 = 0
    col2 = int(-200 * fl)
    col3 = col2
    color = (col1, col2, col3)
    if fl < 0:
        draw_triangle(pixels, x0, y0, x1, y1, x2, y2, color)

image = image.rotate(90)
image.show()