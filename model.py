'''
This script trains a model to recognize letters from images.
'''

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
from PIL import Image
import random
import numpy as np
import cv2

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(26, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

data_dir = "BigDataSet"
lst2 = os.listdir(data_dir)  
lst = []
print(lst2)
for i in lst2:
    files = os.listdir(os.path.join(data_dir, i))
    lst.extend(files)
        
# data_dir = 'output'
# lst = os.listdir(data_dir)

print(f"lst: {len(lst)}")   
x_train = np.empty((0, 28, 28, 1), dtype=np.uint8)
y_train = []
x_test = np.empty((0, 28, 28, 1), dtype=np.uint8)
y_test = []
if len(lst) == 0:
    raise ValueError("No images found in the output directory.")

for i in range(len(lst[:int(len(lst) * 0.8)])):
    c = random.choice(lst)
    image_path = f"BigDataSet/{c[0]}/" + c
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Warning: Could not read image {image_path}")
        continue
    image = cv2.resize(image, (28, 28))  # Ensure the image is resized to 28x28
    lst.remove(c)
    x_train = np.append(x_train, [image.reshape(28, 28, 1)], axis=0)
    y_train.append(ord(c[0]) - ord('A'))  # Convert letter to index

for i in lst:
    image_path = f"BigDataSet/{i[0]}/" + i
    z = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if z is None:
        print(f"Warning: Could not read image {image_path}")
        continue
    z = cv2.resize(z, (28, 28))  # Ensure the image is resized to 28x28
    x_test = np.append(x_test, [z.reshape(28, 28, 1)], axis=0)
    y_test.append(ord(i[0]) - ord('A'))  # Convert letter to index

# Convert labels to numpy arrays
y_train = np.array(y_train)
y_test = np.array(y_test)

# Convert labels to one-hot encoded vectors
y_train = to_categorical(y_train, num_classes=26)
y_test = to_categorical(y_test, num_classes=26)

print()
print(f"lst: {len(lst)}, train: {(x_train.shape)}, test: {(x_test.shape)}")

print()
print(type(x_train))
print(type(y_train))
print(type(x_test))
print(type(y_test))

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False, 
    fill_mode="nearest"
)

# Normalize the images
x_train = x_train / 255.0
x_test = x_test / 255.0

# Fit the model using data augmentation
model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=100, validation_data=(x_test, y_test))

model.save('letter_recognizer_model.h5')
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc}")