import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

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

data_dir = 'output'
lst = os.listdir(data_dir)
x_train = np.empty((0, 28, 28, 1), dtype=np.uint8)
y_train = []
x_test = np.empty((0, 28, 28, 1), dtype=np.uint8)
y_test = []

if len(lst) == 0:
    raise ValueError("No images found in the output directory.")

for i in range(len(lst[:int(len(lst)*0.8)])):
    c = random.choice(lst)
    image = cv2.imread("output/"+c, cv2.IMREAD_GRAYSCALE)
    lst.remove(c)
    x_train = np.append(x_train, [image.reshape(28, 28, 1)], axis=0)
    y_train.append(ord(c[0]) - ord('A'))  # Convert letter to index

for i in lst:
    z = cv2.imread("output/"+i, cv2.IMREAD_GRAYSCALE)
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

# Normalize the images
x_train = x_train / 255.0
x_test = x_test / 255.0

model.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test))
model.save('letter_recognizer_model.h5')
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc}")