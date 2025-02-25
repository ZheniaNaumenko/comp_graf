from array import array

import numpy as np
from PIL import Image, ImageOps


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
v = number_verc(poly)
print(v)
