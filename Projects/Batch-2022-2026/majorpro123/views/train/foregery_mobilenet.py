# ================================
# Import necessary libraries
# ================================
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(2)

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from PIL import Image, ImageChops, ImageEnhance
import os
import itertools


# ================================
# ELA Conversion
# ================================
def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'

    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, temp_image)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1

    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image


# ================================
# Prepare Images (NO flattening)
# ================================
image_size = (224, 224)   # MobileNet requires 224x224

def prepare_image(image_path):
    img = convert_to_ela_image(image_path, 90).resize(image_size)
    img = np.array(img)
    img = preprocess_input(img)  # IMPORTANT for MobileNet
    return img


X = []
Y = []

# ================================
# Load Authentic Images
# ================================
path = '../casia-dataset/CASIA2/Au/'
for dirname, _, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith(('jpg', 'png')):
            full_path = os.path.join(dirname, filename)
            X.append(prepare_image(full_path))
            Y.append(1)

X = X[:2100]
Y = Y[:2100]

# ================================
# Load Tampered Images
# ================================
path = '../casia-dataset/CASIA2/Tp/'
for dirname, _, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith(('jpg', 'png')):
            full_path = os.path.join(dirname, filename)
            X.append(prepare_image(full_path))
            Y.append(0)

print("Total images:", len(X))


# ================================
# Convert to numpy
# ================================
X = np.array(X)
Y = to_categorical(Y, 2)

X_train, X_val, Y_train, Y_val = train_test_split(
    X, Y, test_size=0.2, random_state=5
)


# ================================
# Build MobileNet Model
# ================================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False  # Freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
output = Dense(2, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.summary()


# ================================
# Compile Model
# ================================
epochs = 30
batch_size = 32

optimizer = Adam(learning_rate=1e-4)

model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

early_stopping = EarlyStopping(
    monitor='val_accuracy',
    patience=3,
    verbose=1,
    mode='max'
)


# ================================
# Train Model
# ================================
hist = model.fit(
    X_train,
    Y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_val, Y_val),
    callbacks=[early_stopping]
)


# ================================
# Save Model
# ================================
model.save("../models/mobilenet_casia_model.h5")


# ================================
# Plot Accuracy & Loss
# ================================
fig, ax = plt.subplots(2, 1)

ax[0].plot(hist.history['loss'], label="Train Loss")
ax[0].plot(hist.history['val_loss'], label="Val Loss")
ax[0].legend()

ax[1].plot(hist.history['accuracy'], label="Train Acc")
ax[1].plot(hist.history['val_accuracy'], label="Val Acc")
ax[1].legend()

plt.savefig('../static/performance/acc_loss_mobilenet.jpg')
plt.clf()


# ================================
# Confusion Matrix
# ================================
Y_pred = model.predict(X_val)
Y_pred_classes = np.argmax(Y_pred, axis=1)
Y_true = np.argmax(Y_val, axis=1)

cm = confusion_matrix(Y_true, Y_pred_classes)

plt.imshow(cm, cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xticks(range(2), ["Fake", "Real"])
plt.yticks(range(2), ["Fake", "Real"])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center")

plt.ylabel("True Label")
plt.xlabel("Predicted Label")

plt.savefig('../static/performance/cnf_mobilenet.jpg')
plt.clf()


model.save("../models/best_model_mobilenet.h5")