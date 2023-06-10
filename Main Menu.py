import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfilename
import os
from PIL import ImageTk, Image, ImageDraw, ImageFilter, ImageEnhance
from PIL import ImageGrab
from tkinter import filedialog
from ipycanvas import Canvas
from tkinter import simpledialog, messagebox
import PIL
import numpy as np

from MyImage import *
from Transformation import *
from Filters import *
from Interpolation import *

def convert_array_to_photo(im):
    image = Image.fromarray(im.get_image()) 
    image_tk = ImageTk.PhotoImage(image)

    return image_tk

def load_file():    
    filepath = filedialog.askopenfilename(title="Вибрати фото")

    if filepath:
        global image
        global resized_image
        image = MyImage(filepath)
        
        resized_image = image
        
        root.geometry(f"{image.get_width()}x{image.get_height()}")
        
        photo = convert_array_to_photo(image)
        
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.resized_image = photo  
        message_label.config(text=filepath)  
        return


def save_image(): 
    global resized_image 
    if 'resized_image' in globals():
        filepath = asksaveasfilename(title="Зберегти фото", defaultextension=".jpg",
                                                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])

        resized_image_PIL = Image.fromarray(resized_image.get_image()) 
        resized_image_PIL.save("output.jpg") 
        
        resized_image_PIL.save(filepath)


draw_active = False

def draw():
    global resized_image, draw_active, stop_button

    if 'image' in globals():
        if draw_active:
            return  

        draw_active = True
        print(type(resized_image))

        resized_image_PIL = Image.fromarray(resized_image.get_image()) 

        resized_image_PIL.save("output.jpg") 
        
        draw = ImageDraw.Draw(resized_image_PIL)
        photo = ImageTk.PhotoImage(resized_image_PIL)
        canvas.create_image(0, 0, anchor="nw", image=photo)

        def get_x_and_y(event):
            global lasx, lasy
            lasx, lasy = event.x, event.y

        def draw_smth(event):
            global lasx, lasy
            canvas.create_line((lasx, lasy, event.x, event.y), fill='red', width=4)
            draw.line((lasx, lasy, event.x, event.y), fill='red', width=4)
            lasx, lasy = event.x, event.y

        def stop_drawing():
            global draw_active, stop_button
            draw_active = False
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")
            stop_button.destroy()  

        canvas.bind("<Button-1>", get_x_and_y)
        canvas.bind("<B1-Motion>", draw_smth)

        stop_button = tk.Button(root, text="Stop Drawing", command=stop_drawing)
        stop_button.pack()
    else:
        message_label.config(text="Жодне фото не завантажено.")

    return



def change_size():  #DONE
    if 'image' in globals():
        ratio = tk.simpledialog.askfloat("Коефіцієнт розміру зображення",
                                         "Введіть коефіцієнт розміру зображення:")

        if ratio is not None:
            image.set_image(Scale.do(image.get_image(), ratio))
        
            root.geometry(f"{image.get_width()}x{image.get_height()}")

            photo = convert_array_to_photo(image)

            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def rotate_image(): #DONE
    if 'image' in globals():
        degree = simpledialog.askfloat("Кут повороту",
                                       "Додатній або від'ємний кут повороту:")
        if degree is not None:
            image.set_image(Rotate.do(image.get_image(), degree))
            
            root.geometry(f"{image.get_width()}x{image.get_height()}")
            
            photo = convert_array_to_photo(image)
            
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def create_dialog():
    global resized_image
    dialog = tk.Toplevel(root)
    dialog.transient(root)
    dialog.title("Вирізати зображення")
    
    width_label = tk.Label(dialog, text=f"Максимальний x на тепер: {resized_image.get_height()}")
    width_label.pack()
    
    height_label = tk.Label(dialog, text=f"Максимальний y на тепер: {resized_image.get_height()}")
    height_label.pack()
    

    x1_label = tk.Label(dialog, text="x-координата лівого верхнього кута:")
    x1_entry = tk.Entry(dialog)
    x1_label.pack()
    x1_entry.pack()

    x2_label = tk.Label(dialog, text="x-координата правого нижнього кута:")
    x2_entry = tk.Entry(dialog)
    x2_label.pack()
    x2_entry.pack()

    y1_label = tk.Label(dialog, text="y-координата верхнього лівого кута:")
    y1_entry = tk.Entry(dialog)
    y1_label.pack()
    y1_entry.pack()

    y2_label = tk.Label(dialog, text="y-координата правого нижнього кута:")
    y2_entry = tk.Entry(dialog)
    y2_label.pack()
    y2_entry.pack()

    confirm_button = tk.Button(dialog, text="Підтвердити", command=lambda: process_dialog(dialog, x1_entry.get(), y1_entry.get(), x2_entry.get(), y2_entry.get()))
    confirm_button.pack()

def process_dialog(dialog, x1, y1, x2, y2):
    dialog.destroy()

    if 'resized_image' in globals():
        global resized_image
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)


        resized_image_PIL = Image.fromarray(resized_image.get_image()) 
        resized_image_PIL.save("output.jpg") 

        resized_image_PIL = resized_image_PIL.crop((x1, y1, x2, y2))
        root.geometry(f"{resized_image_PIL.width}x{resized_image_PIL.height}")
        photo = ImageTk.PhotoImage(resized_image_PIL)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def cut_image():
    global resized_image
    create_dialog()
        
        

