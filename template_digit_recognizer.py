'''
Draw a letter on the canvas and the model will predict the letter. 
The confidence of each class is displayed in a bar chart.
'''


import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
import numpy as np
import tkinter as tk
from tkinter import messagebox  # Import messagebox
from PIL import Image, ImageDraw, ImageOps
import os
import threading
import cv2
import matplotlib.pyplot as plt  # Import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Step 1: Load or Train the MNIST Digit Classifier ---
MODEL_FILE = "letter_recognizer_model.h5"

def load_or_train_model():
    if os.path.exists(MODEL_FILE):
        print("Loading preexisting model...")
        model = tf.keras.models.load_model(MODEL_FILE)
    else:
        print("No preexisting model found. Training a new model...")
       

# Load or train the model
model = load_or_train_model()

# --- Create the GUI for Drawing Digits ---
class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Digit Recognizer")

        # Canvas settings
        self.canvas_width = 280  # Scaled-up canvas size
        self.canvas_height = 280
        self.canvas = tk.Canvas(root, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Draw event
        self.canvas.bind("<B1-Motion>", self.paint)

        # Buttons
        self.predict_button = tk.Button(root, text="Predict", command=self.predict)
        self.predict_button.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        # PIL Image for canvas
        self.image = Image.new("L", (28, 28), color=255)  # 28x28 pixel grayscale image with white background
        self.draw = ImageDraw.Draw(self.image)

        # Load the trained model
        self.model = tf.keras.models.load_model(MODEL_FILE)
        
        self.status_label = tk.Label(root, text=" ")
        self.status_label.pack()
        self.count = 0
        self.fig, self.ax = plt.subplots(figsize=(10, 5))  # Create a figure and axis for plotting
        self.bars = self.ax.bar(range(26), np.zeros(26))  # Initialize bars with zero height
        self.ax.set_xlabel('Class')
        self.ax.set_ylabel('Confidence')
        self.ax.set_title('Confidence of Each Class')
        self.ax.set_xticks(range(26))
        self.ax.set_xticklabels([chr(i + ord('A')) for i in range(26)])
        self.figure_canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack()
        threading.Thread(target=self.predict).start()

    def paint(self, event):
        x, y = event.x, event.y
        brush_size = 10  # Reduce brush size
        # Scale coordinates to the 28x28 image size
        scaled_x = x * (28 / self.canvas_width)
        scaled_y = y * (28 / self.canvas_height)
        self.canvas.create_oval(x, y, x + brush_size, y + brush_size, fill='black')
        self.draw.ellipse([scaled_x, scaled_y, scaled_x + (brush_size * (28 / self.canvas_width)), scaled_y + (brush_size * (28 / self.canvas_height))], fill=0)  # Draw smaller brush strokes

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (28, 28), color=255)  # White background
        self.draw = ImageDraw.Draw(self.image)

    def predict(self):
        self.count += 1
        # Convert the drawn image to a NumPy array
        img_resized = self.image.resize((28, 28), Image.LANCZOS)  # Use Image.LANCZOS for resizing
        img_array = np.array(img_resized) / 255.0  # Normalize to 0-1 range
        cv2.imwrite(f"try/{self.count}.png", img_array * 255)  # Save the image in the correct format
        
        img_array = img_array.reshape(1, 28, 28)

        # Make a prediction
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)

        # Update the plot with the correct prediction confidences
        for bar, new_height in zip(self.bars, predictions[0]):
            bar.set_height(new_height)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.figure_canvas.draw()
        
        # Display the result
        print(f"Predicted Digit: {chr(predicted_class + ord('A'))}, Confidence: {confidence:.2f}")
        self.status_label.config(text=f"Predicted Digit: {chr(predicted_class + ord('A'))}, Confidence: {confidence:.2f}")
        self.predict()

# --- Launch the Application ---
if __name__ == "__main__":
    #clear try folder
    for file in os.listdir("try"):
        os.remove(os.path.join("try", file))
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()
