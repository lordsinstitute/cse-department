import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from glob import glob
import os

def create_model():
    # Dataset paths
    train_path = '../Indian Currency Dataset/train'
    validation_path = '../Indian Currency Dataset/test'
    save_dir = '../saved_models_mnet'
    vis_dir = '../static/vis/mnet'

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    # Number of classes
    class_names = glob(train_path + "/*")
    num_classes = len(class_names)
    print("Number of Classes:", num_classes)

    # ✅ Advanced Data Augmentation
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.3,
        shear_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    batch_size = 16

    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        validation_path,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # ✅ Use Transfer Learning (MobileNetV2)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze base layers for faster convergence

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    output = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)

    # ✅ Compile with learning rate scheduler
    opt = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    # ✅ Callbacks for performance tuning
    checkpoint_path = os.path.join(save_dir, 'best_model.h5')
    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    earlystop = EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3, verbose=1, min_lr=1e-6)

    # ✅ Train model
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=25,
        callbacks=[checkpoint, earlystop, reduce_lr],
        verbose=1
    )

    # ✅ Fine-tuning: unfreeze last layers for higher accuracy
    print("\n🔁 Fine-tuning the top layers...")
    base_model.trainable = True
    for layer in base_model.layers[:-40]:
        layer.trainable = False

    opt_fine = tf.keras.optimizers.Adam(learning_rate=1e-5)
    model.compile(optimizer=opt_fine, loss='categorical_crossentropy', metrics=['accuracy'])

    fine_tune_history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=10,
        callbacks=[checkpoint, earlystop, reduce_lr],
        verbose=1
    )

    # ✅ Save final model and metrics
    final_model_path = os.path.join(save_dir, 'final_model.h5')
    model.save(final_model_path)
    print(f"✅ Final model saved at: {final_model_path}")
    print(f"✅ Best model saved at: {checkpoint_path}")

    # Merge histories
    history.history.update(fine_tune_history.history)
    history_df = pd.DataFrame(history.history)
    metrics_csv = os.path.join(save_dir, 'training_metrics.csv')
    history_df.to_csv(metrics_csv, index=False)
    print(f"✅ Training metrics saved at: {metrics_csv}")

    # ✅ Plot accuracy
    plt.figure()
    plt.plot(history_df['accuracy'], label='Train Accuracy', color='green')
    plt.plot(history_df['val_accuracy'], label='Val Accuracy', color='red')
    plt.title('Accuracy vs Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    acc_path = os.path.join(vis_dir, 'accuracy_plot.jpg')
    plt.savefig(acc_path)
    print(f"✅ Accuracy plot saved at: {acc_path}")

    # ✅ Plot loss
    plt.figure()
    plt.plot(history_df['loss'], label='Train Loss', color='blue')
    plt.plot(history_df['val_loss'], label='Val Loss', color='orange')
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
