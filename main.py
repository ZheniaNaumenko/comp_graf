from PIL import Image
import numpy as np

height = int(input("Длина "))
width = int(input("Ширина "))

image_matrix = np.zeros((height, width), dtype=np.uint8)
image1 = Image.fromarray(image_matrix, 'L')
image1.save('black.png')
image1.show()

image_matrix = np.full((height, width), 255, dtype=np.uint8)
image2 = Image.fromarray(image_matrix, 'L')
image2.save('white.png')
image2.show()

image_matrix = np.ones((height, width, 3), dtype=np.uint8)
image_matrix[:] = [255, 0, 0]
image3 = Image.fromarray(image_matrix, 'RGB')
image3.save('red.png')
image3.show()

image_matrix = np.ones((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(width):
        s = (i + j) % 256
        a = i % 256
        b = j % 256
        image_matrix[i, j] = [a, b, s]

image4 = Image.fromarray(image_matrix, 'RGB')
image4.save('grad.png')
image4.show()
