import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import numpy as np

class FilterPipeline:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.filtered_image = None
        self.filters = []
        self.canvas = None
        self.image_item = None
        
        self.create_filter_pipeline_gui()
        
    def apply_filters(self):
        self.filtered_image = self.image.copy()
        for filter_func in self.filters:
            self.filtered_image = filter_func(self.filtered_image)
        self.update_image_display(self.filtered_image)
        
    def add_filter(self, filter_func):
        self.filters.append(filter_func)
        self.apply_filters()
        
    def reset_filters(self):
        self.filters = []
        self.apply_filters()
        
    def update_image_display(self, image):
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.image_item, image=image_tk)
        self.canvas.image = image_tk
        
    def load_image(self):
        self.image = Image.open(self.image_path)
        self.filtered_image = self.image.copy()
        self.update_image_display(self.image)
        
    def create_filter_pipeline_gui(self):
        window = tk.Tk()
        window.title("Конвеєр фільтрів")
        
        self.canvas = tk.Canvas(window)
        self.canvas.pack()
        
        self.load_image()
        
        image_tk = ImageTk.PhotoImage(self.image)
        self.image_item = self.canvas.create_image(0, 0, anchor="nw", image=image_tk)
        
        def add_filter():
            filter_func = get_selected_filter()
            self.add_filter(filter_func)
            
        filter_options = [
            ("Відтінок сірого", lambda img: img.convert("L")),
            ("Розмити", lambda img: img.filter(ImageFilter.BLUR)),
            ("Виділити контури", lambda img: img.filter(ImageFilter.SHARPEN)),
        ]
        selected_filter = tk.StringVar()
        selected_filter.set(filter_options[0][0])
        filter_menu = tk.OptionMenu(window, selected_filter, *[option[0] for option in filter_options])
        filter_menu.pack()
        
        add_button = tk.Button(window, text="Додати фільтр", command=add_filter)
        add_button.pack()
        
        reset_button = tk.Button(window, text="Зкинути", command=self.reset_filters)
        reset_button.pack()
        
        def get_selected_filter():
            selected_option = selected_filter.get()
            for option in filter_options:
                if option[0] == selected_option:
                    return option[1]
        
        window.mainloop()

#Приклад використання
pipeline = FilterPipeline("Панда.jpg")
pipeline.create_filter_pipeline_gui()
