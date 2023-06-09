import numpy as np

class Transformation:
    
    def get_class_name(self):
        return type(self).__name__
    
    def do():
        pass

class Scale(Transformation):

    def do(image, ratio):
        height, width, channels = image.shape

        new_height = int(height * ratio)
        new_width = int(width * ratio)

        scaled_image = np.zeros((new_height, new_width, channels), dtype=np.uint8)

        for y in range(new_height):
            for x in range(new_width):
                src_x = int(x / ratio)
                src_y = int(y / ratio)

                pixel_value = image[src_y, src_x]

                scaled_image[y, x] = pixel_value

        return scaled_image

        

class Rotate(Transformation):
   
    def do(image, angle):
        height, width, channels = image.shape
        
        angle_rad = np.deg2rad(angle)

        center_x = width / 2
        center_y = height / 2

        rotated_image = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                offset_x = x - center_x
                offset_y = y - center_y

                new_x = int(offset_x * np.cos(angle_rad) - offset_y * np.sin(angle_rad) + center_x)
                new_y = int(offset_x * np.sin(angle_rad) + offset_y * np.cos(angle_rad) + center_y)

                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated_image[y, x] = image[new_y, new_x]

        return rotated_image 


class Jitter(Transformation):
    
    def do(image, max_offset):
        height, width, channels = image.shape

        jittered_image = np.zeros_like(image)

        offset_x = np.random.randint(-max_offset, max_offset + 1)
        offset_y = np.random.randint(-max_offset, max_offset + 1)

        for y in range(height):
            for x in range(width):
                new_x = x + offset_x
                new_y = y + offset_y

                if 0 <= new_x < width and 0 <= new_y < height:
                    jittered_image[new_y, new_x] = image[y, x]

        return jittered_image

