"""
Generate synthetic Malicious URL Detection dataset.
Creates 10,000 URLs (5,000 legitimate + 5,000 malicious) with extracted features.
"""
import pandas as pd
import numpy as np
import random
import string
import re

random.seed(42)
np.random.seed(42)

# ───────────── Legitimate domain patterns ─────────────
LEGIT_DOMAINS = [
    'google.com', 'amazon.com', 'facebook.com', 'twitter.com', 'linkedin.com',
    'github.com', 'stackoverflow.com', 'microsoft.com', 'apple.com', 'netflix.com',
    'youtube.com', 'wikipedia.org', 'reddit.com', 'instagram.com', 'yahoo.com',
    'bbc.com', 'cnn.com', 'nytimes.com', 'medium.com', 'quora.com',
    'adobe.com', 'dropbox.com', 'slack.com', 'zoom.us', 'spotify.com',
    'paypal.com', 'ebay.com', 'walmart.com', 'target.com', 'bestbuy.com',
    'coursera.org', 'udemy.com', 'edx.org', 'kaggle.com', 'python.org',
    'npmjs.com', 'docker.com', 'aws.amazon.com', 'cloud.google.com', 'azure.com',
    'heroku.com', 'digitalocean.com', 'godaddy.com', 'shopify.com', 'stripe.com',
    'twitch.tv', 'pinterest.com', 'tumblr.com', 'flickr.com', 'deviantart.com',
]

LEGIT_PATHS = [
    '', '/about', '/contact', '/products', '/services', '/blog', '/news',
    '/help', '/support', '/faq', '/terms', '/privacy', '/careers',
    '/search', '/docs', '/api', '/dashboard', '/settings', '/profile',
    '/home', '/features', '/pricing', '/download', '/resources',
]

LEGIT_SUBDOMAINS = ['www', 'mail', 'docs', 'drive', 'maps', 'blog', 'shop', 'app', 'api', 'dev']

# ───────────── Malicious patterns ─────────────
SUSPICIOUS_WORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'confirm', 'bank',
    'signin', 'password', 'credential', 'security', 'alert', 'suspended',
    'unlock', 'restore', 'wallet', 'payment', 'billing', 'invoice',
]

PHISHING_DOMAINS = [
    'secure-login-verify.com', 'account-update-now.net', 'bank-security-alert.org',
    'paypal-verify.info', 'amazon-login-secure.com', 'facebook-confirm.net',
    'google-account-recovery.org', 'apple-id-verify.info', 'netflix-billing.com',
    'microsoft-security.net',
]

SHORTENERS = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'ow.ly']

TLDs_SUSPICIOUS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.buzz']


def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"


def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_legit_url():
    """Generate a realistic legitimate URL."""
    protocol = random.choice(['https://'] * 9 + ['http://'])
    subdomain = random.choice(LEGIT_SUBDOMAINS + [''] * 5)
    domain = random.choice(LEGIT_DOMAINS)
    path = random.choice(LEGIT_PATHS)

    if subdomain and not domain.startswith(subdomain):
        url = f"{protocol}{subdomain}.{domain}{path}"
    else:
        url = f"{protocol}{domain}{path}"

    # Sometimes add simple query params
    if random.random() < 0.2:
        param = random.choice(['q', 'id', 'page', 'ref', 'lang', 'sort'])
        value = random.choice(['1', 'en', 'home', 'true', random_string(5)])
        url += f"?{param}={value}"

    return url


