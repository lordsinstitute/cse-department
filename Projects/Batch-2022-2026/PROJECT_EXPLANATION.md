# C12 -- Detecting Malicious URLs Using Machine Learning

## A Complete, Beginner-Friendly Explanation of the Entire Project

> **Reading Level:** This document is written so that a 7th grader can understand it.
> Every technical concept is explained with a real-world analogy first, then the
> technical details follow.

---

## Table of Contents

1.  [What Does This Project Do?](#1-what-does-this-project-do)
2.  [What Are Malicious URLs and Phishing?](#2-what-are-malicious-urls-and-phishing)
3.  [Technologies Used](#3-technologies-used)
4.  [Project File Structure](#4-project-file-structure)
5.  [Dataset Generation](#5-dataset-generation)
6.  [Feature Extraction -- Turning a URL into 28 Numbers](#6-feature-extraction----turning-a-url-into-28-numbers)
7.  [The 8 Machine Learning Models Explained](#7-the-8-machine-learning-models-explained)
8.  [Model Comparison and Why Gradient Boosting Won](#8-model-comparison-and-why-gradient-boosting-won)
9.  [Flask Web Application Architecture](#9-flask-web-application-architecture)
10. [Database Design](#10-database-design)
11. [How Prediction Works Step by Step](#11-how-prediction-works-step-by-step)
12. [EDA Visualizations Explained](#12-eda-visualizations-explained)
13. [Security Features](#13-security-features)
14. [Viva Questions and Answers (20 Q&A)](#14-viva-questions-and-answers)

---

## 1. What Does This Project Do?

### Real-World Analogy -- The Security Guard

Imagine you are going to a big concert. At the entrance, there is a security guard.
Every person who wants to enter shows their ticket. The guard looks at the ticket and
checks many things:

- Is the ticket the right size?
- Does it have the official logo?
- Is the barcode real or does it look photocopied?
- Is the date correct?
- Does the name match the person's ID?

Based on all these checks, the guard decides: **"You can go in"** (Legitimate) or
**"Sorry, this ticket is fake"** (Malicious).

### What Our Project Does (Exactly Like the Security Guard)

Our project is a **digital security guard for website links (URLs)**. When you browse
the internet, you click on links every day. Some links take you to real websites like
Google or Amazon. But some links are **traps** -- they take you to fake websites that
try to steal your password, credit card number, or personal information.

Our app works like this:

```
+-------------------+        +---------------------+        +------------------+
|                   |        |                     |        |                  |
|   User enters a   | -----> |   App examines 28   | -----> |   Result:        |
|   URL (website    |        |   different things  |        |   LEGITIMATE     |
|   link) into the  |        |   about the URL     |        |   or MALICIOUS   |
|   web app         |        |   (like a security  |        |   + confidence % |
|                   |        |   guard checking     |        |                  |
|                   |        |   a ticket)          |        |                  |
+-------------------+        +---------------------+        +------------------+
```

**In short:** You give the app a URL. It looks at 28 clues in that URL. A trained
machine learning model then predicts whether the URL is safe (Legitimate) or dangerous
(Malicious), along with a confidence percentage showing how sure it is.

---

## 2. What Are Malicious URLs and Phishing?

### The Analogy -- The Wolf in Sheep's Clothing

You know the story of the wolf who dressed up as a sheep to sneak into the flock?
Malicious URLs work the same way. They **look** like real websites but they are
actually traps.

### What Is a URL?

A URL (Uniform Resource Locator) is simply a **website address**. When you type
`https://www.google.com` in your browser, that entire text is a URL. It is like a
home address, but for a website.

```
Let us break down a URL:

    https://www.google.com/search?q=cats
    |_____|  |_| |________| |____| |____|
      |       |       |        |      |
  Protocol  Sub-   Domain    Path  Query
  (lock on  domain (house   (room  (what you
   the door)       name)    inside) asked for)
```

### What Makes a URL "Malicious"?

A malicious URL is a link that tries to trick you. Here are real examples of tricks
bad guys use:

| Trick | Example | Why It Is Dangerous |
|-------|---------|---------------------|
| Misspelled domain | `g00gle.com` (zeros instead of o's) | Looks like Google but is not |
| IP address instead of name | `http://192.168.1.55/login` | Real companies use names, not numbers |
| Suspicious words | `http://verify-your-account-now.tk` | Tries to scare you into clicking |
| Lots of subdomains | `login.secure.bank.verify.evil.com` | Hides the real domain deep inside |
| URL shorteners | `bit.ly/x8kd92` | Hides where you are really going |
| Suspicious TLD | `free-gift.xyz` | Cheap domain extensions used by scammers |
| @ symbol | `http://google.com@evil.com/steal` | The browser ignores everything before @ |

### What Is Phishing?

Phishing (pronounced "fishing") is when a bad person creates a **fake website** that
looks exactly like a real one (like your bank's website) and sends you a link to it.
When you type your password on the fake site, they **steal it**.

It is called "phishing" because the attacker is "fishing" for your information, using
a fake link as "bait" -- just like a fisherman uses a worm on a hook to catch fish.

---

## 3. Technologies Used

Each technology in this project has a specific job to do. Think of building a house:
you need bricks, cement, pipes, wires, paint, and a blueprint. Each technology is
like one of those building materials.

### 3.1 Python 3 -- The Main Language

**Analogy:** Python is like **English** -- it is the language we use to write all the
instructions for the computer. Just like you write essays in English, we write our
program in Python.

**Why Python?** Python is the most popular language for machine learning because it
is easy to read (it looks almost like English) and has thousands of ready-made tools
(libraries) for data science.

### 3.2 Flask -- The Web Framework (Port 5004)

**Analogy:** Flask is like a **waiter in a restaurant**. When a customer (your browser)
asks for a menu (a web page), the waiter (Flask) goes to the kitchen (Python code),
gets the food (data), puts it on a nice plate (HTML template), and brings it to you.

Flask runs on **port 5004**. Think of a port like an **apartment number** in a building.
The building is your computer, and port 5004 is the specific apartment where this app
lives. You visit it at `http://localhost:5004`.

### 3.3 scikit-learn -- The Machine Learning Toolkit

**Analogy:** scikit-learn is like a **toolbox full of ready-made brain templates**. Instead
of building a brain from scratch, you pick a template (like "Decision Tree" or "Random
Forest"), feed it data, and it learns patterns on its own.

In our project, we use scikit-learn to train 8 different ML models and pick the best one.

### 3.4 pandas -- Data Handling

**Analogy:** pandas is like **Microsoft Excel inside Python**. It lets us organize data
into rows and columns (called a DataFrame), sort it, filter it, and analyze it.

We use pandas to load our CSV dataset of 10,000 URLs and work with the data.

### 3.5 numpy -- Number Crunching

**Analogy:** numpy is like a **super-fast calculator** that can do millions of math
operations in a blink. When we need to process arrays of 28 numbers for each URL,
numpy does the heavy lifting.

### 3.6 matplotlib and seaborn -- Drawing Charts

**Analogy:** matplotlib is like a **set of colored pencils and graph paper**, and seaborn
is like a **stencil set** that makes the drawings prettier. Together, they let us create
charts and graphs to visualize our data.

We generate 12 different charts showing patterns in our URL dataset.

### 3.7 SQLite -- The Database

**Analogy:** SQLite is like a **filing cabinet** inside the app. It stores user accounts
(who registered, their passwords) and prediction history (which URLs were checked and
what the results were).

Unlike big databases like MySQL that need a separate server, SQLite stores everything
in one small file (`url_detect.db`) -- like carrying a mini filing cabinet in your
backpack.

### 3.8 Bootstrap 5 (Dark Theme) -- Making It Look Good

**Analogy:** Bootstrap is like **pre-made furniture from IKEA**. Instead of building
every button, card, and layout from scratch with raw CSS, Bootstrap gives you
beautiful, ready-made components. We use the **dark theme** so the app looks modern
and is easy on the eyes.

### 3.9 Chart.js -- Interactive Charts in the Browser

**Analogy:** While matplotlib draws charts as pictures (PNG images), Chart.js draws
charts **inside the web page** that you can hover over and interact with. It is like
the difference between a printed photo and a video -- one is static, the other moves.

### Technology Summary Table

| Technology | Role | Analogy |
|------------|------|---------|
| Python 3 | Programming language | The language we speak |
| Flask | Web framework (port 5004) | Restaurant waiter |
| scikit-learn | ML model training | Toolbox of brain templates |
| pandas | Data manipulation | Excel inside Python |
| numpy | Numerical computing | Super-fast calculator |
| matplotlib | Static chart generation | Colored pencils and graph paper |
| seaborn | Beautiful statistical plots | Stencil set for prettier charts |
| SQLite | Database storage | Filing cabinet in a backpack |
| Bootstrap 5 | Frontend UI framework | IKEA furniture for websites |
| Chart.js | Interactive browser charts | Moving, hoverable charts |

---

## 4. Project File Structure

```
C12/code/
|
|-- generate_dataset.py      <-- Step 1: Creates 10,000 fake URLs with features
|-- malicious_urls.csv        <-- The generated dataset (10,000 rows x 31 columns)
|-- train_model.py            <-- Step 2: Trains 8 ML models, picks the best
|-- url_model.pkl             <-- The saved best model (Gradient Boosting)
|-- models_info.json          <-- Accuracy/metrics for all 8 models
|-- app.py                    <-- Step 3: The Flask web application
|-- url_detect.db             <-- SQLite database (users + predictions)
|-- Dockerfile                <-- Instructions to run the app in a container
|
|-- static/
|   |-- vis/                  <-- 12 EDA visualization images (PNG)
|       |-- label_dist.png
|       |-- url_length.png
|       |-- https_dist.png
|       |-- ip_dist.png
|       |-- suspicious_words.png
|       |-- domain_length.png
|       |-- subdomains.png
|       |-- special_ratio.png
|       |-- url_depth.png
|       |-- correlation.png
|       |-- feature_importance.png
|       |-- confusion_matrix.png
|
|-- templates/                <-- HTML pages (rendered by Flask)
    |-- base.html             <-- Master layout (navbar, footer, dark theme)
    |-- login.html            <-- User login page
    |-- register.html         <-- User registration page
    |-- home.html             <-- Dashboard with stats and recent scans
    |-- predict.html          <-- Enter URL and get prediction
    |-- history.html          <-- Past scan results
    |-- visualize.html        <-- EDA charts gallery
    |-- dashboard.html        <-- Model comparison (accuracy, F1, etc.)
    |-- about.html            <-- Project info, features, tech stack
```

### How the Files Work Together

```
Step 1: generate_dataset.py  ---creates--->  malicious_urls.csv
                                                    |
Step 2: train_model.py  --------reads-------->------+
              |                                     |
              |---saves--->  url_model.pkl  (best ML model)
              |---saves--->  models_info.json  (all metrics)
              |---saves--->  static/vis/*.png  (12 charts)
                                                    |
Step 3: app.py  --------loads-------->  url_model.pkl
              |                         models_info.json
              |---reads/writes--->  url_detect.db  (database)
              |---serves--->  templates/*.html  (web pages)
              |---serves--->  static/vis/*.png  (chart images)
```

**You run the files in order:** First `generate_dataset.py`, then `train_model.py`,
then `app.py`. Each step builds on the previous one.

---

## 5. Dataset Generation

### The Analogy -- Making Practice Exams

Imagine a teacher wants to train students to spot counterfeit (fake) money. The
teacher cannot use real counterfeit bills (that is illegal!), so instead, the teacher
**makes practice examples** -- some real bills and some fake ones with obvious and
subtle differences. Students study these examples and learn to spot the fakes.

Our `generate_dataset.py` does the same thing. It **creates 10,000 practice URLs** --
5,000 that look like real websites and 5,000 that look like dangerous ones.

### How Legitimate URLs Are Generated

The script has a list of **50 real domain names** like:

```
google.com, amazon.com, facebook.com, twitter.com, github.com,
youtube.com, wikipedia.org, reddit.com, netflix.com, paypal.com ...
```

It combines them with:
- **Protocols:** `https://` (90% of the time) or `http://` (10%)
- **Subdomains:** `www`, `mail`, `docs`, `blog`, `shop`, or none
- **Paths:** `/about`, `/contact`, `/products`, `/blog`, `/help`, etc.
- **Query parameters** (20% chance): `?q=cats`, `?page=1`, `?lang=en`

Example legitimate URLs generated:
```
https://www.google.com/search?q=python
https://github.com/docs
https://mail.yahoo.com
https://amazon.com/products
```

### How Malicious URLs Are Generated

The script uses **8 attack strategies**, each mimicking a real-world trick:

| Strategy | What It Does | Example |
|----------|-------------|---------|
| `ip` | Uses an IP address instead of a domain name | `http://192.168.45.12/login/verify` |
| `long_subdomain` | Chains many subdomains to hide the real domain | `http://login.secure.verify.xk39d.tk/abc123` |
| `suspicious` | Uses known phishing domain patterns | `http://paypal-verify.info/account/update` |
| `misspell` | Misspells famous brand names | `http://g00gle.com/signin` |
| `shortened` | Uses URL shortener services | `https://bit.ly/xk8d92` |
| `encoded` | Uses percent-encoded hex characters | `http://abc123.xyz/%2f%3a%4b/login` |
| `deep_path` | Creates extremely deep directory paths | `http://evil.top/a/b/c/d/e/f/login` |
| `mixed` | Combines multiple suspicious signals | `http://admin@verify-secure.tk/abc?redirect=http://1.2.3.4` |

### Adding Noise (Making It Realistic)

Here is a clever trick: the script **intentionally flips the labels of 8% of the
URLs** (800 out of 10,000). This means some legitimate URLs get labeled as malicious
and vice versa.

**Why?** In real life, no detector is perfect. Some safe-looking URLs are actually
dangerous, and some weird-looking URLs are actually safe. This noise forces the ML
models to work harder and produces realistic accuracy scores (around 90% instead of
an unrealistic 99%).

### The Final Dataset

The output file `malicious_urls.csv` contains:

| Column | Description |
|--------|-------------|
| ID | Row number (1 to 10,000) |
| url | The actual URL string |
| 28 feature columns | Numerical values extracted from the URL |
| label | 0 = Legitimate, 1 = Malicious |

The dataset is **shuffled randomly** so that legitimate and malicious URLs are mixed
together, not grouped.

---

## 6. Feature Extraction -- Turning a URL into 28 Numbers

### The Analogy -- Describing a Person with Numbers

Imagine you need to describe a person to someone who has never seen them, but you can
ONLY use numbers. You might say:

- Height: 170 cm
- Weight: 65 kg
- Age: 25
- Number of tattoos: 0
- Wears glasses: 1 (yes)

You just turned a complex person into a list of numbers! Machine learning models
can only understand numbers, so we need to turn each URL into a list of numbers too.

### The `extract_features()` Function

This function takes a URL string like `https://www.google.com/search?q=python` and
produces **28 numbers**. Here is every single feature explained:

### Character Count Features (13 features)

These count how many times specific characters appear in the URL.

| # | Feature | What It Counts | Example URL: `https://g00gle.com/login?user=1` | Value |
|---|---------|---------------|-----------------------------------------------|-------|
| 1 | `url_length` | Total number of characters | Count all characters | 38 |
| 2 | `n_dots` | Number of dots (.) | g00gle**.** com | 2 |
| 3 | `n_hyphens` | Number of hyphens (-) | None in this URL | 0 |
| 4 | `n_underscores` | Number of underscores (_) | None in this URL | 0 |
| 5 | `n_slashes` | Number of forward slashes (/) | https:**//**...**/**login | 3 |
| 6 | `n_question_marks` | Number of question marks (?) | login **?** user=1 | 1 |
| 7 | `n_equal` | Number of equals signs (=) | user **=** 1 | 1 |
| 8 | `n_at` | Number of @ symbols | None in this URL | 0 |
| 9 | `n_ampersand` | Number of & symbols | None in this URL | 0 |
| 10 | `n_percent` | Number of % symbols | None in this URL | 0 |
| 11 | `n_digits` | Number of digit characters (0-9) | g **00** gle...user= **1** | 3 |
| 12 | `n_letters` | Number of letter characters (a-z, A-Z) | Count all letters | 27 |
| 13 | `n_special` | Number of non-alphanumeric characters | :, /, ., ?, = | 8 |

**Why do these matter?** Malicious URLs tend to have more special characters, more
digits (like IP addresses), and are usually longer than legitimate ones.

### Binary Features (7 features)

These are yes/no questions answered as 1 (yes) or 0 (no).

| # | Feature | The Question | Why It Matters |
|---|---------|-------------|----------------|
| 14 | `has_https` | Does the URL start with `https://`? | Legitimate sites almost always use HTTPS (the secure lock icon). Malicious sites often use plain HTTP. |
| 15 | `has_ip` | Does the URL contain an IP address like `192.168.1.1`? | Real websites use names (google.com), not number addresses. If you see numbers, it is suspicious. |
| 16 | `has_at_symbol` | Does the URL contain an `@` symbol? | The @ symbol in a URL can redirect the browser to a completely different site. This is a classic phishing trick. |
| 17 | `double_slash_redirect` | Does the URL have `//` more than once? | Extra double slashes can be used to redirect users to a different hidden website. |
| 18 | `prefix_suffix` | Does the domain name contain a hyphen (`-`)? | Legitimate domains rarely have hyphens. Phishing domains like `paypal-verify.com` use them a lot. |
| 19 | `is_shortened` | Is it a URL shortener (bit.ly, tinyurl.com, etc.)? | Shorteners hide where the link really goes. Scammers love them because you cannot see the real destination. |
| 20 | `suspicious_tld` | Does it end with a suspicious extension (.tk, .xyz, .top, etc.)? | These domain extensions are free or very cheap, so scammers use them to create throwaway phishing sites. |

### Structural Features (5 features)

These measure the "shape" and "structure" of the URL.

| # | Feature | What It Measures | Why It Matters |
|---|---------|-----------------|----------------|
| 21 | `domain_length` | Length of just the domain part | Phishing domains tend to be longer because they try to include brand names plus extra words like `secure-login-paypal-verify.com`. |
| 22 | `n_subdomains` | How many subdomains (counted by dots in the domain) | `login.secure.verify.evil.com` has 4 subdomains. Legitimate sites usually have 0 or 1 (like `www`). |
| 23 | `path_length` | Length of the path after the domain | Malicious URLs often have long paths to hide the real content deep in fake directories. |
| 24 | `url_depth` | How many levels deep the path goes (counted by slashes) | `evil.com/a/b/c/d/e` has depth 5. Legitimate sites rarely go beyond 2-3 levels. |
| 25 | `n_suspicious_words` | Count of phishing keywords like "login", "verify", "account", "password" | Phishing URLs contain words designed to scare you: "verify your account", "update password", "confirm billing". |

### Ratio Features (3 features)

These calculate proportions (what fraction of the URL is made up of certain characters).

| # | Feature | What It Calculates | Why It Matters |
|---|---------|-------------------|----------------|
| 26 | `digit_ratio` | (number of digits) / (total URL length) | A URL like `http://192.168.1.1/8080/` has a high digit ratio. Real websites have more letters than numbers. |
| 27 | `letter_ratio` | (number of letters) / (total URL length) | Legitimate URLs tend to have a higher letter ratio because they use real English words in their domains and paths. |
| 28 | `special_ratio` | (number of special characters) / (total URL length) | Malicious URLs with encoded characters (%20, %3A) or many symbols have higher special ratios. |

### Putting It All Together -- An Example

Let us extract features from two URLs:

**Legitimate:** `https://www.google.com/search`

```
url_length = 30,  n_dots = 2,  n_hyphens = 0,  has_https = 1,
has_ip = 0,  domain_length = 14,  n_subdomains = 2,
n_suspicious_words = 0,  suspicious_tld = 0, ...
```

**Malicious:** `http://192.168.1.55/verify-account/login?password=reset`

```
url_length = 54,  n_dots = 3,  n_hyphens = 1,  has_https = 0,
has_ip = 1,  domain_length = 13,  n_subdomains = 3,
n_suspicious_words = 3 (verify, account, login, password),  suspicious_tld = 0, ...
```

See the differences? The model learns these patterns from thousands of examples!

---

## 7. The 8 Machine Learning Models Explained

### What Is Machine Learning?

**Analogy -- Learning to Ride a Bicycle:** Nobody is born knowing how to ride a bike.
You try, you fall, you adjust, you try again. Eventually, you learn the pattern of
how to balance. Machine Learning works the same way -- we show the computer thousands
of examples, it tries to find patterns, makes mistakes, adjusts, and eventually
learns to make predictions on its own.

Our project trains **8 different types of learners** and then picks the one that
performs best. It is like having 8 students take the same exam and choosing the one
who scored highest.

---

### Model 1: Logistic Regression -- Accuracy: 91.45%

**Analogy -- The Coin Flip Probability Machine**

Imagine you have a special coin. You put a URL's features into a machine, and it
tilts the coin. If the features look legitimate, the coin tilts toward "Heads"
(Legitimate). If the features look suspicious, it tilts toward "Tails" (Malicious).

Logistic Regression calculates a **probability between 0% and 100%**. If the
probability of being malicious is above 50%, it says "Malicious." Otherwise, it
says "Legitimate."

```
Features -----> [ Mathematical Formula ] -----> Probability (0 to 1)
                                                    |
                                            If > 0.5: Malicious
                                            If < 0.5: Legitimate
```

**How it works technically:** It draws a curved S-shaped line (called a "sigmoid
curve") through the data. Everything above the curve is one class, everything below
is the other.

**Strengths:** Simple, fast, easy to understand.
**Weaknesses:** Struggles when the pattern is not a simple straight-line separation.

---

### Model 2: K-Nearest Neighbors (KNN) -- Accuracy: 91.95%

**Analogy -- Ask Your Neighbors**

Imagine you move to a new neighborhood and want to know if a particular restaurant
is good. You do not read reviews online; instead, you **ask your 5 nearest neighbors**.
If 4 out of 5 say "It is great!", you conclude it is a good restaurant.

KNN works exactly like this. When it gets a new URL, it looks at the **5 most
similar URLs** it has already seen (the 5 "nearest neighbors"). If 4 out of 5 of
those were malicious, it says this new URL is probably malicious too.

```
New URL (?)
    |
    |--- Nearest neighbor 1: Malicious
    |--- Nearest neighbor 2: Malicious
    |--- Nearest neighbor 3: Legitimate
    |--- Nearest neighbor 4: Malicious
    |--- Nearest neighbor 5: Malicious
    |
    Result: 4 out of 5 say Malicious ---> MALICIOUS
```

**K = 5** means we look at the 5 closest neighbors. "Closeness" is measured by
how similar the 28 feature values are.

**Strengths:** Very intuitive, no training phase needed.
**Weaknesses:** Slow with large datasets (has to measure distance to every point).

---

### Model 3: SVM (Support Vector Machine) -- Accuracy: 92.30%

**Analogy -- Drawing a Line Between Two Groups**

Imagine you have a playground with red balls on one side and blue balls on the other.
You need to draw a **line on the ground** that separates the reds from the blues as
perfectly as possible. SVM finds the **best possible line** -- specifically, the one
that has the **maximum distance** from the nearest red ball AND the nearest blue ball.

```
  Legitimate URLs (o)          |          Malicious URLs (x)
                               |
      o    o                   |              x    x
         o     o               |          x      x
      o       o    o           |        x    x
            o                  |             x    x
      o        o               |          x
                               |
                        Maximum margin (widest gap)
```

In our project, the "line" is actually a complex boundary in 28-dimensional space
(since we have 28 features). We use an RBF (Radial Basis Function) kernel, which
can draw **curved boundaries**, not just straight lines.

**Strengths:** Very accurate, handles complex patterns well.
**Weaknesses:** Slow to train on very large datasets.

---

### Model 4: Naive Bayes -- Accuracy: 82.85%

**Analogy -- The Probability Calculator**

Imagine a detective who catches criminals based on statistics. The detective knows:
- 80% of criminals wear black shoes
- 60% of criminals are between 20-30 years old
- 70% of criminals have a tattoo

A suspect walks in wearing black shoes, aged 25, with a tattoo. The detective
multiplies these probabilities together to calculate how likely this person is
a criminal.

Naive Bayes does the same thing with URLs. It knows things like:
- 90% of malicious URLs do not have HTTPS
- 75% of malicious URLs have suspicious words
- 60% of malicious URLs have more than 50 characters

It multiplies all these probabilities together to make its prediction.

The word **"Naive"** means it assumes all features are **independent** (unrelated
to each other). This is a simplification -- in reality, features ARE related --
which is why Naive Bayes scored the lowest (82.85%).

**Strengths:** Extremely fast, works well with small datasets.
**Weaknesses:** The "naive" independence assumption hurts accuracy.

---

### Model 5: Decision Tree -- Accuracy: 89.10%

**Analogy -- The 20 Questions Game**

You know the game "20 Questions"? One person thinks of an animal, and the other
person asks yes/no questions to guess it:

- "Is it bigger than a cat?" --> Yes
- "Does it live in water?" --> No
- "Does it have four legs?" --> Yes
- "Is it a horse?" --> Yes!

A Decision Tree works exactly like this game! It asks a series of yes/no questions
about the URL features:

```
                    [URL Length > 60?]
                    /              \
                 YES                NO
                  |                  |
          [Has IP Address?]    [Has HTTPS?]
           /          \          /        \
         YES          NO       YES        NO
          |            |        |          |
      MALICIOUS  [Suspicious   LEGIT   [Dots > 4?]
                  Words > 2?]            /      \
                  /        \           YES      NO
                YES        NO           |        |
                 |          |        MALICIOUS  LEGIT
             MALICIOUS   LEGIT
```

Each question splits the data into two groups, getting more and more specific until
it reaches a conclusion.

**Strengths:** Easy to understand and visualize. Works like human decision-making.
**Weaknesses:** Can "memorize" the training data too well (called overfitting),
leading to poor performance on new data. Our tree has `max_depth=20` to limit this.

---

### Model 6: Random Forest -- Accuracy: 90.65%

**Analogy -- A Team of Decision Trees Voting**

Imagine you are not sure whether a movie is good. Instead of asking just ONE friend,
you ask **100 friends** (each with different tastes and experiences). Then you go
with the **majority vote**. If 70 out of 100 friends say "It is good!", you trust
the majority.

A Random Forest is a **team of 100 Decision Trees** (`n_estimators=100`). Each tree
is trained on a slightly different random sample of the data and looks at a random
subset of features. When a new URL comes in, all 100 trees vote, and the majority
wins.

```
URL Features -----> Tree 1: Legitimate
               |--> Tree 2: Malicious
               |--> Tree 3: Legitimate
               |--> Tree 4: Legitimate
               |--> Tree 5: Malicious
               |--> ... (100 trees total)
               |--> Tree 100: Legitimate
                                |
                    Majority Vote: LEGITIMATE (let's say 65 out of 100)
```

**Why "Random"?** Each tree gets a random portion of the data and features, so they
all learn slightly different patterns. This diversity makes the group smarter than
any single tree.

**Strengths:** Very robust, rarely overfits, gives feature importance rankings.
**Weaknesses:** Slower than a single Decision Tree, harder to interpret.

---

### Model 7: Gradient Boosting -- Accuracy: 92.35% (BEST MODEL)

**Analogy -- Learning from Mistakes**

Imagine a student taking a series of quizzes. After each quiz, the teacher tells
the student **which questions they got wrong**. The student then studies **only those
weak areas** before the next quiz. After many quizzes, the student becomes excellent
because they have specifically targeted and fixed every weakness.

Gradient Boosting works the same way:

```
Round 1: Tree 1 makes predictions ---> Gets some wrong
                                            |
Round 2: Tree 2 focuses on what Tree 1 got WRONG ---> Still some errors
                                                            |
Round 3: Tree 3 focuses on remaining errors ---> Fewer errors
                                                      |
... (100 rounds) ...
                                                      |
Final: Combine all trees ---> Very accurate predictions!
```

**Key difference from Random Forest:** In a Random Forest, all trees work
**independently** (like 100 friends who do not talk to each other). In Gradient
Boosting, each tree **learns from the previous tree's mistakes** (like a student
improving after each quiz).

Our Gradient Boosting model uses:
- `n_estimators=100` (100 rounds of improvement)
- `max_depth=4` (each tree is small and simple)
- `learning_rate=0.1` (learn slowly and carefully from each mistake)

**This is the BEST model in our project at 92.35% accuracy.**

**Strengths:** Highest accuracy, learns from mistakes, handles complex patterns.
**Weaknesses:** Slower to train than simpler models, can overfit if not tuned carefully.

---

### Model 8: MLP Neural Network -- Accuracy: 92.30%

**Analogy -- A Brain Made of Layers**

Your brain has billions of tiny cells called neurons. Each neuron receives signals
from other neurons, processes them, and sends signals forward. An MLP (Multi-Layer
Perceptron) is a simplified computer version of this.

```
INPUT LAYER          HIDDEN LAYER 1       HIDDEN LAYER 2       OUTPUT
(28 features)        (100 neurons)        (50 neurons)         (2 classes)

url_length   ----\
n_dots       -----\-->  [Neuron 1]  --\
n_hyphens    -----/-->  [Neuron 2]  ---\-->  [Neuron 1]  --\
...          ----/      [Neuron 3]  ---/-->  [Neuron 2]  ---\-->  Legitimate
             ----\      ...         --/     ...          ---/-->  Malicious
has_https    -----\-->  [Neuron 99] -/      [Neuron 49] --/
has_ip       -----/-->  [Neuron 100]-       [Neuron 50] -
...          ----/
special_ratio----/
```

Our MLP has:
- **Input layer:** 28 neurons (one for each feature)
- **Hidden layer 1:** 100 neurons (hidden_layer_sizes=(100, 50))
- **Hidden layer 2:** 50 neurons
- **Output layer:** 2 neurons (Legitimate or Malicious)

Each neuron takes numbers in, multiplies them by "weights" (importance values),
adds them up, and passes the result through an activation function. The network
adjusts its weights over 500 training rounds (`max_iter=500`).

**Strengths:** Can learn very complex patterns that simpler models miss.
**Weaknesses:** Hard to interpret (it is a "black box"), needs more data and time.

---

## 8. Model Comparison and Why Gradient Boosting Won

### Full Results Table

| Rank | Model | Accuracy | Precision | Recall | F1 Score |
|------|-------|----------|-----------|--------|----------|
| 1 | **Gradient Boosting** | **92.35%** | 91.53% | **93.10%** | **92.31%** |
| 2 | SVM | 92.30% | 91.52% | 93.00% | 92.25% |
| 3 | MLP Neural Network | 92.30% | 91.43% | 93.10% | 92.26% |
| 4 | K-Nearest Neighbors | 91.95% | 91.46% | 92.29% | 91.87% |
| 5 | Logistic Regression | 91.45% | 92.05% | 90.47% | 91.25% |
| 6 | Random Forest | 90.65% | 90.56% | 90.47% | 90.51% |
| 7 | Decision Tree | 89.10% | 91.03% | 86.41% | 88.66% |
| 8 | Naive Bayes | 82.85% | 92.25% | 71.20% | 80.37% |

### Understanding the Metrics

**Analogy -- A Doctor Testing for a Disease:**

- **Accuracy:** Out of ALL patients tested, how many did the doctor diagnose correctly?
  (92.35% means out of 2,000 test URLs, 1,847 were classified correctly.)

- **Precision:** Out of everyone the doctor said "You have the disease," how many
  ACTUALLY had it? (91.53% means when the model says "Malicious," it is right
  91.53% of the time.)

- **Recall:** Out of everyone who ACTUALLY had the disease, how many did the doctor
  catch? (93.10% means out of all truly malicious URLs, the model caught 93.10%.)

- **F1 Score:** A balanced combination of Precision and Recall. Like an overall
  grade that considers both false alarms AND missed detections.

### Why Gradient Boosting Won

1. **Highest accuracy (92.35%):** It correctly classified more URLs than any other model.

2. **Best recall (93.10%, tied with MLP):** It caught the most truly malicious URLs.
   Missing a malicious URL is worse than a false alarm, so high recall is critical
   for security.

3. **Learning from mistakes:** Its sequential, error-correcting approach (each tree
   focuses on what previous trees got wrong) is ideal for the subtle patterns in URL
   features.

4. **Handling mixed feature types:** Our 28 features include counts, binary values,
   and ratios. Gradient Boosting handles this mix naturally through its tree-based
   structure.

5. **Beating the noise:** Remember, 8% of labels in our dataset were intentionally
   flipped. Gradient Boosting is robust against this kind of noise because each
   boosting round focuses on the hardest examples, gradually learning to tolerate
   ambiguous cases.

### Why Naive Bayes Performed Worst

Naive Bayes assumes all 28 features are **independent** (unrelated). But in reality,
features are related: a URL with an IP address (`has_ip=1`) is also likely to have
a high `digit_ratio` and probably lacks HTTPS (`has_https=0`). By ignoring these
relationships, Naive Bayes loses valuable information, resulting in 82.85% accuracy
and a particularly low recall of 71.20% (missing almost 30% of malicious URLs).

---

## 9. Flask Web Application Architecture

### The Analogy -- A Restaurant

Think of the Flask app as a restaurant:

| Restaurant | Flask App |
|------------|-----------|
| Customer walks in | User opens browser and goes to `localhost:5004` |
| Waiter takes the order | Flask receives the HTTP request |
| Kitchen prepares food | Python code processes data, runs ML model |
| Food is plated nicely | HTML template is rendered with data |
| Waiter serves the food | Flask sends the HTML page back to the browser |

### How Flask Routes Work

A **route** is a URL path mapped to a Python function. When you visit a URL, Flask
calls the matching function:

```python
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # This function runs when you visit localhost:5004/predict
    ...
```

### All Pages in the Application

| Route | Page | What It Does |
|-------|------|-------------|
| `/login` | Login Page | Enter username and password to sign in |
| `/register` | Register Page | Create a new account (name, username, password) |
| `/logout` | (redirect) | Clears session and redirects to login |
| `/home` | Home/Dashboard | Shows your stats: total scans, malicious found, recent 5 scans. Admin users see global stats too. |
| `/predict` | Detect Page | The main feature! Enter a URL, click "Analyze", and see if it is Legitimate or Malicious with confidence %. Also shows extracted features. |
| `/history` | History Page | Table of all your past scans with URL, prediction, confidence, and timestamp |
| `/visualize` | Visualize Page | Gallery of 12 EDA charts showing patterns in the training dataset |
| `/dashboard` | Model Dashboard | Comparison table and charts of all 8 ML models' accuracy, precision, recall, F1 |
| `/about` | About Page | Project info, list of all 28 features, technology stack used |

### Request-Response Cycle

Here is what happens when you click "Analyze" on the Detect page:

```
1. Browser sends POST request to /predict with the URL you typed
                    |
                    v
2. Flask receives the request, extracts the URL from the form
                    |
                    v
3. The extract_features() function calculates 28 numbers from the URL
                    |
                    v
4. These 28 numbers are fed into the Gradient Boosting model
                    |
                    v
5. The model returns probabilities: [0.15 for Legitimate, 0.85 for Malicious]
                    |
                    v
6. The prediction and confidence are saved to the SQLite database
                    |
                    v
7. Flask renders the predict.html template with the results
                    |
                    v
8. The browser displays: "MALICIOUS - 85.00% confidence" with feature details
```

### Session Management

Flask uses **sessions** to remember who is logged in. A session is like a wristband
at a waterpark -- once you get it at the entrance (login), you can go on any ride
(any page) without showing your ticket again.

```python
session['user_id'] = user['id']       # Store user ID
session['username'] = user['username'] # Store username
session['name'] = user['name']         # Store display name
session['is_admin'] = user['is_admin'] # Store admin status
```

Every protected page checks `if 'user_id' not in session:` -- if you are not logged
in, you get redirected to the login page.

---

## 10. Database Design

### The Analogy -- A School Record System

Think of the database as a **school's record-keeping system** with two filing drawers:
- **Drawer 1 (users):** Student registration cards
- **Drawer 2 (predictions):** Exam result sheets linked to each student

### The `users` Table

```
+----+---------------+----------+-------------------+----------+---------------------+
| id | name          | username | password          | is_admin | created_at          |
+----+---------------+----------+-------------------+----------+---------------------+
| 1  | Administrator | admin    | pbkdf2:sha256:... | 1        | 2024-01-15 10:30:00 |
| 2  | John Doe      | john     | pbkdf2:sha256:... | 0        | 2024-01-16 14:22:00 |
| 3  | Jane Smith    | jane     | pbkdf2:sha256:... | 0        | 2024-01-17 09:15:00 |
+----+---------------+----------+-------------------+----------+---------------------+
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER, Primary Key, Auto-increment | Unique number for each user |
| name | TEXT, NOT NULL | Full display name |
| username | TEXT, UNIQUE, NOT NULL | Login username (must be unique) |
| password | TEXT, NOT NULL | Hashed password (NOT stored as plain text!) |
| is_admin | INTEGER, Default 0 | 1 = admin, 0 = regular user |
| created_at | TEXT, Default CURRENT_TIMESTAMP | When the account was created |

**Note:** An admin account is **automatically created** when the app starts for the
first time (username: `admin`, password: `admin123`).

### The `predictions` Table

```
+----+---------+-----------------------------------+------------+------------+------------+---------+--------+---------------------+
| id | user_id | url                               | prediction | confidence | url_length | has_https| has_ip | created_at          |
+----+---------+-----------------------------------+------------+------------+------------+---------+--------+---------------------+
| 1  | 2       | https://google.com                | Legitimate | 96.50      | 18         | 1       | 0      | 2024-01-16 14:30:00 |
| 2  | 2       | http://192.168.1.1/login          | Malicious  | 89.20      | 26         | 0       | 1      | 2024-01-16 14:31:00 |
| 3  | 3       | http://g00gle.com/verify          | Malicious  | 91.80      | 27         | 0       | 0      | 2024-01-17 09:20:00 |
+----+---------+-----------------------------------+------------+------------+------------+---------+--------+---------------------+
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER, Primary Key | Unique prediction ID |
| user_id | INTEGER, Foreign Key -> users.id | Which user made this prediction |
| url | TEXT | The URL that was analyzed |
| prediction | TEXT | "Legitimate" or "Malicious" |
| confidence | REAL | How confident the model is (e.g., 92.35) |
| url_length | INTEGER | Length of the URL (stored for quick reference) |
| has_https | INTEGER | Whether the URL uses HTTPS |
| has_ip | INTEGER | Whether the URL contains an IP address |
| n_suspicious_words | INTEGER | Count of suspicious keywords found |
| created_at | TEXT | When the prediction was made |

### The Foreign Key Relationship

```
    users TABLE                          predictions TABLE
    +----------+                         +-----------+
    | id = 2   |  <------- user_id = 2   | id = 1    |
    | name =   |                         | url = ... |
    | "John"   |  <------- user_id = 2   | id = 2    |
    +----------+                         | url = ... |
                                         +-----------+
```

The `user_id` column in predictions points back to the `id` column in users. This
way, every prediction is linked to the user who made it. John can only see his own
predictions, not Jane's.

---

## 11. How Prediction Works Step by Step

### The Complete Pipeline

Here is the entire journey from "user types a URL" to "app shows the result":

```
STEP 1: User types URL
"http://g00gle.com/verify-account"
            |
            v
STEP 2: URL Validation
- Check if it contains "://" or "."
- Add "http://" if no protocol given
            |
            v
STEP 3: Feature Extraction (extract_features function)
- Count characters: length=35, dots=2, hyphens=1, ...
- Check binary flags: has_https=0, has_ip=0, has_at=0, ...
- Calculate structure: domain_length=11, n_subdomains=1, ...
- Count suspicious words: "verify" + "account" = 2
- Calculate ratios: digit_ratio=0.057, letter_ratio=0.714, ...
            |
            v
STEP 4: Create Feature Array
[35, 2, 1, 1, 3, 0, 0, 0, 0, 0, 2, 25, 8, 0, 0, 11, 1, 14, 1, 0, 0, 1, 2, 0, 0, 0.057, 0.714, 0.229]
(28 numbers in the exact order the model expects)
            |
            v
STEP 5: Model Prediction (model.predict_proba)
Gradient Boosting model processes the 28 numbers through
its 100 sequential decision trees
            |
            v
STEP 6: Get Probabilities
[0.12, 0.88]
 |       |
 |       +-- 88% chance of being Malicious (class 1)
 +---------- 12% chance of being Legitimate (class 0)
            |
            v
STEP 7: Determine Result
- Highest probability: 0.88 (class 1 = Malicious)
- Confidence: 88.00%
- Result: "Malicious"
            |
            v
STEP 8: Save to Database
INSERT INTO predictions (user_id, url, prediction, confidence, ...)
            |
            v
STEP 9: Render Result Page
- Show big red badge: "MALICIOUS"
- Show confidence: "88.00%"
- Show feature breakdown table
```

### The Key Code

```python
def predict_url(url):
    """Extract features from a URL and predict if malicious."""
    # Step 3: Extract 28 features
    features = extract_features(url)

    # Step 4: Put features in correct order as an array
    feature_values = [features[f] for f in FEATURE_ORDER]
    arr = np.array([feature_values])

    # Step 5-6: Get probabilities from the model
    proba = model.predict_proba(arr)[0]     # e.g., [0.12, 0.88]
    pred_class = int(np.argmax(proba))       # Index of highest: 1
    confidence = round(proba[pred_class] * 100, 2)  # 88.00

    # Step 7: Convert to human-readable label
    prediction = 'Malicious' if pred_class == 1 else 'Legitimate'
    return prediction, confidence, features
```

### What `predict_proba` Returns

The model does not just say "Malicious" or "Legitimate." It gives **probabilities
for both classes**:

```
model.predict_proba([[28 feature values]])

Returns: [[0.12, 0.88]]
            |      |
            |      +-- Probability of being Malicious (class 1)
            +--------- Probability of being Legitimate (class 0)

These always add up to 1.00 (100%)
```

We take the higher probability as the prediction and its value as the confidence score.

---

## 12. EDA Visualizations Explained

### What Is EDA?

**Analogy -- Looking at Your Report Card Before Studying**

Before you start studying for exams, you look at your report card to see which
subjects you are good at and which ones need work. EDA (Exploratory Data Analysis)
is the same thing but for data -- we look at charts and graphs to understand our
dataset before training any models.

### The 12 Visualizations

Our project generates 12 charts saved as PNG images in `static/vis/`:

---

**1. Label Distribution (`label_dist.png`) -- Pie Chart**

Shows the split between Legitimate (50%) and Malicious (50%) URLs in our dataset.
A balanced dataset (equal numbers of both classes) is ideal because the model gets
to see equal examples of both types.

---

**2. URL Length Distribution (`url_length.png`) -- Histogram**

Shows how long URLs are for each class. You will see:
- Legitimate URLs: mostly short (20-50 characters)
- Malicious URLs: spread across a wider range, often longer (40-100+ characters)

**Insight:** Malicious URLs tend to be longer because attackers stuff them with
fake paths, parameters, and suspicious words.

---

**3. HTTPS vs HTTP Distribution (`https_dist.png`) -- Bar Chart**

Shows how many URLs use HTTPS vs HTTP for each class.
- Legitimate: overwhelmingly HTTPS (90%)
- Malicious: much higher proportion of HTTP

**Insight:** The padlock icon (HTTPS) is a sign of a legitimate website. Scammers
often skip HTTPS because getting an SSL certificate requires identity verification.

---

**4. IP Address Presence (`ip_dist.png`) -- Bar Chart**

Shows how many URLs contain an IP address (like `192.168.1.1`) instead of a domain name.
- Legitimate: almost never have IP addresses
- Malicious: a significant portion use IP addresses

**Insight:** Real websites use domain names (google.com), not raw numbers. Using
numbers instead of names is a major red flag.

---

**5. Suspicious Words Count (`suspicious_words.png`) -- Histogram**

Shows how many phishing keywords (login, verify, account, password, etc.) appear in
each URL.
- Legitimate: usually 0 suspicious words
- Malicious: often 1-3 or more suspicious words

**Insight:** Phishing URLs include scary words to create urgency: "Verify your
account NOW" or "Update your password immediately."

---

**6. Domain Length Distribution (`domain_length.png`) -- Histogram**

Shows the length of just the domain name part.
- Legitimate: typically 10-20 characters (google.com = 10)
- Malicious: often longer (secure-login-paypal-verify.com = 31)

**Insight:** Attackers create long domain names that try to include a trusted brand
name plus extra deceptive words.

---

**7. Number of Subdomains (`subdomains.png`) -- Histogram**

Shows how many levels of subdomains each URL has.
- Legitimate: usually 1 (www.google.com -> 1 subdomain)
- Malicious: sometimes 3-5 (login.secure.verify.evil.com -> 4 subdomains)

**Insight:** Attackers stack subdomains to make the URL look complex and to hide
the real domain at the end.

---

**8. Special Character Ratio (`special_ratio.png`) -- Histogram**

Shows what fraction of the URL is made up of special characters (symbols like /, ?, =, %, @).
- Legitimate: lower special character ratio
- Malicious: higher ratio (more encoded characters, symbols)

**Insight:** Malicious URLs often contain encoded characters (%20, %3A) to hide
their true destination.

---

**9. URL Path Depth (`url_depth.png`) -- Histogram**

Shows how many directory levels deep the URL path goes.
- Legitimate: usually 0-2 levels (/about, /products/shoes)
- Malicious: sometimes 4-8 levels (/a/b/c/d/e/login)

**Insight:** Attackers create deep, complex paths to confuse users and hide
malicious content.

---

**10. Feature Correlation Heatmap (`correlation.png`)**

A colored grid showing how much each feature is related to every other feature.
Red means positive correlation (when one goes up, the other goes up too). Blue
means negative correlation.

**Key finding:** `has_https` is negatively correlated with `label` (meaning
legitimate URLs tend to have HTTPS), while `n_suspicious_words` and `has_ip` are
positively correlated with `label` (malicious URLs tend to have these).

---

**11. Feature Importance (`feature_importance.png`) -- Bar Chart**

Shows which of the 28 features are most important for making predictions, as
determined by the Random Forest model. The longer the bar, the more important
that feature is.

**Typical top features:** `url_length`, `n_suspicious_words`, `has_https`,
`domain_length`, `path_length`, `n_dots`, and `special_ratio`.

---

**12. Confusion Matrix (`confusion_matrix.png`) -- Heatmap**

A 2x2 grid showing the four possible outcomes for the best model (Gradient Boosting):

```
                          PREDICTED
                    Legitimate  Malicious
                  +------------+----------+
ACTUAL Legitimate |    929     |    85    |  (True Neg + False Pos)
                  +------------+----------+
ACTUAL Malicious  |     68     |   918    |  (False Neg + True Pos)
                  +------------+----------+
```

| Cell | Name | Meaning |
|------|------|---------|
| 929 | True Negative (TN) | Correctly said "Legitimate" for a legitimate URL |
| 85 | False Positive (FP) | Wrongly said "Malicious" for a legitimate URL (false alarm) |
| 68 | False Negative (FN) | Wrongly said "Legitimate" for a malicious URL (missed danger!) |
| 918 | True Positive (TP) | Correctly said "Malicious" for a malicious URL |

**The most dangerous cell is 68 (False Negatives):** These are malicious URLs that
the model missed. In security, missing a threat is worse than a false alarm.

---

## 13. Security Features

### 13.1 Password Hashing

**Analogy -- The Paper Shredder**

Imagine you write your password on a piece of paper, put it through a **special
shredder**, and store the shredded result. If someone breaks into the filing cabinet,
they find shredded paper, not your actual password. But when you come back and write
your password again, the same shredder produces the **same shredded pattern**, so the
system can verify it is you.

This is exactly what **Werkzeug's password hashing** does:

```python
# When registering -- hash the password before storing
hashed = generate_password_hash('mypassword123')
# Stored in database: "pbkdf2:sha256:260000$abc123$def456..."

# When logging in -- compare the hash, not the plain text
if check_password_hash(stored_hash, 'mypassword123'):
    print("Password matches!")
```

**What is stored in the database:**
```
NOT this:  mypassword123
BUT this:  pbkdf2:sha256:260000$Wq8R3kLp$a1b2c3d4e5f6...
```

Even if someone steals the entire database, they **cannot reverse** the hash to get
the original password. The algorithm used is **PBKDF2 with SHA-256**, which is
industry-standard and includes:
- **Salt:** A random string added to each password before hashing (so two users
  with the same password get different hashes)
- **Iterations (260,000 rounds):** The hashing is repeated hundreds of thousands
  of times, making brute-force attacks extremely slow

### 13.2 XSS Protection via Jinja2

**Analogy -- The Customs Officer Checking Your Luggage**

When you travel internationally, customs officers check your luggage for prohibited
items. Similarly, Jinja2 (Flask's HTML template engine) checks all user-provided
data before putting it on the web page.

**Cross-Site Scripting (XSS)** is an attack where a bad person tries to inject
malicious JavaScript code into a web page. For example, if someone enters this as
their "name" during registration:

```
<script>alert('Hacked!')</script>
```

Without protection, this code would run in other users' browsers. But Jinja2
**automatically escapes** all special HTML characters:

```
Input:   <script>alert('Hacked!')</script>
Output:  &lt;script&gt;alert(&#39;Hacked!&#39;)&lt;/script&gt;
```

The browser treats the escaped version as plain text, not executable code. This
happens automatically whenever you use `{{ variable }}` in Flask templates.

### 13.3 Session-Based Authentication

Every page (except login and register) checks whether the user is logged in:

```python
if 'user_id' not in session:
    return redirect(url_for('login'))
```

This prevents unauthorized users from accessing the prediction, history, or
dashboard pages directly by typing the URL.

### 13.4 SQL Injection Prevention

**Analogy:** Imagine someone fills out a form asking for their name, but instead
writes: `John"; DROP TABLE users; --`. If the app naively puts this into a database
query, it could delete all user data!

Our app uses **parameterized queries** (the `?` placeholder), which prevent this:

```python
# SAFE -- uses ? placeholder
db.execute('SELECT * FROM users WHERE username = ?', (username,))

# UNSAFE (NOT used in our app) -- string concatenation
db.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

With parameterized queries, the database treats the entire input as a plain string
value, never as executable SQL commands.

---

## 14. Viva Questions and Answers

### Q1. What is the main objective of this project?

**Answer:** The main objective is to build a machine learning-based web application
that can detect whether a given URL is legitimate (safe) or malicious (dangerous/phishing).
The user enters a URL into a Flask web app, the system extracts 28 numerical features
from the URL string, and a trained Gradient Boosting model predicts whether the URL
is Legitimate or Malicious along with a confidence percentage.

---

### Q2. Why did you choose Gradient Boosting as the final model?

**Answer:** We compared 8 different machine learning models on the same test set of
2,000 URLs. Gradient Boosting achieved the highest accuracy of 92.35%, the highest
recall of 93.10% (tied with MLP), and the highest F1 score of 92.31%. Gradient
Boosting excels because it uses a sequential learning approach where each new decision
tree specifically focuses on correcting the mistakes of the previous trees, leading
to progressively better predictions. This makes it particularly effective for our
dataset which has 8% label noise.

---

### Q3. What is feature extraction and why is it necessary?

**Answer:** Feature extraction is the process of converting a raw URL string (text)
into a set of 28 numerical values that a machine learning model can understand.
Machine learning models cannot process raw text directly -- they need numbers. For
example, the URL `https://google.com` gets converted into numbers like url_length=18,
n_dots=1, has_https=1, has_ip=0, and so on. These 28 numbers act as a "fingerprint"
of the URL that captures its structural and statistical properties.

---

### Q4. Explain the difference between Precision and Recall in the context of this project.

**Answer:** **Precision** answers: "Out of all URLs the model flagged as malicious,
how many were actually malicious?" A precision of 91.53% means that when the model
says a URL is malicious, it is correct 91.53% of the time (8.47% are false alarms).
**Recall** answers: "Out of all URLs that were truly malicious, how many did the
model catch?" A recall of 93.10% means the model successfully detected 93.10% of
all malicious URLs, but missed 6.90%. In security applications, recall is often
more important because missing a malicious URL (false negative) is more dangerous
than a false alarm (false positive).

---

### Q5. How does the dataset generation work? Why use synthetic data?

**Answer:** The `generate_dataset.py` script creates 10,000 synthetic (artificially
generated) URLs -- 5,000 legitimate and 5,000 malicious. Legitimate URLs are built
from real domain names like google.com and amazon.com with realistic paths. Malicious
URLs are generated using 8 attack strategies: IP-based URLs, long subdomain chains,
misspelled domain names, URL shorteners, encoded characters, deep paths, suspicious
keyword patterns, and mixed attacks. We use synthetic data because (a) it gives us
full control over the balance and difficulty of the dataset, (b) we do not need to
collect and handle real malicious URLs which could pose security risks, and (c) we
can add controlled noise (8% label flipping) to simulate real-world imperfections.

---

### Q6. What is the purpose of adding 8% noise by flipping labels?

**Answer:** In real life, no classification problem is perfectly clean. Some
legitimate-looking URLs turn out to be malicious, and some suspicious-looking URLs
are actually safe. Flipping 8% of labels (800 out of 10,000) simulates this
real-world ambiguity. Without noise, the models might achieve 99%+ accuracy, which
would be unrealistically optimistic. The noise creates a realistic ceiling on
performance (around 92%) and helps reveal meaningful differences between models --
for example, it shows that Naive Bayes (82.85%) handles noise poorly while Gradient
Boosting (92.35%) handles it well.

---

### Q7. What is a confusion matrix? Explain each cell.

**Answer:** A confusion matrix is a 2x2 table that shows four outcomes of a
classification model. For our best model (Gradient Boosting):
- **True Negative (929):** The model correctly predicted "Legitimate" for URLs that
  were actually legitimate.
- **False Positive (85):** The model incorrectly predicted "Malicious" for URLs
  that were actually legitimate (false alarm).
- **False Negative (68):** The model incorrectly predicted "Legitimate" for URLs
  that were actually malicious (missed threat -- the most dangerous error).
- **True Positive (918):** The model correctly predicted "Malicious" for URLs that
  were actually malicious.
The total test set size is 929 + 85 + 68 + 918 = 2,000 URLs.

---

### Q8. What is Flask and how does it work in this project?

**Answer:** Flask is a lightweight Python web framework that handles HTTP
requests and responses. It works like a waiter in a restaurant: when a user's
browser sends a request (like visiting `/predict`), Flask routes it to the
appropriate Python function, which processes the request (runs the ML model),
and returns a response (an HTML page with the prediction result). In our project,
Flask runs on port 5004 and provides 8 routes: login, register, logout, home,
predict, history, visualize, dashboard, and about. It uses Jinja2 templates to
render HTML pages dynamically with data.

---

### Q9. How is password security handled in this project?

**Answer:** Passwords are never stored in plain text. When a user registers,
the password is hashed using Werkzeug's `generate_password_hash()` function,
which uses the PBKDF2-SHA256 algorithm with a random salt and 260,000 iterations.
The resulting hash string (like `pbkdf2:sha256:260000$...`) is stored in the
database. When the user logs in, `check_password_hash()` hashes the entered
password the same way and compares it to the stored hash. Even if an attacker
gains access to the database, they cannot reverse the hash to get the original
password. The salt ensures that two users with the same password will have
different hash values.

---

### Q10. What is the difference between Random Forest and Gradient Boosting?

**Answer:** Both are ensemble methods that use multiple decision trees, but they
differ fundamentally in how the trees are built:
- **Random Forest:** Builds 100 trees **independently and in parallel**. Each tree
  is trained on a random sample of the data with a random subset of features. The
  final prediction is a **majority vote** of all trees. Think of it as 100 friends
  independently giving their opinions.
- **Gradient Boosting:** Builds 100 trees **sequentially**. Each new tree is trained
  specifically on the **mistakes** of the previous trees. The final prediction is the
  **sum of all trees' contributions**. Think of it as one student retaking an exam
  100 times, each time focusing on questions they previously got wrong.
Gradient Boosting generally achieves higher accuracy because it directly corrects
errors, but it is slower to train because trees must be built one after another.

---

### Q11. Explain the role of `train_test_split` in this project.

**Answer:** `train_test_split` divides our dataset of 10,000 URLs into two parts:
80% for training (8,000 URLs) and 20% for testing (2,000 URLs). The training set
is used to teach the model patterns in URLs. The test set is held back and used
to evaluate how well the model performs on URLs it has never seen before. This
simulates real-world usage where the model encounters new, unknown URLs. The
parameter `stratify=y` ensures that both the training and test sets maintain the
same 50/50 ratio of legitimate to malicious URLs. `random_state=42` ensures the
split is reproducible (same split every time the code runs).

---

### Q12. What is a pickle file and why is it used?

**Answer:** A pickle file (`.pkl`) is Python's way of saving an object (like a
trained ML model) to disk so it can be loaded later without retraining. In our
project, `train_model.py` trains the Gradient Boosting model (which takes time)
and saves it as `url_model.pkl`. When `app.py` starts, it loads the pre-trained
model from this file in milliseconds. Without pickling, we would have to retrain
the model every time the app restarts, which would be slow and impractical.
The word "pickle" comes from the idea of "preserving" -- like pickling vegetables
to eat later.

---

### Q13. What are suspicious TLDs and why are they important features?

**Answer:** TLD stands for Top-Level Domain -- the last part of a domain name like
`.com`, `.org`, or `.net`. Suspicious TLDs include `.tk`, `.ml`, `.ga`, `.cf`,
`.gq`, `.xyz`, `.top`, `.club`, `.work`, and `.buzz`. These are considered
suspicious because they are either free or very cheap to register, which means
scammers can create thousands of phishing websites at no cost using these extensions.
Legitimate businesses typically use established TLDs like `.com`, `.org`, `.edu`,
or country-specific ones. In our feature extraction, `suspicious_tld` is a binary
feature (1 if the URL has a suspicious TLD, 0 otherwise) that helps the model
identify potentially malicious URLs.

---

### Q14. How does the `@` symbol in a URL trick users?

**Answer:** In URL syntax, the `@` symbol separates user credentials from the actual
domain. When a browser sees `http://google.com@evil.com/steal`, it ignores everything
before the `@` (including `google.com`) and actually navigates to `evil.com/steal`.
A user might see "google.com" in the URL and think they are going to Google, but they
are actually being taken to `evil.com`. This is why `has_at_symbol` is one of our 28
features -- its presence is a strong indicator of a phishing attempt. Modern browsers
now warn users about `@` symbols in URLs, but older browsers and many URL previews
still show the deceptive portion.

---

### Q15. What is the role of StandardScaler in some of the models?

**Answer:** StandardScaler transforms each feature so that it has a mean of 0 and a
standard deviation of 1 (called "standardization" or "z-score normalization"). This
is necessary for models like Logistic Regression, SVM, KNN, and MLP because they
are sensitive to the scale of features. For example, `url_length` might range from
10 to 200, while `has_https` is only 0 or 1. Without scaling, the model would give
disproportionate weight to `url_length` simply because its numbers are larger.
Tree-based models (Decision Tree, Random Forest, Gradient Boosting) and Naive Bayes
do NOT need scaling because they make decisions based on thresholds and probabilities,
not distances. In our code, StandardScaler is applied using `make_pipeline()` which
ensures the same scaling is applied consistently during both training and prediction.

---

### Q16. What is the purpose of the `models_info.json` file?

**Answer:** The `models_info.json` file stores the complete results from training all
8 models. It contains: (1) the accuracy, precision, recall, F1 score, and confusion
matrix for each model, (2) the name of the best model ("Gradient Boosting"), (3) the
ordered list of all 28 feature names, and (4) the training and test set sizes (8,000
and 2,000). This file is loaded by `app.py` to display model comparison data on the
Dashboard and About pages without needing to retrain. It also provides the
`FEATURE_ORDER` list, which ensures features are fed to the model in the exact same
order they were used during training.

---

### Q17. How does the MLP Neural Network differ from the other models?

**Answer:** The MLP (Multi-Layer Perceptron) is the only model in our project that
is inspired by the human brain. Unlike the other models which use mathematical
formulas (Logistic Regression), distance measurements (KNN), boundary drawing (SVM),
probabilities (Naive Bayes), or tree-based rules (Decision Tree, Random Forest,
Gradient Boosting), the MLP uses **layers of artificial neurons**. Our MLP has an
input layer (28 neurons for 28 features), a first hidden layer (100 neurons), a
second hidden layer (50 neurons), and an output layer (2 neurons for 2 classes).
Each neuron applies a nonlinear transformation to its inputs, allowing the network
to learn complex, non-obvious patterns. However, MLP is a "black box" -- unlike a
Decision Tree, you cannot easily see why it made a particular decision.

---

### Q18. Why is SQLite used instead of MySQL or PostgreSQL?

**Answer:** SQLite is a "serverless" database that stores everything in a single file
(`url_detect.db`). Unlike MySQL or PostgreSQL, which require a separate database
server to be installed, configured, and running, SQLite works out of the box with
zero configuration. For our project, which is a single-user or small-team
application, SQLite is the perfect choice because: (1) it requires no setup, (2) the
database is just one file that can be copied or backed up easily, (3) it is built
into Python's standard library (`import sqlite3`), and (4) it is lightweight and
fast for our scale (thousands of records, not millions). For a production system
serving millions of users, we would upgrade to PostgreSQL or MySQL.

---

### Q19. What would happen if you skipped feature extraction and fed the raw URL string directly to the model?

**Answer:** The model would fail because machine learning models can only process
numerical data, not raw text strings. You cannot feed "https://google.com" directly
into a mathematical algorithm. Feature extraction is the crucial bridge between human-
readable text and machine-readable numbers. Without it, we would need to use
Natural Language Processing (NLP) techniques like tokenization and word embeddings
to convert text into numbers, which would make the project significantly more complex.
Our approach of hand-crafting 28 meaningful features (url_length, has_https,
n_suspicious_words, etc.) is both effective and interpretable -- we know exactly what
each number means and why it matters for detecting malicious URLs.

---

### Q20. If you were to improve this project, what would you add?

**Answer:** Several improvements could be made:
(1) **Real-world dataset:** Replace synthetic data with a real dataset from sources
like PhishTank or the UCI ML Repository for more realistic performance evaluation.
(2) **Real-time URL checking:** Actually visit the URL (safely, in a sandbox) to
check if the website content looks like a phishing page.
(3) **WHOIS lookup:** Check the domain registration date -- newly registered domains
are more suspicious.
(4) **Google Safe Browsing API:** Cross-reference predictions with Google's database
of known malicious URLs.
(5) **Deep learning:** Use a character-level CNN or LSTM that can learn patterns
directly from the raw URL text without manual feature engineering.
(6) **Browser extension:** Package the model into a Chrome/Firefox extension that
checks URLs in real-time as you browse.
(7) **Model retraining:** Add a feedback mechanism where users can report incorrect
predictions, and periodically retrain the model with this new data.

---

*This document provides a complete explanation of the C12 Malicious URL Detection
project. Every component -- from dataset generation to machine learning models to
web application architecture -- has been explained with real-world analogies suitable
for beginners.*
