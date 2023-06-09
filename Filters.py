import numpy as np

class Filter:

    def get_class_name(self):
        return type(self).__name__

    def do():
        pass

class Grayscale(Filter):

    def do(image, gamma=1.0):
        height, width, channels = image.shape
    
        grayscale_image = np.zeros((height, width), dtype=np.uint8)
    
        for y in range(height):
            for x in range(width):
                r, g, b = image[y, x]
            
                gray_value = int((0.2989 * r + 0.5870 * g + 0.1140 * b) ** gamma)
            
                gray_value = np.clip(gray_value, 0, 255)
            
                grayscale_image[y, x] = gray_value
    
        return grayscale_image


class Blur(Filter):

    def do(image, degree):
        kernel_size = 2 * degree + 1
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size * kernel_size)
        blurred_image = Blur.convolve(image, kernel)

        return blurred_image
    

    def convolve(image, kernel):
        height, width, channels = image.shape
        kernel_size = kernel.shape[0]
        offset = kernel_size // 2
        padded_image = np.pad(image, ((offset, offset), (offset, offset), (0, 0)), mode='constant')
        result = np.zeros_like(image)
    
        for i in range(height):
            for j in range(width):
                for c in range(channels):
                    patch = padded_image[i:i+kernel_size, j:j+kernel_size, c]
                    result[i, j, c] = np.sum(patch * kernel)
    
        return result


class Brightness(Filter):
    
    def do(image, degree):
        height, width, channels = image.shape
        adjusted_image = np.zeros((height, width, channels), dtype=np.uint8)
    
        for y in range(height):
            for x in range(width):
                for c in range(channels):
                    adjusted_value = image[y, x, c] + degree
                    adjusted_value = max(0, min(255, adjusted_value))
                    adjusted_image[y, x, c] = adjusted_value
    
        return adjusted_image