def generate_malicious_url():
    """Generate a realistic malicious/phishing URL."""
    strategy = random.choice(['ip', 'long_subdomain', 'suspicious', 'misspell',
                               'shortened', 'encoded', 'deep_path', 'mixed'])

    if strategy == 'ip':
        # URL with IP address instead of domain
        protocol = random.choice(['http://', 'https://'])
        ip = random_ip()
        path = '/' + '/'.join(random.choices(SUSPICIOUS_WORDS, k=random.randint(1, 3)))
        url = f"{protocol}{ip}{path}"
        if random.random() < 0.4:
            url += f"?user={random_string(8)}&token={random_string(16)}"

    elif strategy == 'long_subdomain':
        # Many subdomains to hide the real domain
        protocol = random.choice(['http://'] * 7 + ['https://'] * 3)
        subs = '.'.join([random.choice(SUSPICIOUS_WORDS) for _ in range(random.randint(2, 5))])
        tld = random.choice(TLDs_SUSPICIOUS)
        domain = random_string(random.randint(5, 12)) + tld
        url = f"{protocol}{subs}.{domain}/{random_string(10)}"

    elif strategy == 'suspicious':
        # Known phishing domain patterns
        protocol = random.choice(['http://', 'https://'])
        domain = random.choice(PHISHING_DOMAINS)
        path = '/' + '/'.join(random.choices(SUSPICIOUS_WORDS, k=random.randint(1, 3)))
        url = f"{protocol}{domain}{path}"
        if random.random() < 0.5:
            url += f"?id={random_string(12)}&session={random_string(20)}"

    elif strategy == 'misspell':
        # Misspelled legitimate domains
        misspellings = {
            'google': ['g00gle', 'googie', 'gooogle', 'g0ogle', 'googl3'],
            'amazon': ['amaz0n', 'arnazon', 'amazom', 'amaazon'],
            'facebook': ['faceb00k', 'facebok', 'faceboook', 'faecbook'],
            'paypal': ['paypa1', 'paypai', 'payp4l', 'payypal'],
            'apple': ['app1e', 'appie', 'appl3', 'aapple'],
            'microsoft': ['micr0soft', 'mircosoft', 'microsft', 'mlcrosoft'],
        }
        brand = random.choice(list(misspellings.keys()))
        fake = random.choice(misspellings[brand])
        tld = random.choice(['.com', '.net', '.org'] + TLDs_SUSPICIOUS)
        protocol = random.choice(['http://', 'https://'])
        url = f"{protocol}{fake}{tld}/{random.choice(SUSPICIOUS_WORDS)}"

    elif strategy == 'shortened':
        # URL shorteners hiding malicious content
        shortener = random.choice(SHORTENERS)
        code = random_string(random.randint(5, 8))
        url = f"https://{shortener}/{code}"

    elif strategy == 'encoded':
        # URL with encoded/hex characters
        protocol = 'http://'
        domain = random_string(8) + random.choice(TLDs_SUSPICIOUS)
        hex_part = '%' + '%'.join([format(random.randint(33, 126), '02x') for _ in range(random.randint(3, 8))])
        url = f"{protocol}{domain}/{hex_part}/{random.choice(SUSPICIOUS_WORDS)}"

    elif strategy == 'deep_path':
        # Extremely deep path with many directories
        protocol = random.choice(['http://', 'https://'])
        domain = random_string(10) + random.choice(TLDs_SUSPICIOUS)
        depth = random.randint(4, 8)
        parts = [random.choice(SUSPICIOUS_WORDS + [random_string(6)]) for _ in range(depth)]
        url = f"{protocol}{domain}/{'/'.join(parts)}"

    else:  # mixed
        # Mix of multiple suspicious signals
        protocol = 'http://'
        has_at = random.random() < 0.4
        domain = random.choice(SUSPICIOUS_WORDS) + '-' + random.choice(SUSPICIOUS_WORDS)
        tld = random.choice(TLDs_SUSPICIOUS)
        at_part = f"admin@" if has_at else ""
        url = f"{protocol}{at_part}{domain}{tld}/{random_string(15)}"
        if random.random() < 0.5:
            url += f"?redirect=http://{random_ip()}"

    return url


