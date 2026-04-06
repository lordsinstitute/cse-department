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

def test_model(param):
    """
    data=[['lightcontrol2','/agent2/lightcontrol2','/lightControler','BedroomParents','/agent2/lightcontrol2','/lightControler','BedroomParents','/agent2/lightcontrol2','/lightControler','registerService']]
    df = pd.DataFrame(data, columns=['sourceID','sourceAddress','sourceType','sourceLocation','destinationServiceAddress','destinationServiceType','destinationLocation','accessedNodeAddress','accessedNodeType','operation'])
    sc = StandardScaler()
    X = df.iloc[0].values


    dataset = pd.read_csv('../Dataset.csv')
    label_encoder = []
    sc = StandardScaler()
    X = dataset.iloc[:, :-2].values
    Y = dataset.iloc[:, 12].values
    label_encoder = []
    for i in range(0, 11):
        le = LabelEncoder()
        X[:, i] = le.fit_transform(X[:, i].astype(str))
        label_encoder.append(le)
    pd.DataFrame(X).to_csv("../X_le.csv")
    imputer = SimpleImputer(missing_values=np.nan, strategy='constant', verbose=0)
    imputer = imputer.fit(X[:, [8]])
    X[:, [8]] = imputer.transform(X[:, [8]])
    imputer1 = SimpleImputer(missing_values=np.nan, strategy='mean', verbose=0)
    imputer1 = imputer1.fit(X[:, [10]])
    X[:, [10]] = imputer1.transform(X[:, [10]])
    X = np.array(X, dtype=np.float64)
    pd.DataFrame(X).to_csv("../X_imp.csv")
    X = sc.fit_transform(X)
    pd.DataFrame(X).to_csv("../X_sc.csv")
    Y_le = LabelEncoder()
    Y = Y_le.fit_transform(Y)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]

    pca = PCA(n_components=10)
    X = pca.fit_transform(X)
    df1=pd.DataFrame(X)#.to_csv("../X_train.csv")
    df2=pd.DataFrame(Y)#.to_csv("../Y_train.csv")
    preprocess = pd.concat([df1, df2], axis=1, join='inner')
    preprocess.to_csv("../preprocess.csv")
    """
    m = tf.keras.models.load_model("iot_spam_model.h5")
    Xnew = np.array([param])
    ynew = m.predict(Xnew)
    print("X=%s, \nPredicted=%s" % (Xnew[0], ynew[0]))
    pred=round(ynew[0][0])
    return pred
    """
    Xnew1 = np.array([[3.90061949, -0.54252493, -1.33244856, -0.60496529, -0.33946101, -0.28278929, -0.47406838,
                       -0.02688136, 0.00514039, -0.02944146]])
    ynew1 = m.predict(Xnew1)
    print("X=%s, \nPredicted=%s" % (Xnew1[0], ynew1[0]))
    """

"""
p1=[-2.28026896, -0.60104891, -0.349624, -0.175845, 0.13008477, 0.0845894, -0.02996252, -0.02723482,-0.01630877, 0.00378721]
pred1=test_model(p1)
print(pred1)
print("*********")
p2=[-3.90061949, -0.54252493, -1.33244856, -0.60496529, -0.33946101, -0.28278929, -0.47406838,-0.02688136, 0.00514039, -0.02944146]
pred2=test_model(p2)
print(pred2)
"""