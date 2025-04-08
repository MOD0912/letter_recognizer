'''
Draw a letter on the canvas and the model will predict the letter. 
The confidence of each class is displayed in a bar chart.
'''

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Step 1: Load or Train the MNIST Digit Classifier ---
MODEL_FILE = "letter_recognizer_model.h5"


model = tf.keras.models.load_model(MODEL_FILE)


# Load or train the model

# --- Create the GUI for Drawing Digits ---
class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Letter Recognizer")
        self.pix = 28
        self.count = 0

        # Canvas settings
        self.canvas_width = 280*4 
        self.canvas_height = 280*4
        self.canvas = ctk.CTkCanvas(root, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()#
        self.lst = [[" " for _ in range(int(self.canvas_width/4/self.pix))] for _ in range(int(self.canvas_height/4/self.pix))]
        print(self.lst)
        

        # Draw event
        self.canvas.bind("<B1-Motion>", self.paint)

        # Buttons
        self.clear_button = ctk.CTkButton(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        self.predict_button = ctk.CTkButton(root, text="Predict", command=self.predict)
        self.predict_button.pack()

        # PIL Image for canvas
        self.image = Image.new("L", (280*4, 280*4), color=255)
        self.draw = ImageDraw.Draw(self.image)

        # Load the trained model
        self.model = tf.keras.models.load_model(MODEL_FILE)


        self.draw_grid()

    def draw_grid(self):
        for i in range(0, self.canvas_width, 28*4):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='gray')
        for i in range(0, self.canvas_height, 28*4):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='gray')

    def paint(self, event):
        x, y = event.x, event.y
        brush_size = 10
        self.canvas.create_oval(x, y, x + brush_size, y + brush_size, fill='black')
        self.draw.ellipse([x, y, x + brush_size, y + brush_size], fill=0)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280*4, 280*4), color=255)
        self.draw = ImageDraw.Draw(self.image)
        self.draw_grid()

    def predict(self):
        # Scan the entire canvas in a grid of 14x14 pixels
        for y in range(0, int(self.canvas_height/4), 28):
            for x in range(0, int(self.canvas_width/4), self.pix):
                sub_image = self.image.resize((280, 280), Image.LANCZOS)
                sub_image = sub_image.crop((x, y, x + 28, y + 28)).resize((28, 28), Image.LANCZOS)
                sub_img_array = np.array(sub_image) / 255.0

                if sub_img_array.size != 28 * 28:
                    print(f"Unexpected sub-image array size: {sub_img_array.size}")
                    continue

                sub_img_array = sub_img_array.reshape(28, 28, 1)
                sub_img_array = np.expand_dims(sub_img_array, axis=0)

                sub_predictions = self.model.predict(sub_img_array)
                sub_predicted_class = np.argmax(sub_predictions)
                sub_confidence = np.max(sub_predictions)

                # Convert sub_img_array back to 2D array for saving
                sub_img_2d = (sub_img_array[0].reshape(28, 28) * 255).astype(np.uint8)
                try:
                    cv2.imwrite(f"try/{self.count}_{x}_{y}.png", sub_img_2d)
                except:
                    os.makedirs("try")
                    cv2.imwrite(f"try/{self.count}_{x}_{y}.png", sub_img_2d)
                
                if sub_confidence < 0.8:
                    print(f"Sub-image at ({x}, {y}) - Predicted Digit: {" "}, Confidence: {sub_confidence:.2f} (Low confidence)")
                    sub_predicted_class = " "
                    self.lst[int(y/self.pix)][int(x/self.pix)] = sub_predicted_class
                else:    
                    print(f"Sub-image at ({x}, {y}) - Predicted Digit: {chr(sub_predicted_class + ord('A'))}, Confidence: {sub_confidence:.2f}")
                
                    self.lst[int(y/self.pix)][int(x/self.pix)] = chr(sub_predicted_class + ord('A'))
                self.count += 1
        for i in self.lst:
            print(i)


# --- Launch the Application ---
if __name__ == "__main__":
    if not os.path.exists("try"):
        os.makedirs("try")
    #clear try folder
    for file in os.listdir("try"):
        os.remove(os.path.join("try", file))
    root = ctk.CTk()
    app = DigitRecognizerApp(root)
    root.mainloop()
