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
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.preprocessing import label_binarize
import seaborn as sns

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

    # ================= EVALUATION ================= #

    # IMPORTANT: ensure order consistency
    val_generator.reset()

    y_pred = model.predict(val_generator)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = val_generator.classes

    class_labels = list(val_generator.class_indices.keys())

    print("y_pred shape:", y_pred.shape)
    print("Classes:", class_labels)

    # ---------- CLASSIFICATION REPORT ----------
    report = classification_report(
        y_true, y_pred_classes,
        target_names=class_labels,
        output_dict=True
    )

    report_df = pd.DataFrame(report).transpose()
    report_path = os.path.join(vis_dir, 'classification_report.csv')
    report_df.to_csv(report_path)
    print("✅ Classification report saved")

    # ---------- CONFUSION MATRIX ----------
    cm = confusion_matrix(y_true, y_pred_classes)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d',
                xticklabels=class_labels,
                yticklabels=class_labels)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    cm_path = os.path.join(vis_dir, 'confusion_matrix.png')
    plt.savefig(cm_path)
    plt.close()
    print("✅ Confusion matrix saved")

    # ---------- ACCURACY CURVE ----------
    plt.figure(figsize=(6, 5))
    plt.plot(history_df['accuracy'], marker='o', label='Train Accuracy')
    plt.plot(history_df['val_accuracy'], marker='o', label='Validation Accuracy')
    plt.title("Accuracy Curve")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    plt.savefig(os.path.join(vis_dir, 'accuracy_curve.png'))
    plt.close()
    print("✅ Accuracy curve saved")

    # ---------- LOSS CURVE ----------
    plt.figure(figsize=(6, 5))
    plt.plot(history_df['loss'], marker='o', label='Train Loss')
    plt.plot(history_df['val_loss'], marker='o', label='Validation Loss')
    plt.title("Loss Curve")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.savefig(os.path.join(vis_dir, 'loss_curve.png'))
    plt.close()
    print("✅ Loss curve saved")

    # ---------- ROC + PR CURVES ----------

    num_classes = len(class_labels)

    if num_classes == 2:
        # Binary case
        fpr, tpr, _ = roc_curve(y_true, y_pred[:, 1])
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.title("ROC Curve")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.legend()

        plt.savefig(os.path.join(vis_dir, 'roc_curve.png'))
        plt.close()

        precision, recall, _ = precision_recall_curve(y_true, y_pred[:, 1])

        plt.figure()
        plt.plot(recall, precision)
        plt.title("Precision-Recall Curve")
        plt.xlabel("Recall")
        plt.ylabel("Precision")

        plt.savefig(os.path.join(vis_dir, 'pr_curve.png'))
        plt.close()

        print("✅ ROC & PR curves saved (binary)")


    elif num_classes > 2:
        y_true_bin = label_binarize(y_true, classes=range(num_classes))

        # ROC
        plt.figure()
        for i in range(num_classes):
            fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred[:, i])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f"{class_labels[i]} (AUC={roc_auc:.2f})")

        plt.plot([0, 1], [0, 1], 'k--')
        plt.title("ROC Curve")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.legend()

        plt.savefig(os.path.join(vis_dir, 'roc_curve.png'))
        plt.close()

        # PR Curve
        plt.figure()
        for i in range(num_classes):
            precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_pred[:, i])
            plt.plot(recall, precision, label=class_labels[i])

        plt.title("Precision-Recall Curve")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.legend()

        plt.savefig(os.path.join(vis_dir, 'pr_curve.png'))
        plt.close()

        print("✅ ROC & PR curves saved (multiclass)")

    else:
        print("⚠️ ROC/PR skipped")


if __name__ == "__main__":
    create_model()
