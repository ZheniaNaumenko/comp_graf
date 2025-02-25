from PIL import Image
import numpy as np
import math

height, width = 1000, 1000
# a = int(input("Размер "))
# height, width = a, a

image_matrix = np.full((height, width, 3), 200, dtype=np.uint8)
image = Image.fromarray(image_matrix, 'RGB')
pixels = image.load()
color = (0, 0, 0)


def dotted_line(image, x0, y0, x1, y1, count, color):
    step = 1 / count
    for t in np.arange(0, 1, step):
        x = round((1.0 - t) * x0 + t * x1)
        y = round((1.0 - t) * y0 + t * y1)
        pixels[y, x] = color


def dotted_line_v2(image, x0, y0, x1, y1, color):
    count = int(math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))
    for i in range(count + 1):
        t = i / count
        x = int((1.0 - t) * x0 + t * x1)
        y = int((1.0 - t) * y0 + t * y1)
        pixels[x, y] = color


def x_loop_line(image, x0, y0, x1, y1, color):
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t * y1)
        pixels[x, y] = color


def x_loop_line_hotfix_1(image, x0, y0, x1, y1, color):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t * y1)
        pixels[x, y] = color


def x_loop_line_hotfix_2(image, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True

    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t * y1)
        if xchange:
            pixels[x, y] = color
        else:
            pixels[y, x] = color


def x_loop_line_v2(image, x0, y0, x1, y1, color):
    xchange = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t * y1)
        if xchange:
            pixels[x, y] = color
        else:
            pixels[y, x] = color


def x_loop_line_v2_no_y_calc(image, x0, y0, x1, y1, color):
    xchange = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    dy = abs(y1 - y0) / (x1 - x0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1

    for x in range(x0, x1):
        if xchange:
            pixels[x, y] = color
        else:
            pixels[y, x] = color

        derror += dy
        if derror > 0.5:
            derror -= 1.0
            y += y_update


def x_loop_line_v2_no_y_calc_v2_for_some_unknown_reason(image, x0, y0, x1, y1, color):
    xchange = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    dy = 2 * (x1 - x0) * abs(y1 - y0) / (x1 - x0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1

    for x in range(x0, x1):
        if xchange:
            pixels[x, y] = color
        else:
            pixels[y, x] = color

        derror += dy
        if derror > 2 * (x1 - x0) * 0.5:
            derror -= 2 * (x1 - x0) * 1.0
            y += y_update


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


def save_show(image):
    image.save('zvezda.png')
    image.show()


for i in range(0, 13):
    x0 = int(width / 2)
    y0 = int(height / 2)
    alfa = 2 * math.pi * i / 13
    ax, bx = x0, x0 * 9 / 10
    ay, by = y0, y0 * 9 / 10
    x1 = int(ax + bx * math.cos(alfa))
    y1 = int(ay + by * math.sin(alfa))

    # dotted_line(image, x0, y0, x1, y1, 190, color)
    # dotted_line_v2(image, x0, y0, x1, y1, color)
    # x_loop_line(image, x0, y0, x1, y1, color)
    # x_loop_line_hotfix_1(image, x0, y0, x1, y1, color)
    # x_loop_line_hotfix_2(image, x0, y0, x1, y1, color)
    # x_loop_line_v2(image, x0, y0, x1, y1, color)
    # x_loop_line_v2_no_y_calc(image, x0, y0, x1, y1, color)
    # x_loop_line_v2_no_y_calc_v2_for_some_unknown_reason(image, x0, y0, x1, y1, color)
    bresenham_line(image, x0, y0, x1, y1, color)

save_show(image)
