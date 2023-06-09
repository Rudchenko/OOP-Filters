import tkinter as tk
from PIL import ImageTk, Image, ImageDraw

class ImageCropper:
    def __init__(self, image_path):
        self.image_path = image_path
        self.crop_coordinates = None
        self.points = []
        self.canvas = None
        self.window = None
        
    def draw_selection_line(self):
        if len(self.points) >= 2 and self.canvas is not None:
            self.canvas.delete("selection")
            self.canvas.create_line(self.points, fill="red", tags="selection")
        
    def on_left_click(self, event):
        self.points.append((event.x, event.y))
        self.draw_selection_line()
        
    def on_mouse_move(self, event):
        self.draw_selection_line()
        
    def save_cropped_image(self):
        if len(self.points) >= 2:
            image = Image.open(self.image_path)
            mask_image = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask_image)
            draw.polygon(self.points, fill=255)
                
            cropped_image = Image.new("RGBA", image.size)
            cropped_image.paste(image, mask=mask_image)
            cropped_image.save("cropped_image.png")
            print("Зображення обрізано та збережено як 'cropped_image.png'.")
            self.points = []  # Очищення списку точок
            self.draw_selection_line()  # Оновлення відображення на полотні
        
    def crop_image_custom_shape(self):
        self.window = tk.Tk()
        image = Image.open(self.image_path)
        self.window.geometry(f"{image.width}x{image.height}")
        
        self.canvas = tk.Canvas(self.window, width=image.width, height=image.height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        
        button = tk.Button(self.window, text="Зберегти", command=self.save_cropped_image)
        button.pack()
        
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=image_tk)
        
        self.window.mainloop()

#cropper = ImageCropper("Панда.jpg")
#cropper.crop_image_custom_shape()
