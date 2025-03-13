import customtkinter as ctk
import tensorflow.python as tf
from tensorflow.python.keras.models import load_model

from PIL import Image, ImageOps, ImageGrab
import numpy as np
import io

class Main(ctk.CTk):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.title('Letter Recognizer')
        self.canvas = ctk.CTkCanvas(self, width=280, height=280, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2)
        
        self.clear_button = ctk.CTkButton(self, text='Clear', command=self.clear)
        self.clear_button.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        self.label = ctk.CTkLabel(self, text="", font=("Helvetica", 24))
        self.label.grid(row=2, column=0, columnspan=2)
        
        self.line_id = None
        self.line_points = []
        self.line_options = {}

        self.canvas.bind('<Button-1>', self.set_start)
        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.end_line)
        
        self.update_prediction()

    def draw_line(self, event):
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.canvas.delete(self.line_id)
        self.line_id = self.canvas.create_line(self.line_points, **self.line_options, width=15, fill='black')

    def set_start(self, event):
        self.line_points.extend((event.x, event.y))

    def end_line(self, event=None):
        self.line_points.clear()
        self.line_id = None
    
    def clear(self):
        self.canvas.delete('all')
        self.line_id = None
        self.line_points = []
        self.line_options = {}

    def capture(self):
        """Capture the drawing from the canvas"""
        wid = self.canvas
        x0 = wid.winfo_rootx()
        y0 = wid.winfo_rooty()
        x1 = x0 + wid.winfo_width()
        y1 = y0 + wid.winfo_height()

        im = ImageGrab.grab(bbox=(x0, y0, x1, y1))
        im = im.resize((28, 28))
        im = ImageOps.invert(im.convert('L'))
        input_image = np.expand_dims(im, axis=0)
        input_image = np.expand_dims(input_image, axis=-1) / 255.0
        prediction = self.model.predict(input_image)
        predicted_class = np.argmax(prediction)
        self.label.configure(text=chr(predicted_class + ord('A')))
        print(f"Predicted class: {predicted_class}")
        print(prediction)
        
    def update_prediction(self):
        self.capture()
        self.after(500, self.update_prediction)

model = load_model('letter_recognizer_model.h5')


main = Main(model)
main.mainloop()
