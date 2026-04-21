"""Generate architectural/UML figures for C12 URLShield Malicious URL Detection Report."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Theme colors matching C12 URLShield app
DARK_BG = '#0f0f1a'
DARK_CARD = '#1a1a2e'
ACCENT = '#ffc107'       # Yellow/Gold
TEXT_WHITE = '#ffffff'
TEXT_MUTED = '#a0aec0'
GREEN = '#2ecc71'
RED = '#e74c3c'
BLUE = '#3498db'
ORANGE = '#f39c12'
PURPLE = '#9b59b6'


def save_fig(fig, name):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'  Saved: {name}')


def draw_box(ax, x, y, w, h, text, color=DARK_CARD, text_color=TEXT_WHITE,
             fontsize=9, radius=0.02, edge_color=ACCENT, linewidth=1.5):
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                          facecolor=color, edgecolor=edge_color, linewidth=linewidth)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, fontweight='bold', wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, color=ACCENT, lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))


def draw_label(ax, x, y, text, color=TEXT_MUTED, fontsize=7, ha='center', va='center', fw='normal'):
    ax.text(x, y, text, color=color, fontsize=fontsize, ha=ha, va=va, fontweight=fw)


# ── Fig 1.1: Blacklist vs ML-Based URL Detection Comparison ──────────
def fig_1_1():
    fig, ax = plt.subplots(1, 1, figsize=(11, 5.5))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title('Blacklist vs ML-Based URL Detection', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # --- Left: Blacklist Approach (red) ---
    draw_box(ax, 0.3, 3.0, 4.4, 1.5,
             'Blacklist Approach\n\n'
             '12-48 hr update gap\n'
             'Known URLs only\n'
             'Manual rule updates\n'
             '70-80% coverage',
             color='#3a1520', edge_color=RED, fontsize=9, text_color=RED)

    # Red X icon
    ax.text(2.5, 4.75, 'BLACKLIST', color=RED, fontsize=11, ha='center', fontweight='bold')
    ax.plot(2.5, 4.95, 'X', color=RED, markersize=14, markeredgewidth=3)

    # Bullet details below left box
    left_details = [
        'Static database of known bad URLs',
        'Cannot detect zero-day phishing',
        'Requires constant manual curation',
        'High false-negative rate',
    ]
    for i, item in enumerate(left_details):
        ax.text(2.5, 2.65 - i * 0.45, f'- {item}', color=TEXT_MUTED, fontsize=7, ha='center')

    # --- VS in the middle ---
    ax.text(5.5, 3.75, 'VS', color=ACCENT, fontsize=22, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_CARD, edgecolor=ACCENT, linewidth=2))

    # --- Right: ML-Based Approach (green) ---
    draw_box(ax, 6.3, 3.0, 4.4, 1.5,
             'ML-Based Detection\n\n'
             'Real-time analysis\n'
             'Zero-day detection\n'
             '28 URL features\n'
             '92.35% accuracy',
             color='#153a20', edge_color=GREEN, fontsize=9, text_color=GREEN)

    ax.text(8.5, 4.75, 'URLShield ML', color=GREEN, fontsize=11, ha='center', fontweight='bold')
    ax.plot(8.5, 4.95, 'o', color=GREEN, markersize=10, markeredgewidth=2)

    # Bullet details below right box
    right_details = [
        'Gradient Boosting classifier',
        'Detects unseen phishing patterns',
        'Automated feature extraction',
        'Sub-second prediction latency',
    ]
    for i, item in enumerate(right_details):
        ax.text(8.5, 2.65 - i * 0.45, f'+ {item}', color=TEXT_MUTED, fontsize=7, ha='center')

    save_fig(fig, 'fig_1_1_comparison.png')


# ── Fig 4.1: System Architecture ──────────────────────────────
def fig_4_1():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('System Architecture Diagram', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # ===== OFFLINE TRAINING PHASE (top) =====
    # Phase label
    phase_box = FancyBboxPatch((0.2, 7.85), 13.6, 0.55, boxstyle="round,pad=0.05",
                                facecolor='#2a1a00', edgecolor=ACCENT, linewidth=1.5, linestyle='--')
    ax.add_patch(phase_box)
    ax.text(7.0, 8.12, 'OFFLINE TRAINING PHASE', color=ACCENT, fontsize=12, fontweight='bold', ha='center')

    # generate_dataset.py
    draw_box(ax, 0.4, 6.8, 2.0, 0.75, 'generate_\ndataset.py', color='#1e3a5f', fontsize=8)
    draw_arrow(ax, 2.4, 7.17, 3.0, 7.17)

    # malicious_urls.csv
    draw_box(ax, 3.0, 6.8, 2.0, 0.75, 'malicious_urls.csv\n10,000 URLs\n28 features', color='#34495e', fontsize=7)
    draw_arrow(ax, 5.0, 7.17, 5.6, 7.17)

    # train_model.py
    draw_box(ax, 5.6, 6.8, 2.0, 0.75, 'train_model.py', color='#1e3a5f', fontsize=8)
    draw_arrow(ax, 7.6, 7.17, 8.2, 7.17)

    # 8 ML Models box
    draw_box(ax, 8.2, 6.6, 2.2, 1.15, '8 ML Models\n\nLR, KNN, SVM\nNB, DT, RF\nGB, MLP', color=PURPLE, fontsize=7)
    draw_arrow(ax, 10.4, 7.17, 11.0, 7.17)

    # Best model selection
    draw_box(ax, 11.0, 6.8, 2.6, 0.75, 'Best Model\nGradient Boosting\n92.35% acc', color=GREEN, fontsize=7)

    # Outputs row below
    ax.text(2.0, 6.4, 'Saved Artifacts:', color=ACCENT, fontsize=8, fontweight='bold', ha='center')
    draw_box(ax, 0.4, 5.7, 1.8, 0.55, 'url_model.pkl', color='#34495e', fontsize=7)
    draw_box(ax, 2.5, 5.7, 2.2, 0.55, 'models_info.json', color='#34495e', fontsize=7)
    draw_box(ax, 5.0, 5.7, 2.2, 0.55, '12 Vis PNGs\n(static/vis/)', color='#34495e', fontsize=7)

    draw_arrow(ax, 12.3, 6.8, 1.3, 6.25)
    draw_arrow(ax, 12.3, 6.8, 3.6, 6.25)
    draw_arrow(ax, 9.3, 6.6, 6.1, 6.25)

    # ===== ONLINE SERVING PHASE (middle) =====
    phase_box2 = FancyBboxPatch((0.2, 4.55), 13.6, 0.55, boxstyle="round,pad=0.05",
                                 facecolor='#001a2a', edgecolor=BLUE, linewidth=1.5, linestyle='--')
    ax.add_patch(phase_box2)
    ax.text(7.0, 4.82, 'ONLINE SERVING PHASE', color=BLUE, fontsize=12, fontweight='bold', ha='center')

    # User Browser
    draw_box(ax, 0.4, 3.2, 2.0, 0.9, 'User\nBrowser', color='#34495e', fontsize=9)

    draw_arrow(ax, 2.4, 3.65, 3.2, 3.65)
    ax.text(2.8, 3.9, 'POST /predict', color=TEXT_MUTED, fontsize=6, ha='center')

    # Flask App
    draw_box(ax, 3.2, 3.2, 2.4, 0.9, 'Flask App\nPort 5004\n(app.py)', color='#1e3a5f', fontsize=8)

    draw_arrow(ax, 5.6, 3.65, 6.3, 3.65)
    ax.text(5.95, 3.9, 'URL string', color=TEXT_MUTED, fontsize=6, ha='center')

    # Feature Extraction
    draw_box(ax, 6.3, 3.2, 2.4, 0.9, 'extract_features()\n28 numerical\nfeatures', color=ORANGE, fontsize=8)

    draw_arrow(ax, 8.7, 3.65, 9.4, 3.65)
    ax.text(9.05, 3.9, 'feature vector', color=TEXT_MUTED, fontsize=6, ha='center')

    # Gradient Boosting Predict
    draw_box(ax, 9.4, 3.2, 2.4, 0.9, 'Gradient Boosting\npredict_proba()\nLegit / Malicious', color=GREEN, fontsize=7)

    draw_arrow(ax, 11.8, 3.65, 12.5, 3.65)

    # Result
    draw_box(ax, 12.2, 3.2, 1.4, 0.9, 'Result\n+ Conf %', color=ACCENT, text_color='#000000', fontsize=8)

    # Return arrow
    draw_arrow(ax, 12.9, 3.2, 1.4, 2.6, color=TEXT_MUTED)
    ax.text(7.0, 2.7, 'render result page', color=TEXT_MUTED, fontsize=6, ha='center')

    # ===== DATABASE LAYER (bottom) =====
    phase_box3 = FancyBboxPatch((0.2, 1.55), 13.6, 0.55, boxstyle="round,pad=0.05",
                                 facecolor='#1a0a2a', edgecolor=PURPLE, linewidth=1.5, linestyle='--')
    ax.add_patch(phase_box3)
    ax.text(7.0, 1.82, 'DATABASE LAYER (SQLite)', color=PURPLE, fontsize=12, fontweight='bold', ha='center')

    # Users table
    draw_box(ax, 2.0, 0.3, 3.5, 1.0, 'users table\n\nid | name | username\npassword | is_admin | created_at',
             color='#2a1a3e', edge_color=PURPLE, fontsize=7)

    # Predictions table
    draw_box(ax, 8.0, 0.3, 4.0, 1.0,
             'predictions table\n\nid | user_id (FK) | url | prediction\nconfidence | url_length | has_https\nhas_ip | n_suspicious_words | created_at',
             color='#2a1a3e', edge_color=PURPLE, fontsize=6)

    # Arrow from Flask to DB
    draw_arrow(ax, 4.4, 3.2, 3.75, 1.3, color=PURPLE)
    draw_arrow(ax, 4.4, 3.2, 10.0, 1.3, color=PURPLE)

    save_fig(fig, 'fig_4_1_architecture.png')


# ── Fig 4.2: Use Case Diagram ─────────────────────────────────
def fig_4_2():
    fig, ax = plt.subplots(1, 1, figsize=(13, 9))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Use Case Diagram', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # --- Draw stick figure actor ---
    def draw_actor(ax, x, y, name, color=TEXT_WHITE):
        ax.plot(x, y + 0.35, 'o', color=color, markersize=14)       # Head
        ax.plot([x, x], [y + 0.15, y - 0.2], color=color, lw=2)     # Body
        ax.plot([x - 0.35, x + 0.35], [y + 0.05, y + 0.05], color=color, lw=2)  # Arms
        ax.plot([x, x - 0.25], [y - 0.2, y - 0.55], color=color, lw=2)  # Left leg
        ax.plot([x, x + 0.25], [y - 0.2, y - 0.55], color=color, lw=2)  # Right leg
        ax.text(x, y - 0.8, name, color=color, fontsize=9, ha='center', fontweight='bold')

    # Actors
    draw_actor(ax, 1.0, 7.8, 'Guest', RED)
    draw_actor(ax, 1.0, 5.2, 'Auth User', GREEN)
    draw_actor(ax, 1.0, 2.2, 'Admin', ACCENT)
    draw_actor(ax, 12.0, 4.5, 'ML Pipeline', PURPLE)

    # System boundary
    rect = plt.Rectangle((2.8, 0.3), 7.0, 8.4, fill=False,
                          edgecolor=ACCENT, lw=2, linestyle='--', zorder=0)
    ax.add_patch(rect)
    ax.text(6.3, 8.85, 'URLShield System', color=ACCENT, fontsize=12, ha='center', fontweight='bold')

    # --- Guest Use Cases ---
    guest_cases = ['Login', 'Register']
    for i, uc in enumerate(guest_cases):
        cy = 8.1 - i * 0.8
        draw_box(ax, 3.3, cy - 0.22, 2.5, 0.44, uc, color='#3a1520', edge_color=RED, fontsize=9)
        draw_arrow(ax, 1.5, 7.8 + 0.1, 3.3, cy, color=RED)

    # --- Auth User Use Cases ---
    auth_cases = ['Predict URL', 'View Result', 'View History',
                  'Visualize EDA', 'Model Dashboard', 'About', 'Logout']
    for i, uc in enumerate(auth_cases):
        cy = 7.0 - i * 0.7
        draw_box(ax, 3.3, cy - 0.22, 2.5, 0.44, uc, color='#153a20', edge_color=GREEN, fontsize=8)
        draw_arrow(ax, 1.5, 5.2 + 0.1, 3.3, cy, color=GREEN)

    # --- Admin Use Cases (extends Auth + platform stats) ---
    admin_cases = ['All Auth User\nFunctions', 'Platform Stats']
    for i, uc in enumerate(admin_cases):
        cy = 2.4 - i * 0.85
        draw_box(ax, 3.3, cy - 0.22, 2.5, 0.44, uc, color='#2a1a00', edge_color=ACCENT, fontsize=8)
        draw_arrow(ax, 1.5, 2.2 + 0.1, 3.3, cy, color=ACCENT)

    # <<extends>> arrow from Admin's "All Auth User Functions" to Auth cases
    ax.annotate('', xy=(4.55, 3.08), xytext=(4.55, 2.18 + 0.22),
                arrowprops=dict(arrowstyle='->', color=TEXT_MUTED, lw=1, linestyle='--'))
    ax.text(4.95, 2.8, '<<extends>>', color=TEXT_MUTED, fontsize=6, fontstyle='italic')

    # --- ML Pipeline Use Cases ---
    ml_cases = ['Generate Dataset\n(10K URLs)', 'Train 8 Models', 'Generate 12\nCharts', 'Save Best Model\n(Gradient Boosting)']
    for i, uc in enumerate(ml_cases):
        cy = 6.6 - i * 1.0
        draw_box(ax, 7.3, cy - 0.27, 2.2, 0.54, uc, color='#1a0a2a', edge_color=PURPLE, fontsize=7)
        draw_arrow(ax, 11.5, 4.5 + 0.1, 9.5, cy, color=PURPLE)

    save_fig(fig, 'fig_4_2_usecase.png')


# ── Fig 4.3: Class Diagram ────────────────────────────────────
def fig_4_3():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8.5))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.set_title('Class Diagram', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    classes = [
        # (x, y, w, h, name, attributes, methods, header_color)
        (0.3, 5.3, 3.2, 2.6,
         'FeatureExtractor',
         'url: str\nSUSPICIOUS_WORDS: list[19]\nSHORTENERS: list[6]\nSUSPICIOUS_TLDS: list[10]',
         'extract_features(url) -> dict\n  -> 28 numerical features\n  url_length, n_dots, has_ip...\n  digit_ratio, letter_ratio...',
         ORANGE),

        (4.0, 5.3, 3.2, 2.6,
         'ModelTrainer',
         'models: dict[8]\nX_train, X_test: array\ny_train, y_test: array\nbest_model: Classifier',
         'load_and_prepare() -> df, X, y\ntrain_models() -> results\nevaluate() -> metrics\nsave_best() -> url_model.pkl',
         BLUE),

        (7.7, 5.3, 3.0, 2.6,
         'FlaskApp',
         'app: Flask\nmodel: pkl\nmodels_info: json\nsecret_key: str',
         'index() -> redirect\npredict() -> result\nhome() -> dashboard\nhistory() -> list\nvisualize() / dashboard()',
         GREEN),

        (11.2, 5.3, 2.5, 2.6,
         'SQLiteDB',
         'db_path: url_detect.db\nconn: Connection\ncursor: Cursor',
         'init_db() -> tables\nget_db() -> connection\nexecute(sql) -> rows\ncommit() / close()',
         PURPLE),

        (0.3, 1.5, 3.2, 2.6,
         'UserAuth',
         'session: Flask.session\nuser_id: int\nusername: str\nis_admin: bool',
         'register(name, user, pwd)\nlogin(user, pwd) -> bool\nlogout() -> clear session\ncheck_password_hash()',
         RED),

        (4.0, 1.5, 3.2, 2.6,
         'PredictionEngine',
         'model: GradientBoosting\nFEATURE_ORDER: list[28]\nproba: array\npred_class: int',
         'predict_url(url) -> (pred, conf)\nextract_features(url) -> dict\npredict_proba() -> array\nmap_class() -> Legit/Malicious',
         ACCENT),

        (7.7, 1.5, 3.0, 2.6,
         'DatasetGenerator',
         'N_LEGIT: 5000\nN_MALICIOUS: 5000\nLEGIT_DOMAINS: list[50]\nSUSPICIOUS_WORDS: list[19]',
         'generate_legit_url()\ngenerate_malicious_url()\nextract_features(url)\nsave_csv() -> malicious_urls.csv',
         ORANGE),

        (11.2, 1.5, 2.5, 2.6,
         'HistoryTracker',
         'user_id: int\npredictions: list\nrecent: list[5]',
         'get_history(user_id)\nstore_prediction()\nget_stats() -> dict\nadmin_stats() -> dict',
         BLUE),
    ]

    for x, y, w, h, name, attrs, methods, hdr_color in classes:
        header_h = 0.45
        attr_h = (h - header_h) * 0.45
        method_h = (h - header_h) * 0.55

        # Header
        draw_box(ax, x, y + h - header_h, w, header_h, name,
                 color=hdr_color, fontsize=8, text_color=TEXT_WHITE)

        # Attributes section
        attr_box = FancyBboxPatch((x, y + method_h), w, attr_h,
                                   boxstyle="round,pad=0.02",
                                   facecolor=DARK_CARD, edgecolor=hdr_color, linewidth=1)
        ax.add_patch(attr_box)
        ax.text(x + 0.1, y + method_h + attr_h - 0.12, attrs,
                color=TEXT_MUTED, fontsize=5.5, va='top', family='monospace')

        # Methods section
        method_box = FancyBboxPatch((x, y), w, method_h,
                                     boxstyle="round,pad=0.02",
                                     facecolor=DARK_CARD, edgecolor=hdr_color, linewidth=1)
        ax.add_patch(method_box)
        ax.text(x + 0.1, y + method_h - 0.12, methods,
                color=GREEN, fontsize=5.5, va='top', family='monospace')

    # Relationships (arrows between classes)
    # FeatureExtractor -> PredictionEngine
    draw_arrow(ax, 1.9, 5.3, 5.6, 4.1, color=ORANGE)
    ax.text(3.5, 4.85, 'uses', color=TEXT_MUTED, fontsize=6, fontstyle='italic')

    # ModelTrainer -> PredictionEngine
    draw_arrow(ax, 5.6, 5.3, 5.6, 4.1, color=BLUE)

    # FlaskApp -> SQLiteDB
    draw_arrow(ax, 10.7, 6.6, 11.2, 6.6, color=GREEN)

    # FlaskApp -> UserAuth
    draw_arrow(ax, 8.2, 5.3, 1.9, 4.1, color=GREEN)
    ax.text(4.8, 4.85, 'authenticates', color=TEXT_MUTED, fontsize=6, fontstyle='italic')

    # FlaskApp -> PredictionEngine
    draw_arrow(ax, 9.2, 5.3, 5.6, 4.1, color=GREEN)

    # DatasetGenerator -> ModelTrainer
    draw_arrow(ax, 9.2, 4.1, 5.6, 5.3, color=ORANGE)

    save_fig(fig, 'fig_4_3_class.png')


# ── Fig 4.4: Sequence Diagram ─────────────────────────────────
def fig_4_4():
    fig, ax = plt.subplots(1, 1, figsize=(13, 8))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Sequence Diagram -- URL Prediction Workflow', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # Lifelines
    actors = ['User', 'Flask App', 'FeatureExtractor', 'GradientBoosting', 'SQLite']
    positions = [1.5, 3.8, 6.3, 8.8, 11.2]
    colors = [TEXT_WHITE, BLUE, ORANGE, GREEN, PURPLE]

    for pos, name, clr in zip(positions, actors, colors):
        draw_box(ax, pos - 0.8, 7.2, 1.6, 0.55, name, color=DARK_CARD, edge_color=clr, fontsize=8)
        ax.plot([pos, pos], [0.5, 7.2], color=TEXT_MUTED, lw=1, linestyle='--', alpha=0.5)
        # Bottom box
        draw_box(ax, pos - 0.5, 0.2, 1.0, 0.3, '', color=DARK_CARD, edge_color=clr, fontsize=6)

    # Activation boxes (thin rectangles on lifelines)
    for pos, y_top, y_bot, clr in [
        (3.8, 6.8, 1.2, BLUE),
        (6.3, 6.0, 4.8, ORANGE),
        (8.8, 4.5, 3.2, GREEN),
        (11.2, 2.8, 1.8, PURPLE),
    ]:
        act = FancyBboxPatch((pos - 0.12, y_bot), 0.24, y_top - y_bot,
                              boxstyle="round,pad=0.01",
                              facecolor=clr, edgecolor=clr, linewidth=1, alpha=0.25)
        ax.add_patch(act)

    # Messages (x_from, x_to, y, label)
    messages = [
        (1.5, 3.8, 6.8, '1. POST /predict (url)', TEXT_WHITE),
        (3.8, 6.3, 6.1, '2. extract_features(url)', ORANGE),
        (6.3, 3.8, 5.5, '3. return 28 features (dict)', ORANGE),
        (3.8, 8.8, 4.6, '4. model.predict_proba(features)', GREEN),
        (8.8, 3.8, 4.0, '5. return [legit_prob, mal_prob]', GREEN),
        (3.8, 3.8, 3.5, '6. map to Legitimate / Malicious', BLUE),
        (3.8, 11.2, 2.8, '7. INSERT INTO predictions (...)', PURPLE),
        (11.2, 3.8, 2.2, '8. OK (committed)', PURPLE),
        (3.8, 1.5, 1.5, '9. render predict.html + result', TEXT_WHITE),
    ]

    for x1, x2, y, label, clr in messages:
        if x1 == x2:
            # Self-message (curved)
            ax.annotate('', xy=(x1 + 1.0, y - 0.25), xytext=(x1 + 0.12, y),
                        arrowprops=dict(arrowstyle='->', color=clr, lw=1.5,
                                       connectionstyle='arc3,rad=-0.3'))
            ax.text(x1 + 0.7, y - 0.05, label, color=clr, fontsize=6.5, ha='left')
        else:
            draw_arrow(ax, x1, y, x2, y, color=clr)
            mid = (x1 + x2) / 2
            ax.text(mid, y + 0.18, label, color=clr, fontsize=6.5, ha='center')

    save_fig(fig, 'fig_4_4_sequence.png')


# ── Fig 4.5: Activity Diagram ─────────────────────────────────
def fig_4_5():
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Activity Diagram', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # Start node (filled circle)
    ax.plot(6.0, 9.5, 'o', color=ACCENT, markersize=15, markeredgewidth=2)
    ax.text(6.0, 9.15, 'Start', color=TEXT_MUTED, fontsize=7, ha='center')

    # Main flow activities
    draw_box(ax, 4.5, 8.4, 3.0, 0.5, 'Open Application', color=DARK_CARD, fontsize=9)
    draw_arrow(ax, 6.0, 9.35, 6.0, 8.9)

    # Decision diamond for Login/Register
    diamond_x, diamond_y = 6.0, 7.65
    diamond = plt.Polygon([[diamond_x, diamond_y + 0.35],
                            [diamond_x + 0.7, diamond_y],
                            [diamond_x, diamond_y - 0.35],
                            [diamond_x - 0.7, diamond_y]],
                           facecolor=ACCENT, edgecolor=ACCENT, linewidth=1.5, alpha=0.3)
    ax.add_patch(diamond)
    ax.text(diamond_x, diamond_y, 'Auth?', color=ACCENT, fontsize=8, ha='center', va='center', fontweight='bold')
    draw_arrow(ax, 6.0, 8.4, 6.0, 8.0)

    # Login path (right)
    draw_box(ax, 8.0, 7.35, 2.0, 0.5, 'Login', color='#153a20', edge_color=GREEN, fontsize=9)
    draw_arrow(ax, 6.7, 7.65, 8.0, 7.6)
    ax.text(7.3, 7.85, 'existing user', color=TEXT_MUTED, fontsize=6, ha='center')

    # Register path (left)
    draw_box(ax, 2.0, 7.35, 2.0, 0.5, 'Register', color='#1e3a5f', edge_color=BLUE, fontsize=9)
    draw_arrow(ax, 5.3, 7.65, 4.0, 7.6)
    ax.text(4.7, 7.85, 'new user', color=TEXT_MUTED, fontsize=6, ha='center')

    # Both converge to Home Dashboard
    draw_box(ax, 4.5, 6.2, 3.0, 0.5, 'Home Dashboard', color=DARK_CARD, fontsize=9)
    draw_arrow(ax, 9.0, 7.35, 9.0, 6.55)
    ax.annotate('', xy=(7.5, 6.45), xytext=(9.0, 6.45),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))
    draw_arrow(ax, 3.0, 7.35, 3.0, 6.55)
    ax.annotate('', xy=(4.5, 6.45), xytext=(3.0, 6.45),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    # Branch diamond from Home
    branch_x, branch_y = 6.0, 5.35
    branch = plt.Polygon([[branch_x, branch_y + 0.35],
                           [branch_x + 0.7, branch_y],
                           [branch_x, branch_y - 0.35],
                           [branch_x - 0.7, branch_y]],
                          facecolor=ACCENT, edgecolor=ACCENT, linewidth=1.5, alpha=0.3)
    ax.add_patch(branch)
    ax.text(branch_x, branch_y, 'Action?', color=ACCENT, fontsize=8, ha='center', va='center', fontweight='bold')
    draw_arrow(ax, 6.0, 6.2, 6.0, 5.7)

    # Branch activities
    # Predict URL flow (center-left)
    draw_box(ax, 0.5, 4.2, 2.3, 0.5, 'Enter URL', color=DARK_CARD, fontsize=8)
    draw_arrow(ax, 5.3, 5.35, 2.3, 4.7)

    draw_box(ax, 0.5, 3.3, 2.3, 0.5, 'Extract 28\nFeatures', color=ORANGE, fontsize=8)
    draw_arrow(ax, 1.65, 4.2, 1.65, 3.8)

    draw_box(ax, 0.5, 2.4, 2.3, 0.5, 'Classify URL', color=GREEN, fontsize=8)
    draw_arrow(ax, 1.65, 3.3, 1.65, 2.9)

    # Result split
    draw_box(ax, 0.0, 1.4, 1.4, 0.5, 'Legitimate', color='#153a20', edge_color=GREEN, fontsize=7, text_color=GREEN)
    draw_box(ax, 1.9, 1.4, 1.4, 0.5, 'Malicious', color='#3a1520', edge_color=RED, fontsize=7, text_color=RED)
    draw_arrow(ax, 1.2, 2.4, 0.7, 1.9)
    draw_arrow(ax, 2.1, 2.4, 2.6, 1.9)

    # History (center-right offset)
    draw_box(ax, 4.0, 4.2, 2.0, 0.5, 'View History', color=DARK_CARD, fontsize=8)
    draw_arrow(ax, 5.6, 5.0, 5.0, 4.7)

    # Visualize
    draw_box(ax, 6.5, 4.2, 2.0, 0.5, 'Visualize EDA', color=DARK_CARD, fontsize=8)
    draw_arrow(ax, 6.3, 5.0, 7.5, 4.7)

    # Dashboard
    draw_box(ax, 9.0, 4.2, 2.3, 0.5, 'Model Dashboard', color=DARK_CARD, fontsize=8)
    draw_arrow(ax, 6.7, 5.35, 9.0, 4.5)

    # About
    draw_box(ax, 9.0, 3.3, 2.3, 0.5, 'About', color=DARK_CARD, fontsize=8)
    draw_arrow(ax, 6.7, 5.2, 10.15, 3.8)

    # All converge to Logout
    draw_box(ax, 4.5, 0.5, 3.0, 0.5, 'Logout', color='#3a1520', edge_color=RED, fontsize=9)

    # Converging arrows to logout
    draw_arrow(ax, 0.7, 1.4, 4.5, 0.85)
    draw_arrow(ax, 2.6, 1.4, 4.5, 0.75)
    draw_arrow(ax, 5.0, 4.2, 5.5, 1.0)
    draw_arrow(ax, 7.5, 4.2, 6.5, 1.0)
    draw_arrow(ax, 10.15, 4.2, 7.5, 0.85)
    draw_arrow(ax, 10.15, 3.3, 7.5, 0.75)

    # End node (bullseye)
    ax.plot(6.0, 0.05, 'o', color=ACCENT, markersize=15, markeredgewidth=2)
    ax.plot(6.0, 0.05, 'o', color=ACCENT, markersize=8, markeredgewidth=0)
    draw_arrow(ax, 6.0, 0.5, 6.0, 0.2)

    save_fig(fig, 'fig_4_5_activity.png')


# ── Fig 4.6: UI Wireframe ─────────────────────────────────────
def fig_4_6():
    fig, ax = plt.subplots(1, 1, figsize=(12, 7.5))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor('#0f0f1a')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')
    ax.set_title('UI Wireframe -- URL Detection Page', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # ── Navbar ──
    navbar = FancyBboxPatch((0.3, 6.7), 11.4, 0.55, boxstyle="round,pad=0.03",
                             facecolor=DARK_CARD, edgecolor=ACCENT, linewidth=1.5)
    ax.add_patch(navbar)
    ax.text(0.7, 6.97, 'URLShield', color=ACCENT, fontsize=12, fontweight='bold')
    ax.plot(0.55, 6.97, 's', color=ACCENT, markersize=8)  # Shield icon

    nav_links = ['Home', 'Predict', 'History', 'Visualize', 'Dashboard', 'About', 'Logout']
    for i, link in enumerate(nav_links):
        clr = ACCENT if link == 'Predict' else TEXT_MUTED
        ax.text(4.0 + i * 1.2, 6.97, link, color=clr, fontsize=7, ha='center', va='center')

    # ── Left Panel: URL Input ──
    left_panel = FancyBboxPatch((0.3, 2.8), 5.2, 3.6, boxstyle="round,pad=0.04",
                                 facecolor=DARK_CARD, edgecolor='#2a2a4e', linewidth=1.5)
    ax.add_patch(left_panel)

    ax.text(2.9, 6.15, 'Analyze URL', color=TEXT_WHITE, fontsize=11, ha='center', fontweight='bold')
    ax.text(2.9, 5.85, 'Enter a URL to check if it is safe or malicious',
            color=TEXT_MUTED, fontsize=7, ha='center')

    # URL input field
    input_box = FancyBboxPatch((0.6, 5.2), 4.6, 0.4, boxstyle="round,pad=0.03",
                                facecolor='#252545', edgecolor='#3a3a5e', linewidth=1)
    ax.add_patch(input_box)
    ax.text(0.85, 5.4, 'https://example.com/path?param=value', color=TEXT_MUTED, fontsize=7, va='center')

    # Analyze button
    draw_box(ax, 1.5, 4.55, 2.8, 0.45, 'Analyze URL', color=ACCENT, text_color='#000000', fontsize=10)

    # Quick test buttons
    ax.text(2.9, 4.25, 'Quick Test URLs:', color=TEXT_MUTED, fontsize=7, ha='center')
    quick_tests = [
        ('https://google.com', GREEN, 0.6, 3.75),
        ('https://github.com/docs', GREEN, 2.9, 3.75),
        ('http://192.168.1.1/login/verify', RED, 0.6, 3.3),
        ('http://g00gle.tk/account', RED, 2.9, 3.3),
    ]
    for text, clr, x, y in quick_tests:
        btn = FancyBboxPatch((x, y), 2.1, 0.3, boxstyle="round,pad=0.02",
                              facecolor=DARK_BG, edgecolor=clr, linewidth=0.8)
        ax.add_patch(btn)
        ax.text(x + 1.05, y + 0.15, text, color=clr, fontsize=5.5, ha='center', va='center')

    # ── Right Panel: Result Cards ──
    right_panel = FancyBboxPatch((5.8, 2.8), 5.9, 3.6, boxstyle="round,pad=0.04",
                                  facecolor=DARK_CARD, edgecolor='#2a2a4e', linewidth=1.5)
    ax.add_patch(right_panel)

    ax.text(8.75, 6.15, 'Detection Result', color=TEXT_WHITE, fontsize=11, ha='center', fontweight='bold')

    # Legitimate card (green)
    legit_card = FancyBboxPatch((6.0, 4.8), 2.5, 1.1, boxstyle="round,pad=0.04",
                                 facecolor='#153a20', edgecolor=GREEN, linewidth=2)
    ax.add_patch(legit_card)
    ax.plot(6.5, 5.55, 'o', color=GREEN, markersize=18, markeredgewidth=2)
    ax.text(6.5, 5.55, '+', color=GREEN, fontsize=14, ha='center', va='center', fontweight='bold')
    ax.text(7.6, 5.55, 'Legitimate', color=GREEN, fontsize=10, fontweight='bold', va='center')
    ax.text(7.6, 5.2, 'Confidence: 96.8%', color=TEXT_MUTED, fontsize=7, va='center')

    # Malicious card (red)
    mal_card = FancyBboxPatch((9.0, 4.8), 2.5, 1.1, boxstyle="round,pad=0.04",
                               facecolor='#3a1520', edgecolor=RED, linewidth=2)
    ax.add_patch(mal_card)
    ax.plot(9.5, 5.55, 'o', color=RED, markersize=18, markeredgewidth=2)
    ax.text(9.5, 5.55, 'X', color=RED, fontsize=12, ha='center', va='center', fontweight='bold')
    ax.text(10.5, 5.55, 'Malicious', color=RED, fontsize=10, fontweight='bold', va='center')
    ax.text(10.5, 5.2, 'Confidence: 89.3%', color=TEXT_MUTED, fontsize=7, va='center')

    # Feature table below result
    ax.text(8.75, 4.5, 'Extracted Features', color=ACCENT, fontsize=9, ha='center', fontweight='bold')

    feature_table = [
        ('URL Length', '47'),
        ('Domain Length', '12'),
        ('Has HTTPS', 'Yes'),
        ('Has IP', 'No'),
        ('Suspicious Words', '0'),
        ('URL Depth', '2'),
        ('Special Chars', '8'),
        ('Digit Ratio', '3.2%'),
    ]
    # Table header
    table_y = 4.2
    hdr = FancyBboxPatch((6.2, table_y - 0.05), 5.2, 0.25, boxstyle="round,pad=0.01",
                          facecolor='#252545', edgecolor='#3a3a5e', linewidth=0.5)
    ax.add_patch(hdr)
    ax.text(7.5, table_y + 0.07, 'Feature', color=ACCENT, fontsize=6, ha='center', fontweight='bold')
    ax.text(10.2, table_y + 0.07, 'Value', color=ACCENT, fontsize=6, ha='center', fontweight='bold')

    for i, (feat, val) in enumerate(feature_table):
        row_y = table_y - 0.28 - i * 0.22
        bg_color = '#1a1a2e' if i % 2 == 0 else '#151530'
        row = FancyBboxPatch((6.2, row_y - 0.03), 5.2, 0.2, boxstyle="round,pad=0.01",
                              facecolor=bg_color, edgecolor='#2a2a4e', linewidth=0.3)
        ax.add_patch(row)
        ax.text(7.5, row_y + 0.07, feat, color=TEXT_MUTED, fontsize=5.5, ha='center')
        ax.text(10.2, row_y + 0.07, val, color=TEXT_WHITE, fontsize=5.5, ha='center')

    # ── Bottom section hint ──
    footer = FancyBboxPatch((0.3, 2.3), 11.4, 0.35, boxstyle="round,pad=0.02",
                             facecolor=DARK_CARD, edgecolor='#2a2a4e', linewidth=0.8)
    ax.add_patch(footer)
    ax.text(6.0, 2.47, 'URLShield uses Gradient Boosting with 28 features for real-time malicious URL detection',
            color=TEXT_MUTED, fontsize=7, ha='center')

    save_fig(fig, 'fig_4_6_wireframe.png')


# ── Fig 4.7: ER / Database Schema Diagram ─────────────────────
def fig_4_7():
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.set_title('ER / Database Schema Diagram', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    # ── users table ──
    ux, uy, uw, uh = 0.8, 1.0, 4.0, 4.5

    # Table name header
    draw_box(ax, ux, uy + uh - 0.55, uw, 0.55, 'users', color=BLUE, fontsize=11)

    # Table body
    table_bg = FancyBboxPatch((ux, uy), uw, uh - 0.55, boxstyle="round,pad=0.03",
                               facecolor=DARK_CARD, edgecolor=BLUE, linewidth=1.5)
    ax.add_patch(table_bg)

    user_fields = [
        ('id', 'INTEGER', 'PK, AUTO'),
        ('name', 'TEXT', 'NOT NULL'),
        ('username', 'TEXT', 'UNIQUE, NOT NULL'),
        ('password', 'TEXT', 'NOT NULL'),
        ('is_admin', 'INTEGER', 'DEFAULT 0'),
        ('created_at', 'TEXT', 'DEFAULT NOW'),
    ]

    for i, (fname, ftype, constraint) in enumerate(user_fields):
        row_y = uy + uh - 0.55 - 0.12 - i * 0.55
        # PK gets special highlight
        if 'PK' in constraint:
            key_bg = FancyBboxPatch((ux + 0.05, row_y - 0.15), uw - 0.1, 0.45,
                                     boxstyle="round,pad=0.01",
                                     facecolor='#1e3a5f', edgecolor=BLUE, linewidth=0.5)
            ax.add_patch(key_bg)
            ax.text(ux + 0.2, row_y + 0.07, 'PK', color=ACCENT, fontsize=6, fontweight='bold')

        ax.text(ux + 0.6, row_y + 0.07, fname, color=TEXT_WHITE, fontsize=8, fontweight='bold')
        ax.text(ux + 2.0, row_y + 0.07, ftype, color=ORANGE, fontsize=7)
        ax.text(ux + 3.2, row_y + 0.07, constraint, color=TEXT_MUTED, fontsize=6)

        if i < len(user_fields) - 1:
            ax.plot([ux + 0.1, ux + uw - 0.1], [row_y - 0.18, row_y - 0.18],
                    color='#2a2a4e', lw=0.5)

    # ── predictions table ──
    px, py, pw, ph = 6.5, 0.5, 5.0, 5.5

    # Table name header
    draw_box(ax, px, py + ph - 0.55, pw, 0.55, 'predictions', color=PURPLE, fontsize=11)

    # Table body
    pred_bg = FancyBboxPatch((px, py), pw, ph - 0.55, boxstyle="round,pad=0.03",
                              facecolor=DARK_CARD, edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(pred_bg)

    pred_fields = [
        ('id', 'INTEGER', 'PK, AUTO'),
        ('user_id', 'INTEGER', 'FK -> users.id'),
        ('url', 'TEXT', 'NOT NULL'),
        ('prediction', 'TEXT', 'NOT NULL'),
        ('confidence', 'REAL', 'NOT NULL'),
        ('url_length', 'INTEGER', ''),
        ('has_https', 'INTEGER', ''),
        ('has_ip', 'INTEGER', ''),
        ('n_suspicious_words', 'INTEGER', ''),
        ('created_at', 'TEXT', 'DEFAULT NOW'),
    ]

    for i, (fname, ftype, constraint) in enumerate(pred_fields):
        row_y = py + ph - 0.55 - 0.12 - i * 0.48
        if 'PK' in constraint:
            key_bg = FancyBboxPatch((px + 0.05, row_y - 0.12), pw - 0.1, 0.4,
                                     boxstyle="round,pad=0.01",
                                     facecolor='#2a1a3e', edgecolor=PURPLE, linewidth=0.5)
            ax.add_patch(key_bg)
            ax.text(px + 0.2, row_y + 0.07, 'PK', color=ACCENT, fontsize=6, fontweight='bold')
        elif 'FK' in constraint:
            fk_bg = FancyBboxPatch((px + 0.05, row_y - 0.12), pw - 0.1, 0.4,
                                    boxstyle="round,pad=0.01",
                                    facecolor='#1a2a1e', edgecolor=GREEN, linewidth=0.5)
            ax.add_patch(fk_bg)
            ax.text(px + 0.2, row_y + 0.07, 'FK', color=GREEN, fontsize=6, fontweight='bold')

        ax.text(px + 0.6, row_y + 0.07, fname, color=TEXT_WHITE, fontsize=7.5, fontweight='bold')
        ax.text(px + 2.4, row_y + 0.07, ftype, color=ORANGE, fontsize=6.5)
        ax.text(px + 3.6, row_y + 0.07, constraint, color=TEXT_MUTED, fontsize=5.5)

        if i < len(pred_fields) - 1:
            ax.plot([px + 0.1, px + pw - 0.1], [row_y - 0.15, row_y - 0.15],
                    color='#2a2a4e', lw=0.5)

    # ── Relationship arrow: users 1 ---< N predictions ──
    # Draw from users.id to predictions.user_id
    # Arrow from right side of users table to left side of predictions table
    arrow_y = 4.2
    ax.annotate('', xy=(px, arrow_y), xytext=(ux + uw, arrow_y),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2.5))

    # Cardinality labels
    ax.text(ux + uw + 0.15, arrow_y + 0.2, '1', color=ACCENT, fontsize=12, fontweight='bold')
    ax.text(px - 0.35, arrow_y + 0.2, 'N', color=ACCENT, fontsize=12, fontweight='bold')
    ax.text((ux + uw + px) / 2, arrow_y + 0.3, 'has many', color=TEXT_MUTED, fontsize=8,
            ha='center', fontstyle='italic')

    save_fig(fig, 'fig_4_7_er_diagram.png')


# ── Fig 5.1: Development Phases ───────────────────────────────
def fig_5_1():
    fig, ax = plt.subplots(1, 1, figsize=(12, 5.5))
    fig.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title('Development Phases', color=TEXT_WHITE,
                 fontsize=15, fontweight='bold', pad=18)

    phases = [
        ('Phase 1\nDataset\nEngineering', BLUE,
         'generate_dataset.py\n10,000 URLs (50/50 split)\n28 features extracted\n8% noise injection'),
        ('Phase 2\nML Pipeline', GREEN,
         'train_model.py\n8 classifiers trained\n10 EDA visualizations\nBest: Gradient Boosting'),
        ('Phase 3\nWeb\nApplication', ORANGE,
         'Flask app (app.py)\n7 routes, SQLite DB\nUser auth + sessions\nReal-time prediction'),
        ('Phase 4\nTesting &\nDocker', PURPLE,
         'Unit + integration tests\nDocker containerization\nModel performance eval\nDocumentation'),
    ]

    box_w = 2.2
    box_h = 1.6
    gap = 0.6
    start_x = 0.5

    for i, (title, color, details) in enumerate(phases):
        x = start_x + i * (box_w + gap)
        # Phase number circle
        ax.plot(x + box_w / 2, 4.8, 'o', color=color, markersize=22, markeredgewidth=2)
        ax.text(x + box_w / 2, 4.8, str(i + 1), color=TEXT_WHITE, fontsize=12,
                ha='center', va='center', fontweight='bold')

        # Phase title box
        draw_box(ax, x, 3.2, box_w, box_h, title, color=color, fontsize=10)

        # Arrow between phases
        if i > 0:
            prev_x = start_x + (i - 1) * (box_w + gap) + box_w
            draw_arrow(ax, prev_x, 4.0, x, 4.0, color=ACCENT, lw=2)

        # Details below
        detail_lines = details.split('\n')
        for j, line in enumerate(detail_lines):
            ax.text(x + box_w / 2, 2.9 - j * 0.35, line,
                    color=TEXT_MUTED, fontsize=7, ha='center')

    # Progress bar at the bottom
    bar_y = 0.8
    bar_h = 0.3
    total_w = 4 * box_w + 3 * gap
    for i, (_, color, _) in enumerate(phases):
        seg_x = start_x + i * (total_w / 4)
        seg_w = total_w / 4
        seg = FancyBboxPatch((seg_x, bar_y), seg_w - 0.05, bar_h,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor=color, linewidth=1, alpha=0.6)
        ax.add_patch(seg)
        ax.text(seg_x + seg_w / 2, bar_y + bar_h / 2,
                f'Phase {i + 1}', color=TEXT_WHITE, fontsize=7,
                ha='center', va='center', fontweight='bold')

    ax.text(start_x + total_w / 2, 0.5, 'Project Timeline',
            color=TEXT_MUTED, fontsize=8, ha='center')

    save_fig(fig, 'fig_5_1_phases.png')


# ── Generate all figures ───────────────────────────────────────
if __name__ == '__main__':
    print('Generating C12 URLShield Malicious URL Detection Figures...\n')
    fig_1_1()
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    fig_4_5()
    fig_4_6()
    fig_4_7()
    fig_5_1()
    print(f'\nAll 9 figures saved to: {FIGURES_DIR}')
