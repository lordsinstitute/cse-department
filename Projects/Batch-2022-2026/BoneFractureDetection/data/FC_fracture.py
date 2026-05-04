import numpy as np
import pandas as pd
import os.path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
import itertools

# load images to build and train the model
#                       ....                                     /    img1.jpg
#             test      Hand            patient0000   positive  --   img2.png
#           /                /                         \    .....
#   Dataset   -         Elbow  ------   patient0001
#           \ train               \         /                           img1.png
#                       Shoulder        patient0002     negative --      img2.jpg
#                       ....                   \
#

def load_path(path, part):
    """
    load X-ray dataset
    """
    dataset = []
    for folder in os.listdir(path):
        folder = path + '/' + str(folder)
        if os.path.isdir(folder):
            for body in os.listdir(folder):
                if body == part:
                    body_part = body
                    path_p = folder + '/' + str(body)
                    for id_p in os.listdir(path_p):
                        patient_id = id_p
                        path_id = path_p + '/' + str(id_p)
                        for lab in os.listdir(path_id):
                            if lab.split('_')[-1] == 'positive':
                                label = 'fractured'
                            elif lab.split('_')[-1] == 'negative':
                                label = 'normal'
                            path_l = path_id + '/' + str(lab)
                            for img in os.listdir(path_l):
                                img_path = path_l + '/' + str(img)
                                dataset.append(
                                    {
                                        'body_part': body_part,
                                        'patient_id': patient_id,
                                        'label': label,
                                        'image_path': img_path
                                    }
                                )
    return dataset


# this function get part and know what kind of part to train, save model and save plots
def trainPart(part):
    # categories = ['fractured', 'normal']
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    image_dir = '../Dataset/'
    data = load_path(image_dir, part)
    labels = []
    filepaths = []

    # add labels for dataframe for each category 0-fractured, 1- normal
    for row in data:
        labels.append(row['label'])
        filepaths.append(row['image_path'])

    filepaths = pd.Series(filepaths, name='Filepath').astype(str)
    labels = pd.Series(labels, name='Label')

    images = pd.concat([filepaths, labels], axis=1)

    # split all dataset 10% test, 90% train (after that the 90% train will split to 20% validation and 80% train
    train_df, test_df = train_test_split(images, train_size=0.9, shuffle=True, random_state=1)

    # each generator to process and convert the filepaths into image arrays,
    # and the labels into one-hot encoded labels.
    # The resulting generators can then be used to train and evaluate a deep learning model.

    # now we have 10% test, 72% training and 18% validation
    train_generator = tf.keras.preprocessing.image.ImageDataGenerator(horizontal_flip=True,
                                                                      preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
                                                                      validation_split=0.2)

    # use ResNet50 architecture
    test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=tf.keras.applications.resnet50.preprocess_input)

    train_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col='Filepath',
        y_col='Label',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=64,
        shuffle=True,
        seed=42,
        subset='training'
    )

    val_images = train_generator.flow_from_dataframe(
        dataframe=train_df,
        x_col='Filepath',
        y_col='Label',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=64,
        shuffle=True,
        seed=42,
        subset='validation'
    )

    test_images = test_generator.flow_from_dataframe(
        dataframe=test_df,
        x_col='Filepath',
        y_col='Label',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=32,
        shuffle=False
    )

    # we use rgb 3 channels and 224x224 pixels images, use feature extracting , and average pooling
    pretrained_model = tf.keras.applications.resnet50.ResNet50(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet',
        pooling='avg')

    # for faster performance
    pretrained_model.trainable = False

    inputs = pretrained_model.input
    x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
    x = tf.keras.layers.Dense(50, activation='relu')(x)

    # outputs Dense '2' because of 2 classes, fratured and normal
    outputs = tf.keras.layers.Dense(2, activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    # print(model.summary())
    print("-------Training " + part + "-------")

    # Adam optimizer with low learning rate for better accuracy
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    # early stop when our model is over fit or vanishing gradient, with restore best values
    callbacks = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    history = model.fit(train_images, validation_data=val_images, epochs=25, callbacks=[callbacks])

    # save model to this path
    model.save("../model/weights/ResNet50_" + part + "_frac.h5")
    results = model.evaluate(test_images, verbose=0)
    print(part + " Results:")
    print(results)
    print(f"Test Accuracy: {np.round(results[1] * 100, 2)}%")

    # -------------------- Predictions --------------------
    y_true = test_images.classes
    y_pred_probs = model.predict(test_images)

    # Since binary classification → take probability of class 1
    y_pred = np.argmax(y_pred_probs, axis=1)

    class_names = list(test_images.class_indices.keys())

    # Create folder for this part
    save_dir = os.path.join("../static/plots/FractureDetection/", part)
    os.makedirs(save_dir, exist_ok=True)

    report = classification_report(y_true, y_pred, target_names=class_names)

    with open(os.path.join(save_dir, "classification_report.txt"), "w") as f:
        f.write(report)

    print("\nClassification Report:\n", report)

    cm = confusion_matrix(y_true, y_pred)

    plt.figure()
    plt.imshow(cm)
    plt.title(part + " Confusion Matrix")
    plt.colorbar()

    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment="center")

    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "confusion_matrix.jpeg"))
    plt.clf()

    # Probability for positive class (fractured)
    y_scores = y_pred_probs[:, 1]

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(part + " ROC Curve")
    plt.legend()

    plt.savefig(os.path.join(save_dir, "roc_curve.jpeg"))
    plt.clf()

    precision, recall, _ = precision_recall_curve(y_true, y_scores)

    plt.figure()
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(part + " Precision-Recall Curve")

    plt.savefig(os.path.join(save_dir, "pr_curve.jpeg"))
    plt.clf()


    # create plots for accuracy and save it
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    figAcc = plt.gcf()
    my_file = os.path.join("../plots/FractureDetection/" + part + "/_Accuracy.jpeg")
    figAcc.savefig(my_file)
    plt.clf()

    # create plots for loss and save it
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    figAcc = plt.gcf()
    my_file = os.path.join("../plots/FractureDetection/" + part + "/_Loss.jpeg")
    figAcc.savefig(my_file)

# run the function and create model for each parts in the array
categories_parts = ["Elbow", "Hand", "Shoulder"]
for category in categories_parts:
    trainPart(category)