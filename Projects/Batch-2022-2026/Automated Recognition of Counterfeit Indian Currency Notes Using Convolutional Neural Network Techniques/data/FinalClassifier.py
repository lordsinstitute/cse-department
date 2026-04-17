import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from glob import glob
import os

def create_model():
    # dataset of fake real recognition
    train_path = '../Indian Currency Dataset/train'
    validation_path = '../Indian Currency Dataset/test'
    save_dir = '../saved_models'
    vis_dir = '../static/vis'

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    # no. of classes in recognition data
    class_names = glob(train_path + "/*")
    num_classes = len(class_names)
    print("Number of Classes:", num_classes)

    # Data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1 / 255,
        shear_range=0.3,
        horizontal_flip=True,
        zoom_range=0.3
    )
    val_datagen = ImageDataGenerator(rescale=1 / 255)

    batch_size = 10

    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=batch_size,
        color_mode="rgb",
        class_mode="categorical"
    )

    val_generator = val_datagen.flow_from_directory(
        validation_path,
        target_size=(224, 224),
        batch_size=batch_size,
        color_mode="rgb",
        class_mode="categorical"
    )

    # CNN Model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),

        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Callbacks
    checkpoint_path = os.path.join(save_dir, 'best_model.h5')
    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    earlystop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)

    # Train model
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=20,
        callbacks=[checkpoint, earlystop],
        verbose=1
    )

    # Save final model
    final_model_path = os.path.join(save_dir, 'final_model.h5')
    model.save(final_model_path)
    print(f"✅ Final model saved at: {final_model_path}")
    print(f"✅ Best model saved at: {checkpoint_path}")

    # Save performance metrics
    history_df = pd.DataFrame(history.history)
    metrics_csv = os.path.join(save_dir, 'training_metrics.csv')
    history_df.to_csv(metrics_csv, index=False)
    print(f"✅ Training metrics saved at: {metrics_csv}")

    # Plot accuracy
    plt.figure()
    plt.plot(history.history['accuracy'], 'go--', label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], 'ro--', label='Validation Accuracy')
    plt.title('Accuracy vs Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    acc_path = os.path.join(vis_dir, 'accuracy_plot.jpg')
    plt.savefig(acc_path)
    print(f"✅ Accuracy plot saved at: {acc_path}")

    # Plot loss
    plt.figure()
    plt.plot(history.history['loss'], 'bo--', label='Training Loss')
    plt.plot(history.history['val_loss'], 'ro--', label='Validation Loss')
    plt.title('Loss vs Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    loss_path = os.path.join(vis_dir, 'loss_plot.jpg')
    plt.savefig(loss_path)
    print(f"✅ Loss plot saved at: {loss_path}")

    return model, history_df


if __name__ == "__main__":
    create_model()
