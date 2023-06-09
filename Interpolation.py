import numpy as np
import matplotlib.pyplot as plt
import math

class Interpolation:
    
    def do(image, ratio):
        pass
    
    def get_rgb(image, x, y):
        pass
    
    def get_class_name(self):
        return type(self).__name__


class Bilinear(Interpolation):
    def do(image, new_height, new_width):
        height, width, channels = image.get_size()

        height_ratio = height / new_height
        width_ratio = width / new_width

        interpolated_image = np.zeros((new_height, new_width, channels), dtype=np.uint8)

        for y in range(new_height):
            for x in range(new_width):
                src_x = x * width_ratio
                src_y = y * height_ratio

                x1 = int(np.floor(src_x))
                y1 = int(np.floor(src_y))
                x2 = min(x1 + 1, width - 1)
                y2 = min(y1 + 1, height - 1)

                p11 = image.get_rgb(x1, y1)
                p12 = image.get_rgb(x1, y2)
                p21 = image.get_rgb(x1, y2)
                p22 = image.get_rgb(x2, y2)

                for c in range(channels):
                    weight_x = src_x - x1
                    weight_y = src_y - y1

                    interpolated_value = (1 - weight_y) * ((1 - weight_x) * p11[c] + weight_x * p21[c]) + \
                                     weight_y * ((1 - weight_x) * p12[c] + weight_x * p22[c])

                    interpolated_image[y, x, c] = interpolated_value

        return interpolated_image




class Bicubic(Interpolation):
    def do(image, new_height, new_width):

        height, width, channels = image.get_size()


        height_ratio = height / new_height
        width_ratio = width / new_width

        interpolated_image = np.zeros((new_height, new_width, channels), dtype=np.uint8)

        for y in range(new_height):
            for x in range(new_width):
                src_x = x * width_ratio
                src_y = y * height_ratio

                x1 = int(np.floor(src_x)) - 1
                y1 = int(np.floor(src_y)) - 1
                x2 = min(x1 + 4, width - 1)
                y2 = min(y1 + 4, height - 1)

                x1 = max(x1, 0)
                y1 = max(y1, 0)

                pixels = image.get_image[x1:x2 + 1, y1:y2 + 1]

                for c in range(channels):
                    interpolated_value = bicubic_interpolate(pixels[:, :, c], src_x - x1, src_y - y1)

                    interpolated_image[y, x, c] = interpolated_value

        return interpolated_image


    def bicubic_interpolate(pixels, x, y):
        a = -0.5
        def cubic_interpolate(p0, p1, p2, p3, x):
            return p1 + 0.5 * x * (p2 - p0 + x * (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3 + x * (3.0 * (p1 - p2) + p3 - p0)))
        x0 = np.clip(int(np.floor(x)), 0, pixels.shape[1] - 1)
        y0 = np.clip(int(np.floor(y)), 0, pixels.shape[0] - 1)
        x1 = x0 + 1
        y1 = y0 + 1
        p00 = pixels[y0, x0]
        p01 = pixels[y0, x1]
        p02 = pixels[y0, min(x1 + 1, pixels.shape[1] - 1)]
        p03 = pixels[y0, min(x1 + 2, pixels.shape[1] - 1)]
        p10 = pixels[y1, x0]
        p11 = pixels[y1, x1]
        p12 = pixels[y1, min(x1 + 1, pixels.shape[1] - 1)]
        p13 = pixels[y1, min(x1 + 2, pixels.shape[1] - 1)]
        p20 = pixels[min(y1 + 1, pixels.shape[0] - 1), x0]
        p21 = pixels[min(y1 + 1, pixels.shape[0] - 1), x1]
        p22 = pixels[min(y1 + 1, pixels.shape[0] - 1), min(x1 + 1, pixels.shape[1] - 1)]
        p23 = pixels[min(y1 + 1, pixels.shape[0] - 1), min(x1 + 2, pixels.shape[1] - 1)]
        p30 = pixels[min(y1 + 2, pixels.shape[0] - 1), x0]
        p31 = pixels[min(y1 + 2, pixels.shape[0] - 1), x1]
        p32 = pixels[min(y1 + 2, pixels.shape[0] - 1), min(x1 + 1, pixels.shape[1] - 1)]
        p33 = pixels[min(y1 + 2, pixels.shape[0] - 1), min(x1 + 2, pixels.shape[1] - 1)]
        weight_x = x - x0
        weight_y = y - y0
        interpolated_value = np.zeros((1,), dtype=np.float32)


        for c in range(interpolated_value.shape[0]):
            interpolated_value[c] = cubic_interpolate(p00[c], p01[c], p02[c], p03[c], weight_x) + \
                                    a * (cubic_interpolate(p10[c], p11[c], p12[c], p13[c], weight_x) - cubic_interpolate(p00[c], p01[c], p02[c], p03[c], weight_x)) + \
                                    a * (cubic_interpolate(p20[c], p21[c], p22[c], p23[c], weight_x) - cubic_interpolate(p10[c], p11[c], p12[c], p13[c], weight_x)) + \
                                    a ** 2 * (cubic_interpolate(p30[c], p31[c], p32[c], p33[c], weight_x) - cubic_interpolate(p20[c], p21[c], p22[c], p23[c], weight_x))

        return interpolated_value