def extract_features(url):
    """Extract numerical features from a URL string."""
    features = {}

    features['url_length'] = len(url)
    features['n_dots'] = url.count('.')
    features['n_hyphens'] = url.count('-')
    features['n_underscores'] = url.count('_')
    features['n_slashes'] = url.count('/')
    features['n_question_marks'] = url.count('?')
    features['n_equal'] = url.count('=')
    features['n_at'] = url.count('@')
    features['n_ampersand'] = url.count('&')
    features['n_percent'] = url.count('%')
    features['n_digits'] = sum(c.isdigit() for c in url)
    features['n_letters'] = sum(c.isalpha() for c in url)
    features['n_special'] = sum(not c.isalnum() for c in url)

    # Protocol
    features['has_https'] = 1 if url.startswith('https://') else 0

    # IP address detection
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['has_ip'] = 1 if re.search(ip_pattern, url) else 0

    # Domain analysis
    try:
        after_protocol = url.split('://')[-1]
        domain_part = after_protocol.split('/')[0].split('?')[0].split('@')[-1]
        features['domain_length'] = len(domain_part)
        features['n_subdomains'] = domain_part.count('.')
    except Exception:
        features['domain_length'] = 0
        features['n_subdomains'] = 0

    # Path analysis
    try:
        after_domain = url.split('://')[-1]
        path_part = '/'.join(after_domain.split('/')[1:])
        features['path_length'] = len(path_part)
        features['url_depth'] = path_part.count('/') + 1 if path_part else 0
    except Exception:
        features['path_length'] = 0
        features['url_depth'] = 0

    # Suspicious indicators
    url_lower = url.lower()
    features['has_at_symbol'] = 1 if '@' in url else 0
    features['double_slash_redirect'] = 1 if url.count('//') > 1 else 0
    features['prefix_suffix'] = 1 if '-' in url.split('://')[-1].split('/')[0] else 0

    # Suspicious words count
    suspicious_count = sum(1 for word in SUSPICIOUS_WORDS if word in url_lower)
    features['n_suspicious_words'] = suspicious_count

    # URL shortener detection
    shortener_domains = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'ow.ly',
                         'tiny.cc', 'cutt.ly', 'rb.gy']
    features['is_shortened'] = 1 if any(s in url_lower for s in shortener_domains) else 0

    # Suspicious TLD
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.buzz']
    features['suspicious_tld'] = 1 if any(url_lower.endswith(t) or (t + '/') in url_lower for t in suspicious_tlds) else 0

    # Ratio features
    total_chars = len(url) if len(url) > 0 else 1
    features['digit_ratio'] = round(features['n_digits'] / total_chars, 4)
    features['letter_ratio'] = round(features['n_letters'] / total_chars, 4)
    features['special_ratio'] = round(features['n_special'] / total_chars, 4)

    return features


if __name__ == '__main__':
    print('=' * 55)
    print('Malicious URL Detection - Dataset Generator')
    print('=' * 55)

    N_LEGIT = 5000
    N_MALICIOUS = 5000

    print(f'\n[1/3] Generating {N_LEGIT} legitimate URLs...')
    legit_urls = [generate_legit_url() for _ in range(N_LEGIT)]

    print(f'[2/3] Generating {N_MALICIOUS} malicious URLs...')
    malicious_urls = [generate_malicious_url() for _ in range(N_MALICIOUS)]

    print('[3/3] Extracting features from all URLs...')
    rows = []

    for url in legit_urls:
        feat = extract_features(url)
        feat['url'] = url
        feat['label'] = 0  # 0 = Legitimate
        rows.append(feat)

    for url in malicious_urls:
        feat = extract_features(url)
        feat['url'] = url
        feat['label'] = 1  # 1 = Malicious
        rows.append(feat)

    # Add noise: flip labels for ~8% of samples (makes classification harder and
    # creates realistic model accuracy differences between algorithms)
    n_flip = int(len(rows) * 0.08)
    flip_indices = random.sample(range(len(rows)), n_flip)
    for idx in flip_indices:
        rows[idx]['label'] = 1 - rows[idx]['label']
    print(f'  Added noise: flipped {n_flip} labels for realistic difficulty')

    df = pd.DataFrame(rows)

    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Add ID column
    df.insert(0, 'ID', range(1, len(df) + 1))

    # Save
    df.to_csv('malicious_urls.csv', index=False)

    print(f'\nDataset saved: malicious_urls.csv')
    print(f'  Total records: {len(df)}')
    print(f'  Legitimate: {(df["label"] == 0).sum()}')
    print(f'  Malicious:  {(df["label"] == 1).sum()}')
    print(f'  Features:   {len(df.columns) - 3} (excluding ID, url, label)')
    print(f'\nFeature columns:')
    feature_cols = [c for c in df.columns if c not in ['ID', 'url', 'label']]
    for i, col in enumerate(feature_cols, 1):
        print(f'  {i:2d}. {col}')
    print('\nDone!')