def interpol_line(): #DONE
    if 'image' in globals():
        ratio = simpledialog.askfloat("Рівень лінійної інтерполяції",
                                       "Введіть рівень лінійної інтерполяції:")
        if ratio is not None:
            image.set_image(Bilinear.do(image, image.get_height()*int(ratio),
                                        image.get_width()*int(ratio)))
        
            root.geometry(f"{image.get_width()}x{image.get_height()}")
        
            photo = convert_array_to_photo(image)
        
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")


def interpol_cubic(): #DONE
    if 'image' in globals():
        ratio = simpledialog.askfloat("Рівень бікубічної інтерполяції",
                                       "Введіть рівень бікубічної інтерполяції:")
        if ratio is not None:
            image.set_image(Bicubic.do(image, image.get_height()*int(ratio),
                                        image.get_width()*int(ratio)))
        
            root.geometry(f"{image.get_width()}x{image.get_height()}")
        
            photo = convert_array_to_photo(image)
        
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")


def apply_bw_filter():#DONE
    if 'image' in globals():
        gamma = simpledialog.askfloat("Рівень сірості",
                                       "Введіть рівень сірості:")
        if gamma is not None:
            image.set_image(Grayscale.do(image.get_image(), gamma))
        
            root.geometry(f"{image.get_width()}x{image.get_height()}")

            photo = convert_array_to_photo(image)
            
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def apply_blur_filter():#DONE
    if 'image' in globals():
        degree = simpledialog.askfloat("Рівень розмиття",
                                       "Введіть рівень розмиття:")
        if degree is not None:
            image.set_image(Blur.do(image.get_image(), int(degree)))
            
            root.geometry(f"{image.get_width()}x{image.get_height()}")
            
            photo = convert_array_to_photo(image)
            
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def apply_Brightness_filter():#DONE
    if 'image' in globals():
        degree = simpledialog.askfloat("Рівень яскравості",
                                       "Введіть рівень яскравості:")
        if degree is not None:
            image.set_image(Brightness.do(image.get_image(), degree))
            
            root.geometry(f"{image.get_width()}x{image.get_height()}")

            photo = convert_array_to_photo(image)
            
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.resized_image = photo
    else:
        message_label.config(text="Жодне фото не завантажено.")

def create_pipeline():
    about_text = "Тут Ви можете поєднати фільтри"

    window = tk.Tk()
    window.title("Вибери поєднання")

    label = tk.Label(window, text=about_text)
    label.pack()

    button1 = tk.Button(window, text="Відтінок сірого + яскравість", command=lambda: (apply_bw_filter(), apply_Brightness_filter(), window.destroy()))
    button1.pack()

    button2 = tk.Button(window, text="Розмиття + яскравість", command=lambda: (apply_blur_filter(),  apply_Brightness_filter(), window.destroy()))
    button2.pack()


    window.mainloop()

def show_about_info(): #DONE
    about_text = "Це програма для завантаження, редагування та збереження зображень.\n\n"\
                 "Ви можете вибрати фото, малювати на ньому, змінювати розмір, робити інтерполяцію, "\
                 "повертати, обрізати та застосовувати фільтри.\n\n"\
                 "Щоб почати, оберіть пункт меню 'Файл' та виберіть 'Завантажити', "\
                 "щоб завантажити зображення."
    messagebox.showinfo("Про застосунок", about_text)

root = tk.Tk()
root.title("Редактор фото")
root.geometry("300x300")

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

menubar = Menu(root)

message_label = tk.Label(root, text="")
message_label.pack()

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Файл", menu=filemenu)
filemenu.add_command(label="Завантажити", command=load_file)
filemenu.add_command(label="Зберегти", command=save_image)
filemenu.add_separator()
filemenu.add_command(label="Вийти", command=root.quit)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Редактувати", menu=edit_menu)
edit_menu.add_command(label="Малювати", command=draw)
edit_menu.add_command(label="Змінити розмір", command=change_size)
edit_menu.add_command(label="Повернути", command=rotate_image)
edit_menu.add_command(label="Обрізати", command=cut_image)
edit_menu.add_command(label="Створити конвеєр", command=create_pipeline)

# Додавання підвкладок до підвкладки "Інтерполяція"
interpolation_menu = tk.Menu(edit_menu, tearoff=0)
edit_menu.add_cascade(label="Інтерполяція", menu=interpolation_menu)
interpolation_menu.add_command(label="Лінійна", command=interpol_line)
interpolation_menu.add_command(label="Кубічна", command=interpol_cubic)

# Додавання підвкладок до підвкладки "Фільтри"
filters_menu = tk.Menu(edit_menu, tearoff=0)
edit_menu.add_cascade(label="Фільтри", menu=filters_menu)
filters_menu.add_command(label="Віттінок сірого", command=apply_bw_filter)
filters_menu.add_command(label="Розмиття зображення", command=apply_blur_filter)
filters_menu.add_command(label="Зміна яскравості", command=apply_Brightness_filter)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Допомога", menu=helpmenu)
helpmenu.add_command(label="Про застосунок", command=show_about_info)

root.config(menu=menubar)

root.mainloop()
