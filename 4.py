import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Лабораторная работа №4")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.transformations = []

    def create_widgets(self):
        button_width = 30 

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack(side="top", fill=tk.X, padx=10, pady=10)

        self.open_button = tk.Button(self.frame_buttons, text="Открыть изображение", width=button_width, command=self.open_image)
        self.open_button.pack(side="top", pady=5)

        self.affine_button = tk.Button(self.frame_buttons, text="Афинные преобразования", width=button_width, command=self.affine_transform)
        self.affine_button.pack(side="top", pady=5)

        self.nonlinear_button = tk.Button(self.frame_buttons, text="Нелинейные преобразования", width=button_width, command=self.nonlinear_transform)
        self.nonlinear_button.pack(side="top", pady=5)

        self.save_button = tk.Button(self.frame_buttons, text="Сохранить результат", width=button_width, command=self.save_result)
        self.save_button.pack(side="top", pady=5)

        self.restore_button = tk.Button(self.frame_buttons, text="Восстановить исходное изображение", width=button_width, command=self.restore_original)
        self.restore_button.pack(side="top", pady=5)

        self.image_label = tk.Label(self)
        self.image_label.pack(side="bottom", fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.original_image = None
        self.transformed_image = None

    def open_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = Image.open(path)
            self.transformed_image = self.original_image.copy()
            self.display_image(self.transformed_image)
            self.transformations = []

    def display_image(self, image):
        self.image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image)
        self.image_label.image = self.image

    def affine_transform(self):
        if self.transformed_image:
            # Поворот изображения
            self.transformed_image = self.transformed_image.rotate(45, expand=True)

            # Скос изображения
            width, height = self.transformed_image.size
            matrix = (1, 0.5, 0, 0, 1, 0)  # Скос по оси X
            self.transformed_image = self.transformed_image.transform((width, height), Image.AFFINE, matrix)

            self.display_image(self.transformed_image)
            self.transformations.append(("affine", 45, matrix))

    def nonlinear_transform(self):
        if self.transformed_image:
            array = np.array(self.transformed_image)
            width, height = array.shape[1], array.shape[0]
            transformed_array = np.zeros_like(array)
            coordinates = [] 
            for i in range(height):
                for j in range(width):
                    if i == 0:
                        x_prime = 0
                    else:
                        x_prime = np.log(i)
                    y_prime = j
                    i_prime = int(np.sqrt(np.exp(x_prime)))
                    j_prime = int(y_prime)
                    if 0 <= i_prime < height and 0 <= j_prime < width:
                        transformed_array[i, j] = array[i_prime, j_prime]
                        coordinates.append((i_prime, j_prime)) 
            self.transformed_image = Image.fromarray(transformed_array)
            self.display_image(self.transformed_image)
            self.transformations.append(("nonlinear", coordinates))

    def save_result(self):
        if self.transformed_image:
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if filename:
                self.transformed_image.save(filename)

    def restore_original(self):
        if self.transformations:
            for transformation in reversed(self.transformations):
                if transformation[0] == "affine":
                    angle = -transformation[1]
                    matrix = transformation[2]

                    # Обратный скос
                    inverse_matrix = (1, -matrix[1], 0, -matrix[3], 1, 0)
                    width, height = self.transformed_image.size
                    self.transformed_image = self.transformed_image.transform((width, height), Image.AFFINE, inverse_matrix)

                    # Обратный поворот
                    self.transformed_image = self.transformed_image.rotate(angle, expand=True)
            self.display_image(self.transformed_image)
            self.transformations = []

root = tk.Tk()
app = Application(master=root)
app.mainloop()
