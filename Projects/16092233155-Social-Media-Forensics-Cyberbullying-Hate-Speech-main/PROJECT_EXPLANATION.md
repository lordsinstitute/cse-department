# Social Media Hate Speech Analysis — Project Explanation

This document explains the Social Media Hate Speech Analysis project in simple language that anyone can understand.

## What is This Project?

This is a website that can read a piece of text — like a tweet, a comment, or a social media post — and figure out if it contains hate speech, offensive language, or if it's perfectly fine (clean).

Think of it like a teacher reading students' messages and deciding: "This one is fine," "This one is rude," or "This one is really harmful and targets a group of people."

## Why Was This Project Built?

Social media is used by billions of people every day. Unfortunately, some people use it to spread hate and bully others. Manually reading every single post to find the bad ones is impossible — there are too many.

This project shows how computers can help:
- **Social media companies** can automatically flag harmful content
- **Online communities** can keep their spaces safer
- **Researchers** can study the spread of hate speech
- **Schools** can detect cyberbullying

## The Three Categories

### 1. Hate Speech (Red)
This is the most serious category. Hate speech targets people based on things they can't change or shouldn't be discriminated for:
- Race or ethnicity
- Religion
- Gender
- Nationality
- Disability

Example: "All [group] should be banned from our country" — This targets an entire group of people unfairly.

### 2. Offensive (Orange)
This is rude, mean, or profane language, but it doesn't target a specific protected group. It's still not nice, but it's different from hate speech.

Example: "You're such an idiot, shut up" — This is mean and rude, but it's directed at a person's behavior, not their identity.

### 3. Clean (Green)
Normal, everyday social media content. Happy posts, opinions, news sharing, jokes — anything that's not harmful.

Example: "Just had an amazing dinner with my family!" — This is perfectly fine.

## How Does It Work?

### Step 1: The Data

The project uses a dataset of 15,000 social media-style posts:
- About 8,250 (55%) are clean
- About 3,750 (25%) are offensive
- About 3,000 (20%) are hate speech

This mix reflects reality — most social media content is fine, some is rude, and a smaller amount is truly hateful.

### Step 2: Cleaning the Text (Preprocessing)

Before the computer can analyze text, it needs to clean it up:

