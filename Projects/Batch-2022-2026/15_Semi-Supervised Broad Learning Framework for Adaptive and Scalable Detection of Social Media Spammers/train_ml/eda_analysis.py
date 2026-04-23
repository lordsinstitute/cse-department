import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import TRAIN_PATH, EDA_PATH

sns.set(style="darkgrid")


df = pd.read_csv(TRAIN_PATH)

print(df.info())
print(df.describe())
print(df['Type'].value_counts())


# -------------------------------
# Class Distribution
# -------------------------------

plt.figure()

sns.countplot(x='Type', data=df)

plt.title("Spam vs Quality Tweets")

plt.savefig(EDA_PATH + "class_distribution.png")

plt.close()


# -------------------------------
# Followers Distribution
# -------------------------------

plt.figure()

sns.histplot(df['followers'], bins=50)

plt.title("Followers Distribution")

plt.savefig(EDA_PATH + "followers_distribution.png")

plt.close()


# -------------------------------
# Following Distribution
# -------------------------------

plt.figure()

sns.histplot(df['following'], bins=50)

plt.title("Following Distribution")

plt.savefig(EDA_PATH + "following_distribution.png")

plt.close()


# -------------------------------
# Tweet Length Distribution
# -------------------------------

df['tweet_length'] = df['Tweet'].astype(str).apply(len)

plt.figure()

sns.histplot(df['tweet_length'], bins=40)

plt.title("Tweet Length Distribution")

plt.savefig(EDA_PATH + "tweet_length_distribution.png")

plt.close()


# -------------------------------
# Correlation Heatmap
# -------------------------------

numeric_cols = ['following', 'followers', 'actions']

plt.figure()

sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")

plt.title("Feature Correlation")

plt.savefig(EDA_PATH + "correlation_heatmap.png")

plt.close()


print("EDA graphs saved in static/eda/")