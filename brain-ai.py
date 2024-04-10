#from helper import IMAGE_RES
IMAGE_RES = 100
import warnings
warnings.filterwarnings('ignore')


import os
import cv2
import time
import json
import keras
import tensorflow
import numpy as np
import seaborn as sns
from PIL import Image
import tensorflow as tf
from keras import backend as K
import matplotlib.pyplot as plt
from keras.regularizers import l2
from sklearn.metrics import confusion_matrix
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import image
from keras.optimizers.schedules import ExponentialDecay
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping,
    LearningRateScheduler,
    ReduceLROnPlateau,
)
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout,
    BatchNormalization,
)

# training

# define the subdirectory where you training data is located
training_sub = "data/train"
testing_sub = "data/test"

training_path = "/kaggle/input/fer2013/train"
validation_path = "/kaggle/input/fer2013/test"




datagen = ImageDataGenerator(
    rescale=1./255,  #normalize pixel values to be between 0 and 1
    #horizontal_flip=True,  #randomly flip images horizontally
    #validation_split=0.3 # set data split
)

target_size = (IMAGE_RES, IMAGE_RES)  
batch_size = 32

train_generator = datagen.flow_from_directory(
    training_path,
    target_size=target_size,
    batch_size=batch_size,
    class_mode="categorical", 
  
)

validation_generator = datagen.flow_from_directory(
    validation_path,
    target_size=target_size,
    batch_size=batch_size,
    class_mode="categorical", 
   
)

class_names = os.listdir(training_path)

num_rows = 3  
num_cols = (len(class_names) + num_rows - 1) // num_rows

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 6))


for i, class_name in enumerate(class_names):
    class_path = os.path.join(training_path, class_name)

    image_files = [
        f for f in os.listdir(class_path) if f.endswith(".jpg") or f.endswith(".png")
    ]

    img_path = os.path.join(class_path, image_files[0])
    img = image.load_img(img_path, target_size=target_size)
    axs[i // num_cols, i % num_cols].imshow(img)
    axs[i // num_cols, i % num_cols].set_title(f"Class: {class_name}")
    axs[i // num_cols, i % num_cols].axis("off")


plt.tight_layout()


plt.show()

num_train_samples = train_generator.samples
num_validation_samples = validation_generator.samples
num_classes = train_generator.num_classes
class_indices = train_generator.class_indices
file_name = "data_lookup_train.json"

with open(file_name, "w") as json_file:
    json.dump(class_indices, json_file)


print(f"Number of training samples: {num_train_samples}")
print(f"Number of validation samples: {num_validation_samples}")
print(f"Number of classes: {num_classes}")
print(f"Class indices: {class_indices}")

#num_classes = len(directory_reverse_lookup.keys())
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Dropout, Flatten

# Load the VGG16 model, excluding the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMAGE_RES, IMAGE_RES, 3))

# Freeze the base model's layers to prevent training them
for layer in base_model.layers:
    layer.trainable = False

    

x = base_model.output
x = Flatten()(x)
x = Dense(64, activation='relu')(x)
x = Dropout(0.5)(x)

predictions = Dense(num_classes, activation='softmax')(x)
model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)


# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])


def lr_scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * 0.1

checkpoint = ModelCheckpoint(
    'best_weights.keras',
    monitor='val_loss',  
    save_best_only=True,
    mode='min',  
    verbose=1
)


#model = models.Sequential([
#    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_RES, IMAGE_RES, 3)),
#    layers.MaxPooling2D((2, 2)),
#    layers.Conv2D(64, (3, 3), activation='relu'),
#    layers.MaxPooling2D((2, 2)),
#    layers.Conv2D(64, (3, 3), activation='relu'),
#    layers.Flatten(),
#    layers.Dense(64, activation='relu'),
#    layers.Dense(num_classes, activation='softmax')
#])



early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
lr_schedule = ReduceLROnPlateau(
    monitor="val_loss", factor=0.1, patience=5, min_lr=1e-6, verbose=1
)
model.summary()

history = model.fit(
    train_generator,
    steps_per_epoch=num_train_samples // batch_size,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=num_validation_samples // batch_size,
    callbacks=[early_stopping, lr_schedule, checkpoint],
)

# Save the model weights
model.save_weights('model_weights.weights.h5')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()


