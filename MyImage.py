import matplotlib.pyplot as plt

class MyImage:
    def __init__(self, path): 
        self.__path = path
        self.image = plt.imread(self.__path)
        
    def image_to_array(image): #поки ніде не використовується
        return asarray(image)
    
    def array_to_image(array):  #поки ніде не використовується
        return Image.fromarray(array)
    
    def get_rgb(self, x, y): 
        return self.image[y][x]
    
    def set_rgb(self, x, y, r, g, b): 
        self.image[y][x] = r, g, b

    def get_size(self): # тут лучче назвать get_shatpe
        return self.image.shape
        
    def get_height(self):  
        return self.get_size()[0]
    
    def get_width(self):  
        return self.get_size()[1]
    
    def get_path(self):  
        return self.__path
    
    def get_image(self): #поки ніде не використовується
        return self.image

    def set_image(self, new_image):
        self.image = new_image


