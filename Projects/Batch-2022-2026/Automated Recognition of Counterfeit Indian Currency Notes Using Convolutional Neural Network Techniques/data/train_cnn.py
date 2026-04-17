import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.preprocessing import label_binarize
from glob import glob
import os

def create_model():

    train_path = '../Indian Currency Dataset/train'
    validation_path = '../Indian Currency Dataset/test'
    save_dir = '../saved_models_cnn'
    vis_dir = '../static/cnn'

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    class_names = glob(train_path + "/*")
    num_classes = len(class_names)
    print("Number of Classes:", num_classes)

    # Data Generators
    train_datagen = ImageDataGenerator(rescale=1/255, shear_range=0.3,
                                       horizontal_flip=True, zoom_range=0.3)

    val_datagen = ImageDataGenerator(rescale=1/255)

    train_generator = train_datagen.flow_from_directory(
        train_path, target_size=(224,224), batch_size=10, class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        validation_path, target_size=(224,224), batch_size=10,
        class_mode='categorical', shuffle=False   # IMPORTANT
    )

    # Model
    model = Sequential([
        Conv2D(32,(3,3),activation='relu',input_shape=(224,224,3)),
        MaxPooling2D(2,2),

        Conv2D(64,(3,3),activation='relu'),
        MaxPooling2D(2,2),

        Conv2D(128,(3,3),activation='relu'),
        MaxPooling2D(2,2),

        Conv2D(256,(3,3),activation='relu'),
        MaxPooling2D(2,2),

        Flatten(),
        Dense(512,activation='relu'),
        Dropout(0.5),
        Dense(num_classes,activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Callbacks
    checkpoint = ModelCheckpoint(os.path.join(save_dir,'best_model.h5'),
                                 monitor='val_accuracy', save_best_only=True)

    earlystop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Train
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=20,
        callbacks=[checkpoint, earlystop]
    )

    # ---------- PREDICTIONS ----------
    val_generator.reset()
    y_pred = model.predict(val_generator)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = val_generator.classes

    class_labels = list(val_generator.class_indices.keys())

    # ---------- CLASSIFICATION REPORT ----------
    report = classification_report(y_true, y_pred_classes, target_names=class_labels, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_path = os.path.join(vis_dir, 'classification_report.csv')
    report_df.to_csv(report_path)
    print("✅ Classification report saved")

    # ---------- CONFUSION MATRIX ----------
    cm = confusion_matrix(y_true, y_pred_classes)

    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_labels, yticklabels=class_labels)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    cm_path = os.path.join(vis_dir, 'confusion_matrix.png')
    plt.savefig(cm_path)
    plt.close()
    print("✅ Confusion matrix saved")

    # ---------- ACCURACY CURVE ----------
    plt.figure(figsize=(6, 5))

    plt.plot(history.history['accuracy'], marker='o', label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], marker='o', label='Validation Accuracy')

    plt.title('Model Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)

    acc_path = os.path.join(vis_dir, 'accuracy_curve.png')
    plt.savefig(acc_path)
    plt.close()

    print("✅ Accuracy curve saved")

    # ---------- LOSS CURVE ----------
    plt.figure(figsize=(6, 5))

    plt.plot(history.history['loss'], marker='o', label='Train Loss')
    plt.plot(history.history['val_loss'], marker='o', label='Validation Loss')

    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    loss_path = os.path.join(vis_dir, 'loss_curve.png')
    plt.savefig(loss_path)
    plt.close()

    print("✅ Loss curve saved")

    # ---------- ROC CURVE ----------
    print("y_pred shape:", y_pred.shape)
    print("num_classes:", num_classes)
    print("class labels:", class_labels)
    """
    y_true_bin = label_binarize(y_true, classes=range(num_classes))

    plt.figure()

    for i in range(num_classes):
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{class_labels[i]} (AUC={roc_auc:.2f})")

    plt.plot([0,1],[0,1],'k--')
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()

    roc_path = os.path.join(vis_dir, 'roc_curve.png')
    plt.savefig(roc_path)
    plt.close()
    print("✅ ROC curve saved")

    # ---------- PRECISION-RECALL CURVE ----------
    plt.figure()

    for i in range(num_classes):
        precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_pred[:, i])
        plt.plot(recall, precision, label=class_labels[i])

    plt.title("Precision-Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend()

    pr_path = os.path.join(vis_dir, 'pr_curve.png')
    plt.savefig(pr_path)
    plt.close()
    print("✅ PR curve saved")

    return model
    """
    # ---------- ROC + PR (FIXED) ----------

    if num_classes == 2:
        # Use only positive class (class 1)
        fpr, tpr, _ = roc_curve(y_true, y_pred[:, 1])
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.title("ROC Curve (Binary)")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.legend()
        plt.savefig(os.path.join(vis_dir, 'roc_curve.png'))
        plt.close()

        # PR Curve
        precision, recall, _ = precision_recall_curve(y_true, y_pred[:, 1])

        plt.figure()
        plt.plot(recall, precision)
        plt.title("Precision-Recall Curve (Binary)")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.savefig(os.path.join(vis_dir, 'pr_curve.png'))
        plt.close()

        print("✅ ROC & PR (binary) saved")


    elif num_classes > 2:
        y_true_bin = label_binarize(y_true, classes=range(num_classes))

        plt.figure()
        for i in range(num_classes):
            fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred[:, i])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f"{class_labels[i]} (AUC={roc_auc:.2f})")

        plt.plot([0, 1], [0, 1], 'k--')
        plt.title("ROC Curve (Multiclass)")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.legend()
        plt.savefig(os.path.join(vis_dir, 'roc_curve.png'))
        plt.close()

        plt.figure()
        for i in range(num_classes):
            precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_pred[:, i])
            plt.plot(recall, precision, label=class_labels[i])

        plt.title("Precision-Recall Curve (Multiclass)")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.legend()
        plt.savefig(os.path.join(vis_dir, 'pr_curve.png'))
        plt.close()

        print("✅ ROC & PR (multiclass) saved")

    else:
        print("⚠️ ROC/PR skipped: insufficient classes")


if __name__ == "__main__":
    create_model()