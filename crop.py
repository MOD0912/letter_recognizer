import os
from PIL import Image, ImageTk
import customtkinter as ctk

'''
Crop images to the desired size
'''


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.file = 0
        
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.label = ctk.CTkLabel(self, text=" ")
        exitb = ctk.CTkButton(self, text="Exit", command=self.quit)
        save = ctk.CTkButton(self, text="Save", command=self.save)
        self.entry = ctk.CTkEntry(self, placeholder_text="x, y")
        self.entry2 = ctk.CTkEntry(self, placeholder_text="width, height")
        
        self.bind("<Return>", self.crop)
        
        save.grid(row=1, column=0, sticky="nsew")
        exitb.grid(row=1, column=1, sticky="nsew")
        self.label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.entry.grid(row=2, column=0, sticky="nsew", columnspan=2)
        self.entry2.grid(row=3, column=0, sticky="nsew", columnspan=2)
        
        self.open()
    
    def save(self):
        '''
        440 450
        1500 2475
        
        500 540
        1400 2320
        '''
        self.cropimage.save(f"pictures/{self.file}_copy.jpg")
        self.file += 1
        self.open()
        

    def crop(self, event):
        self.x, self.y = self.entry.get().split(",")
        self.width, self.height = self.entry2.get().split(",")
        self.x = int(self.x)
        self.y = int(self.y)
        self.width = int(self.width)
        self.height = int(self.height)
        print(self.x, self.y)
        print(self.width, self.height)
        self.cropimage = self.image.crop((self.x, self.y, self.x+self.width, self.y+self.height))
        self.label.configure(image=ctk.CTkImage(self.cropimage, size=(self.cropimage.size[0]/4, self.cropimage.size[1]/4)))
        
    def open(self):
        self.image = Image.open(f"pictures/{self.file}.jpg")
        self.label.configure(image=ctk.CTkImage(self.image, size=(self.image.size[0]/4, self.image.size[1]/4)))
        print(self.image.size)
    
if __name__ == "__main__":
    Main().mainloop()