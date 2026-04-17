import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def clean_tweet(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)


def preprocess_dataframe(df):

    df = df.copy()

    # -------- Handle missing text --------
    df['Tweet'] = df['Tweet'].fillna("")

    # -------- Clean tweets --------
    df['clean_tweet'] = df['Tweet'].apply(clean_tweet)

    # -------- Numeric missing values --------
    numeric_cols = ['followers', 'following', 'actions']

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())

    # -------- Feature engineering --------
    df['tweet_length'] = df['Tweet'].astype(str).apply(len)

    df['follower_following_ratio'] = df['followers'] / (df['following'] + 1)

    # Final safety check
    df = df.fillna(0)

    return df


def vectorize_text(train_text):

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1,2)
    )

    X = vectorizer.fit_transform(train_text)

    return X, vectorizer