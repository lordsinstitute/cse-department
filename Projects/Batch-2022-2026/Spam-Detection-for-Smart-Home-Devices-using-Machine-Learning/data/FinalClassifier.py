import matplotlib
matplotlib.use('Agg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from sklearn.model_selection import validation_curve
from sklearn.model_selection import learning_curve
import tensorflow as tf
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.ensemble import AdaBoostClassifier

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler


def create_model():
    dataset = pd.read_csv('Dataset.csv')
    label_encoder = []
    sc = StandardScaler()
    X = dataset.iloc[:, :-2].values
    Y = dataset.iloc[:, 12].values
    label_encoder = []
    for i in range(0, 11):
        le = LabelEncoder()
        X[:, i] = le.fit_transform(X[:, i].astype(str))
        label_encoder.append(le)
    imputer = SimpleImputer(missing_values=np.nan, strategy='constant')
    imputer = imputer.fit(X[:, [8]])
    X[:, [8]] = imputer.transform(X[:, [8]])
    imputer1 = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer1 = imputer1.fit(X[:, [10]])
    X[:, [10]] = imputer1.transform(X[:, [10]])
    X = np.array(X, dtype=np.float64)
    X = sc.fit_transform(X)
    Y_le = LabelEncoder()
    Y = Y_le.fit_transform(Y)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]

    pca = PCA(n_components=10)
    X = pca.fit_transform(X)

    df1 = pd.DataFrame(X)  # .to_csv("../X_train.csv")
    df2 = pd.DataFrame(Y)  # .to_csv("../Y_train.csv")
    preprocess = pd.concat([df1, df2], axis=1, join='inner')
    preprocess.to_csv("preprocess.csv")

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    print(X_train.shape)
    print(y_train.shape)

    print(X_train[1])
    print(y_train[1])

    print(X_train[1300])
    print(y_train[1300])

    # example of training a final classification model

    # generate 2d classification dataset
    X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
    scalar = MinMaxScaler()
    scalar.fit(X)
    X = scalar.transform(X)
    # define and fit the final model

    model = Sequential()
    model.add(Dense(4, input_shape=(10,), activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    #model.add(tf.keras.layers.Dense(256, input_shape=(X_train.shape[1],), activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history=model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, verbose=1)

    acc=model.evaluate(X_train, y_train, verbose=0)
    print(acc[1]*100)

    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('static/pimg/macc.jpg')
    plt.clf()
    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('static/pimg/mloss.jpg')

    model.save("iot_spam_model.h5")
    msg = "Model created successfully"
    print(msg)
    return acc
    """
    m=tf.keras.models.load_model("../iot_spam_model.h5")
    Xnew = np.array([[-2.28026896, -0.60104891, -0.349624, -0.175845, 0.13008477, 0.0845894, -0.02996252, -0.02723482,
                      -0.01630877, 0.00378721]])
    ynew = m.predict(Xnew)
    print("X=%s, \nPredicted=%s" % (Xnew[0],  ynew[0]))

    Xnew1 = np.array([[3.90061949,-0.54252493,-1.33244856,-0.60496529,-0.33946101,-0.28278929,-0.47406838,-0.02688136,0.00514039,-0.02944146]])
    ynew1 = m.predict(Xnew1)
    print("X=%s, \nPredicted=%s" % (Xnew1[0], ynew1[0]))
    """

#create_model()