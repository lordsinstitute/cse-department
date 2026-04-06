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

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.ensemble import AdaBoostClassifier

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler

accuracy = []
precision = []
recall = []
fscore = []

def compAlg():
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
    #X = np.array(X, dtype=np.float)
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
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    #########################################################################################
    bm = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=20)
    bm.fit(X_train, y_train)
    predict = bm.predict(X_test)
    calculateMetrics(predict, y_test, "Bagged Model")
    train_sizes, train_scores, test_scores = learning_curve(bm, X, Y, cv=10, scoring='accuracy', n_jobs=-1,
                                                            train_sizes=np.linspace(0.01, 1.0, 50))
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, '--', color="#111111", label="0 score")
    plt.plot(train_sizes, test_mean, color="#111111", label="1 score")

    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")

    plt.title("Spam score distribution by Bagged Model")
    plt.xlabel("Score"), plt.ylabel("Density"), plt.legend(loc="best")
    plt.tight_layout()
    #plt.show()
    plt.savefig("static/pimg/bag.jpg")
    ###########################################################################################################

    br = GaussianNB()  # linear_model.BayesianRidge()
    br.fit(X_train, y_train)
    predict = br.predict(X_test)
    calculateMetrics(predict, y_test, "Bayesian Generalized Linear Model")
    train_sizes, train_scores, test_scores = learning_curve(br, X, Y, cv=10, scoring='accuracy', n_jobs=-1,
                                                            train_sizes=np.linspace(0.01, 1.0, 50))
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, '--', color="#111111", label="0 score")
    plt.plot(train_sizes, test_mean, color="#111111", label="1 score")

    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")

    plt.title("Spam score distribution by Bayesian Generalized Linear Model")
    plt.xlabel("Score"), plt.ylabel("Density"), plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("static/pimg/gnb.jpg")
    ##############################################################################################
    br = AdaBoostClassifier(n_estimators=100, random_state=0)
    br.fit(X_train, y_train)
    predict = br.predict(X_test)
    calculateMetrics(predict, y_test, "AdaBoost ")
    train_sizes, train_scores, test_scores = learning_curve(br, X, Y, cv=10, scoring='accuracy', n_jobs=-1,
                                                            train_sizes=np.linspace(0.01, 1.0, 50))
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, '--', color="#111111", label="0 score")
    plt.plot(train_sizes, test_mean, color="#111111", label="1 score")

    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")

    plt.title("Spam score distribution by Adaboost")
    plt.xlabel("Score"), plt.ylabel("Density"), plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("static/pimg/ab.jpg")

    ################################################################################################

    clf1 = LogisticRegression(multi_class='multinomial', random_state=1)
    clf2 = RandomForestClassifier(n_estimators=50, random_state=1)
    clf3 = GaussianNB()

    eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')

    br = eclf1
    br.fit(X_train, y_train)
    predict = br.predict(X_test)
    calculateMetrics(predict, y_test, "Voting Classification Model")
    train_sizes, train_scores, test_scores = learning_curve(br, X, Y, cv=10, scoring='accuracy', n_jobs=-1,
                                                            train_sizes=np.linspace(0.01, 1.0, 50))
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, '--', color="#111111", label="0 score")
    plt.plot(train_sizes, test_mean, color="#111111", label="1 score")

    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")

    plt.title("Spam score distribution by Voting Classification")
    plt.xlabel("Score"), plt.ylabel("Density"), plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("static/pimg/vc.jpg")
    ################################################################################################
    br = DecisionTreeClassifier(criterion="gini")
    br.fit(X_train, y_train)
    predict = br.predict(X_test)
    calculateMetrics(predict, y_test, "DecisionTrees ")
    train_sizes, train_scores, test_scores = learning_curve(br, X, Y, cv=10, scoring='accuracy', n_jobs=-1,
                                                            train_sizes=np.linspace(0.01, 1.0, 50))
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, '--', color="#111111", label="0 score")
    plt.plot(train_sizes, test_mean, color="#111111", label="1 score")

    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")

    plt.title("Spam score distribution by Decision Trees")
    plt.xlabel("Score"), plt.ylabel("Density"), plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("static/pimg/dt.jpg")
    ######################################################################################################
    df = pd.DataFrame([['Bagged Model', 'Precision', precision[0]], ['Bagged Model', 'Recall', recall[0]],
                       ['Bagged Model', 'F1 Score', fscore[0]], ['Bagged Model', 'Accuracy', accuracy[0]],
                       ['Bayesian GLM', 'Precision', precision[1]], ['Bayesian GLM', 'Recall', recall[1]],
                       ['Bayesian GLM', 'F1 Score', fscore[1]], ['Bayesian GLM', 'Accuracy', accuracy[1]],
                       ['Adaboost', 'Precision', precision[2]], ['Adaboost', 'Recall', recall[2]],
                       ['Adaboost', 'F1 Score', fscore[2]], ['Adaboost', 'Accuracy', accuracy[2]],
                       ['Voting Classifier', 'Precision', precision[3]], ['Voting Classifier', 'Recall', recall[3]],
                       ['Voting Classifier', 'F1 Score', fscore[3]], ['Voting Classifier', 'Accuracy', accuracy[3]],
                       ['Decision Trees', 'Precision', precision[4]], ['Decision Trees', 'Recall', recall[4]],
                       ['Decision Trees', 'F1 Score', fscore[4]], ['Decision Trees', 'Accuracy', accuracy[4]]

                       ], columns=['Parameters', 'Algorithms', 'Value'])
    #my_cmap = plt.get_cmap("Blues")
    #df.pivot("Parameters", "Algorithms", "Value").plot(kind='bar')
    #addlabels(df['Parameters'],df['Value'])
    df.pivot(index="Parameters", columns="Algorithms", values="Value").plot(kind='bar')

    plt.title("All Algorithms Comparison Graph")
    plt.savefig("static/pimg/Algcomp.jpg")

    return accuracy, precision, recall, fscore




def calculateMetrics(predict, testY, algorithm):
    p = precision_score(testY, predict,average='macro') * 100
    r = recall_score(testY, predict,average='macro') * 100
    f = f1_score(testY, predict,average='macro') * 100
    a = accuracy_score(testY,predict)*100

    accuracy.append(a)
    precision.append(p)
    recall.append(r)
    fscore.append(f)





#compAlg()

