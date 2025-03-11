from operator import matmul

import numpy as np
from PIL import Image, ImageOps
import math
import random


def barcoords(x, y, x0, y0, x1, y1, x2, y2):
    x, y = int(x), int(y)
    lam0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lam1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lam2 = 1.0 - lam0 - lam1
    return lam0, lam1, lam2


def draw_triangle(pixels, x0, y0, x1, y1, x2, y2, z0, z1, z2, zbuffer, color):
    xmin = int(min(x0, x1, x2))
    xmin = 0 if xmin < 0 else int(min(x0, x1, x2))
    xmax = int(max(x0, x1, x2) + 1.0) if int(max(x0, x1, x2) + 1.0) <= 1000 else 0
    ymin = int(min(y0, y1, y2)) if int(min(y0, y1, y2)) >= 0 else 0
    ymax = int(max(y0, y1, y2) + 1.0) if int(max(y0, y1, y2) + 1.0) <= 1000 else 0
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            lam0, lam1, lam2 = barcoords(x, y, x0, y0, x1, y1, x2, y2)
            if 0 <= lam0 and 0 <= lam1 and 0 <= lam2:
                z_ish = z0 * lam0 + z1 * lam1 + z2 * lam2
                if z_ish < zbuffer[x, y]:
                    pixels[y, x] = color
                    zbuffer[x, y] = z_ish




def norma(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    A = np.array([x1 - x2, y1 - y2, z1 - z2])
    B = np.array([x1 - x0, y1 - y0, z1 - z0])
    norma = np.cross(A, B)
    return norma

def pr(n, l):
    proz = np.dot(n, l) / (np.linalg.norm(n) * np.linalg.norm(l))
    return proz

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

def r_calc(a, b, c):
    alpha = np.radians(a)
    beta = np.radians(b)
    gamma = np.radians(c)

    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), np.sin(alpha)],
        [0, -np.sin(alpha), np.cos(alpha)]
    ])

    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

    R_z = np.array([
        [np.cos(gamma), np.sin(gamma), 0],
        [-np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])

    r = R_z @ R_y @ R_x
    return r

poly = open_poly("model_1.obj")
num = number_verc(poly)
v = open_v("model_1.obj")
obj_image_matrix = np.full((1000, 1000, 3), 255, dtype=np.uint8)
image = Image.fromarray(obj_image_matrix, 'RGB')
pixels = image.load()
l = np.array([0, 0, 1])
zbuffer = np.full((1000, 1000), np.inf)
r = r_calc(0, 180, 0)
t = np.array([0.0, -0.04, 0.0])


for i in range(0, len(v)):
    v[i] = r @ v[i] + t

for i in range(0, len(poly)):

    x0 = v[num[i][0] - 1][0] *5000 + 500
    x1 = v[num[i][1] - 1][0]*5000 + 500
    x2 = v[num[i][2] - 1][0]*5000 + 500

    y0 = v[num[i][0] - 1][1]*5000 + 500
    y1 = v[num[i][1] - 1][1]*5000 + 500
    y2 = v[num[i][2] - 1][1]*5000 + 500

    z0 = v[num[i][0] - 1][2]*5000 + 500
    z1 = v[num[i][1] - 1][2]*5000 + 500
    z2 = v[num[i][2] - 1][2]*5000 + 500

    rand = random.randint(0, 255)
    n = norma(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    fl = pr(n, l)
    col1 = 0
    col2 = int(-150 * fl)
    col3 = col2
    color = (col1, col2, col3)
    if fl < 0:
        draw_triangle(pixels, x0, y0, x1, y1, x2, y2, z0, z1, z2, zbuffer, color)


image = image.rotate(90)
image.show()