1. **Make everything lowercase** — "HELLO" becomes "hello" (so the computer treats them the same)
2. **Remove URLs** — Links like "http://example.com" are removed (they don't help with classification)
3. **Remove @mentions** — "@username" is removed
4. **Remove #hashtags** — "#trending" is removed
5. **Remove special characters** — Emojis, punctuation, and numbers are removed
6. **Remove common words** — Words like "the", "is", "at", "and" are removed because they appear in all types of text and don't help distinguish categories

### Step 3: Converting Text to Numbers (TF-IDF)

Computers don't understand words — they understand numbers. So we need to convert text into numbers.

**TF-IDF** stands for "Term Frequency — Inverse Document Frequency." Here's what it means:

- **Term Frequency (TF):** How often a word appears in a specific text. If "hate" appears 3 times in a post, its TF is high for that post.
- **Inverse Document Frequency (IDF):** How rare a word is across ALL texts. The word "the" appears everywhere (low IDF), but "disgusting" is less common (high IDF).
- **TF-IDF = TF × IDF:** Words that are frequent in a specific text but rare overall get the highest scores. These are the most useful words for classification.

We also use **bigrams** — pairs of words like "hate speech" or "shut up" — because sometimes two words together carry more meaning than individually.

The result: each text becomes a row of 5,000 numbers (one for each important word or word pair).

### Step 4: Training the Model

The computer learns from 12,000 examples (80% of the data). Here's how:

1. **Show it labeled examples** — The computer sees the TF-IDF numbers AND the correct label (Hate Speech, Offensive, or Clean)
2. **Find patterns** — It learns rules like:
   - Texts with words like "immigrants," "deported," "inferior" together → likely Hate Speech
   - Texts with words like "stupid," "idiot," "shut up" → likely Offensive
   - Texts with words like "love," "amazing," "family" → likely Clean
3. **Test itself** — It predicts labels for the 3,000 examples it hasn't seen and checks how many it got right

### Step 5: Choosing the Best Model

We train 6 different types of models and compare them:

| Model | How It Works (Simple Explanation) | Accuracy |
|-------|----------------------------------|----------|
| Logistic Regression | Draws mathematical lines to separate the three categories | 94.83% |
| Naive Bayes | Uses probability — "what are the chances this word appears in hate speech?" | 94.83% |
| SVM | Finds the best boundary between categories with maximum gap | 94.83% |
| KNN | Looks at the 5 most similar texts and picks the most common label | 94.73% |
| Gradient Boosting | Builds many small models, each fixing the previous one's mistakes | 94.50% |
| Random Forest | Uses 100 decision trees and takes a vote | 94.17% |

**Logistic Regression wins** with 94.83% accuracy — it correctly classifies about 95 out of every 100 texts.

## What Do the Accuracy Metrics Mean?

- **Accuracy (94.83%)** — Out of 100 texts, the model correctly classifies about 95 of them
- **Precision (94.87%)** — When the model says "this is hate speech," it's right about 95% of the time
- **Recall (94.83%)** — Out of all actual hate speech texts, the model catches about 95% of them
- **F1 Score (94.81%)** — A balance between precision and recall (you want both to be high)

## What is Logistic Regression?

Despite the name, Logistic Regression is used for **classification** (sorting things into categories), not regression.

Imagine sorting mail into three boxes: "Important," "Spam," and "Regular." Logistic Regression learns a formula that looks at certain features of each letter (who sent it, what words are in it, etc.) and calculates a probability for each box. The letter goes in the box with the highest probability.

For our project:
- It looks at the TF-IDF scores (which words are present and how important they are)
- It calculates three probabilities: P(Hate Speech), P(Offensive), P(Clean)
- It picks the category with the highest probability
- That probability becomes the "confidence" score you see on the website

## How Does the Website Work?

### The Server (Flask)

Flask is a Python web framework — it receives requests from your browser and sends back web pages. When you visit a URL like `/predict`:
1. Flask checks if you're logged in
2. If it's a GET request, it shows the text analysis form
3. If it's a POST request (you submitted the form), it runs the model and shows results

### The Database (SQLite)

SQLite is a lightweight database stored in a single file (`hate_speech.db`). It has two tables:
- **users** — stores everyone's login information (passwords are encrypted)
- **predictions** — stores every analysis made, linked to the user who made it

### Authentication

When you register:
1. Your password is hashed (scrambled) using PBKDF2-SHA256 — even if someone sees the database, they can't read your password
2. Your account is saved

When you log in:
1. The system hashes the password you typed
2. It compares it with the stored hash
3. If they match, you get a session cookie (like a digital wristband at a water park)
4. This cookie tells the server "this person is logged in" for every page they visit

### The Visualizations

Eight charts are generated when the model is trained:
1. **Class Distribution** — bar chart showing how many texts are in each category
2. **Text Length Distribution** — how long texts are in each category
3. **Word Count Distribution** — how many words texts have in each category
4. **Word Cloud (Hate Speech)** — most common words in hate speech texts
5. **Word Cloud (Clean)** — most common words in clean texts
6. **Top TF-IDF Features** — most important words for each category
7. **Model Comparison** — accuracy and F1 scores of all 6 models
8. **Confusion Matrix** — shows where the best model gets confused between categories

## What is a Confusion Matrix?

A confusion matrix is a table that shows how often the model confuses one category for another:

```
                  Predicted
                  Hate  Off.  Clean
Actual Hate    [  580    30    25  ]
Actual Off.    [   25   715    29  ]
Actual Clean   [   20    25  1551  ]
```

- The diagonal (580, 715, 1551) shows correct predictions
- Off-diagonal numbers show mistakes
- For example, 30 Hate Speech texts were incorrectly classified as Offensive

## Key Findings

1. **Word choice is the strongest signal** — hate speech uses dehumanizing words targeting groups, while offensive language uses general insults
2. **Context matters** — the same word can be hate speech in one context and offensive in another
3. **Clean text is easiest to detect** — it has very different vocabulary from harmful content
4. **Linear models work well** — Logistic Regression and SVM perform as well as more complex models, suggesting clear patterns in the vocabulary

## Important Note

This is a student project for educational purposes. The model is trained on synthetic data and may not perform perfectly on real-world social media content. For production use:
- Train on larger, real-world datasets
- Consider cultural context and sarcasm
- Have human moderators review flagged content
- Regularly update the model as language evolves

## Summary

This project demonstrates:
1. **Natural Language Processing** — cleaning and preprocessing text data
2. **Feature Engineering** — converting text to numerical features using TF-IDF
3. **Machine Learning** — training and comparing 6 classification models
4. **Web Development** — building a Flask application with authentication
5. **Data Visualization** — creating informative EDA charts
6. **Model Deployment** — serving predictions via a web interface
7. **Database Management** — storing users and analysis history in SQLite

It shows how AI and machine learning can be applied to make social media platforms safer by automatically detecting harmful content.
