"""
Generate dark-themed matplotlib figures for the Car Insurance Claim
Amount Prediction project report.

Produces 7 publication-quality figures saved to figures/ at 150 DPI.

Usage:
    python generate_figures.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
BG_COLOR = '#1a1a2e'
TEXT_COLOR = 'white'
RED = '#e74c3c'
BLUE = '#3498db'
GREEN = '#2ecc71'
ORANGE = '#f39c12'
ACCENT_COLORS = [RED, BLUE, GREEN, ORANGE]
BOX_FACE = '#16213e'
BOX_EDGE = '#0f3460'
ARROW_COLOR = '#e94560'
FONT_SIZE = 12
DPI = 150

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(OUT_DIR, exist_ok=True)

plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': BG_COLOR,
    'savefig.facecolor': BG_COLOR,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
    'font.size': FONT_SIZE,
    'axes.edgecolor': '#444466',
    'grid.color': '#2a2a4a',
})


# ===================================================================
# Helper utilities
# ===================================================================

def _rounded_box(ax, x, y, w, h, text, facecolor=BOX_FACE,
                 edgecolor=BOX_EDGE, fontsize=11, text_color=TEXT_COLOR,
                 linewidth=2, pad=0.15):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', zorder=3,
            wrap=True)
    return box


def _arrow(ax, x1, y1, x2, y2, color=ARROW_COLOR, lw=2,
           arrowstyle='->', mutation_scale=18):
    """Draw a curved arrow between two points."""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=arrowstyle,
        color=color, linewidth=lw, mutation_scale=mutation_scale,
        connectionstyle='arc3,rad=0',
        zorder=1,
    )
    ax.add_patch(arrow)
    return arrow


def _save(fig, name):
    """Save figure and close."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'  Saved {path}')


# ===================================================================
# 1. System Architecture Diagram
# ===================================================================

def fig_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.suptitle('System Architecture Diagram', fontsize=18,
                 fontweight='bold', color=TEXT_COLOR, y=0.96)

    # --- Boxes ---
    # User
    _rounded_box(ax, 1.5, 8, 2.2, 1.2, 'User\n(Browser)',
                 facecolor='#1b2838', edgecolor=BLUE, fontsize=12)

    # Flask Web App
    _rounded_box(ax, 5.5, 8, 3.0, 1.2,
                 'Flask Web App\n(Port 5002)',
                 facecolor='#1b2838', edgecolor=GREEN, fontsize=12)

    # ML Prediction Engine
    _rounded_box(ax, 10.5, 8, 3.0, 1.2,
                 'ML Prediction Engine\n(Gradient Boosting)',
                 facecolor='#1b2838', edgecolor=RED, fontsize=12)

    # SQLite DB
    _rounded_box(ax, 3.5, 4.5, 2.8, 1.2,
                 'SQLite Database\n(users, predictions)',
                 facecolor='#1b2838', edgecolor=ORANGE, fontsize=11)

    # EDA Visualization Module
    _rounded_box(ax, 7.5, 4.5, 3.2, 1.2,
                 'EDA Visualization\n(matplotlib / seaborn)',
                 facecolor='#1b2838', edgecolor=BLUE, fontsize=11)

    # Chart.js Dashboard
    _rounded_box(ax, 11.5, 4.5, 2.4, 1.2,
                 'Chart.js\nDashboard',
                 facecolor='#1b2838', edgecolor=GREEN, fontsize=11)

    # Model file
    _rounded_box(ax, 10.5, 1.5, 2.8, 1.0,
                 'claim_model.pkl\n(Saved Model)',
                 facecolor='#1b2838', edgecolor='#9b59b6', fontsize=10)

    # --- Arrows ---
    # User -> Flask
    _arrow(ax, 2.6, 8, 4.0, 8, color=BLUE, lw=2.5)
    ax.text(3.3, 8.35, 'HTTP', fontsize=9, ha='center', color=BLUE)

    # Flask -> ML Engine
    _arrow(ax, 7.0, 8, 9.0, 8, color=RED, lw=2.5)
    ax.text(8.0, 8.35, 'predict()', fontsize=9, ha='center', color=RED)

    # Flask -> SQLite
    _arrow(ax, 5.0, 7.4, 3.8, 5.1, color=ORANGE, lw=2)
    ax.text(3.8, 6.4, 'read/write', fontsize=9, ha='center', color=ORANGE)

    # Flask -> EDA
    _arrow(ax, 5.8, 7.4, 7.2, 5.1, color=BLUE, lw=2)
    ax.text(7.0, 6.4, 'generate', fontsize=9, ha='center', color=BLUE)

    # Flask -> Chart.js
    _arrow(ax, 6.5, 7.4, 11.2, 5.1, color=GREEN, lw=2)
    ax.text(9.5, 6.4, 'JSON data', fontsize=9, ha='center', color=GREEN)

    # ML Engine -> Model file
    _arrow(ax, 10.5, 7.4, 10.5, 2.0, color='#9b59b6', lw=2)
    ax.text(11.2, 3.3, 'load model', fontsize=9, ha='center', color='#9b59b6')

    # Legend strip at bottom
    ax.text(7, 0.5, 'Car Insurance Claim Prediction  |  Flask + Gradient Boosting + SQLite + Chart.js',
            fontsize=10, ha='center', va='center', color='#888899',
            style='italic')

    _save(fig, 'fig_system_architecture.png')


# ===================================================================
# 2. Use Case Diagram
# ===================================================================

def fig_use_case_diagram():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.suptitle('Use Case Diagram', fontsize=18,
                 fontweight='bold', color=TEXT_COLOR, y=0.96)

    # --- Actors ---
    # User stick figure
    ux, uy = 1.5, 5.5
    ax.plot(ux, uy + 0.7, 'o', color=BLUE, markersize=18, zorder=3)
    ax.plot([ux, ux], [uy + 0.4, uy - 0.3], color=BLUE, lw=2, zorder=3)
    ax.plot([ux - 0.4, ux + 0.4], [uy + 0.15, uy + 0.15], color=BLUE, lw=2, zorder=3)
    ax.plot([ux - 0.3, ux], [uy - 0.9, uy - 0.3], color=BLUE, lw=2, zorder=3)
    ax.plot([ux + 0.3, ux], [uy - 0.9, uy - 0.3], color=BLUE, lw=2, zorder=3)
    ax.text(ux, uy - 1.2, 'User', fontsize=12, ha='center',
            fontweight='bold', color=BLUE)

    # Admin stick figure
    adx, ady = 12.5, 5.5
    ax.plot(adx, ady + 0.7, 'o', color=RED, markersize=18, zorder=3)
    ax.plot([adx, adx], [ady + 0.4, ady - 0.3], color=RED, lw=2, zorder=3)
    ax.plot([adx - 0.4, adx + 0.4], [ady + 0.15, ady + 0.15], color=RED, lw=2, zorder=3)
    ax.plot([adx - 0.3, adx], [ady - 0.9, ady - 0.3], color=RED, lw=2, zorder=3)
    ax.plot([adx + 0.3, adx], [ady - 0.9, ady - 0.3], color=RED, lw=2, zorder=3)
    ax.text(adx, ady - 1.2, 'Admin', fontsize=12, ha='center',
            fontweight='bold', color=RED)

    # System boundary
    rect = mpatches.FancyBboxPatch(
        (3.5, 0.6), 7, 8.5,
        boxstyle="round,pad=0.3",
        facecolor='#0e1628', edgecolor='#334466', linewidth=2,
        linestyle='--', zorder=0,
    )
    ax.add_patch(rect)
    ax.text(7, 9.3, 'Car Insurance Claim Prediction System',
            fontsize=13, ha='center', fontweight='bold', color='#aabbdd')

    # --- Use Cases (ellipses) ---
    user_cases = [
        (7, 8.2, 'Register'),
        (7, 7.2, 'Login'),
        (7, 6.2, 'Make Prediction'),
        (7, 5.2, 'View History'),
        (7, 4.2, 'View Visualizations'),
        (7, 3.2, 'View Dashboard'),
        (7, 2.2, 'View About'),
    ]
    admin_case = (7, 1.2, 'View All Users Stats')

    for cx, cy, label in user_cases:
        ellipse = mpatches.Ellipse((cx, cy), 3.8, 0.75,
                                   facecolor='#16213e', edgecolor=GREEN,
                                   linewidth=1.5, zorder=2)
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color=TEXT_COLOR, zorder=3)
        # line from User
        ax.plot([ux + 0.5, cx - 1.9], [uy + 0.1, cy], color='#557799',
                lw=1, alpha=0.5, zorder=1)

    # Admin-only use case
    cx, cy, label = admin_case
    ellipse = mpatches.Ellipse((cx, cy), 3.8, 0.75,
                               facecolor='#2a1528', edgecolor=RED,
                               linewidth=1.5, zorder=2)
    ax.add_patch(ellipse)
    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=11, fontweight='bold', color=TEXT_COLOR, zorder=3)

    # Lines from Admin to ALL use cases
    for cx, cy, _ in user_cases + [admin_case]:
        ax.plot([adx - 0.5, cx + 1.9], [ady + 0.1, cy], color='#774455',
                lw=1, alpha=0.4, zorder=1)

    _save(fig, 'fig_use_case_diagram.png')


# ===================================================================
# 3. ML Training Pipeline
# ===================================================================

def fig_ml_pipeline():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.suptitle('ML Training Pipeline', fontsize=18,
                 fontweight='bold', color=TEXT_COLOR, y=0.96)

    # Pipeline steps as a flowing diagram (two rows)
    steps_top = [
        ('Dataset\n(10,000 records)', RED),
        ('Feature Extraction\n(17 features)', BLUE),
        ('Label Encoding\n(9 categorical)', GREEN),
        ('Train-Test Split\n(80 / 20)', ORANGE),
    ]

    steps_bottom = [
        ('Train 4 Models\n(RF, GB, SVM, LR)', RED),
        ('Evaluate Models\n(Acc, Prec, Rec, F1)', BLUE),
        ('Select Best Model\n(GB  91.95%)', GREEN),
        ('Save Model\n(claim_model.pkl)', ORANGE),
    ]

    # --- Top row (left to right) ---
    top_y = 6.0
    x_positions_top = [1.75, 5.0, 8.25, 11.5]
    box_w, box_h = 2.8, 1.4

    for i, ((label, color), x) in enumerate(zip(steps_top, x_positions_top)):
        _rounded_box(ax, x, top_y, box_w, box_h, label,
                     facecolor='#16213e', edgecolor=color, fontsize=11,
                     linewidth=2.5)
        # Step number badge
        badge = mpatches.Circle((x - box_w / 2 + 0.25, top_y + box_h / 2 - 0.2),
                                0.22, facecolor=color, edgecolor='none', zorder=4)
        ax.add_patch(badge)
        ax.text(x - box_w / 2 + 0.25, top_y + box_h / 2 - 0.2,
                str(i + 1), fontsize=9, ha='center', va='center',
                fontweight='bold', color='white', zorder=5)
        if i < len(steps_top) - 1:
            _arrow(ax, x + box_w / 2 + 0.05, top_y,
                   x_positions_top[i + 1] - box_w / 2 - 0.05, top_y,
                   color='#e94560', lw=2.5)

    # Arrow from top-right down to bottom-right
    _arrow(ax, 11.5, top_y - box_h / 2 - 0.05,
           11.5, 2.8 + box_h / 2 + 0.05,
           color='#e94560', lw=2.5)

    # --- Bottom row (right to left) ---
    bot_y = 2.8
    x_positions_bot = [11.5, 8.25, 5.0, 1.75]

    for i, ((label, color), x) in enumerate(zip(steps_bottom, x_positions_bot)):
        _rounded_box(ax, x, bot_y, box_w, box_h, label,
                     facecolor='#16213e', edgecolor=color, fontsize=11,
                     linewidth=2.5)
        step_num = i + 5
        badge = mpatches.Circle((x - box_w / 2 + 0.25, bot_y + box_h / 2 - 0.2),
                                0.22, facecolor=color, edgecolor='none', zorder=4)
        ax.add_patch(badge)
        ax.text(x - box_w / 2 + 0.25, bot_y + box_h / 2 - 0.2,
                str(step_num), fontsize=9, ha='center', va='center',
                fontweight='bold', color='white', zorder=5)
        if i < len(steps_bottom) - 1:
            _arrow(ax, x - box_w / 2 - 0.05, bot_y,
                   x_positions_bot[i + 1] + box_w / 2 + 0.05, bot_y,
                   color='#e94560', lw=2.5)

    # Subtitle
    ax.text(7, 0.6,
            'Pipeline: CSV -> Preprocessing -> Model Training -> Evaluation -> Deployment',
            fontsize=10, ha='center', color='#888899', style='italic')

    _save(fig, 'fig_ml_pipeline.png')


# ===================================================================
# 4. Data Preprocessing Pipeline
# ===================================================================

def fig_data_preprocessing():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.suptitle('Data Preprocessing Pipeline', fontsize=18,
                 fontweight='bold', color=TEXT_COLOR, y=0.96)

    steps = [
        ('Raw CSV\n(Car_Insurance_Claim.csv)', RED, '10,000 rows\n19 columns'),
        ('Drop ID Column\n(Remove non-predictive)', BLUE, 'Removed: ID\n18 columns remain'),
        ('Encode Categorical\n(LabelEncoder)', GREEN, '9 categorical features\nconverted to numeric'),
        ('Split Features / Target\n(X, y separation)', ORANGE, 'X: 17 features\ny: OUTCOME'),
        ('Stratified Train-Test\nSplit (80/20)', '#9b59b6', 'Train: 8,000\nTest: 2,000'),
        ('Ready for\nModel Training', RED, 'All numeric\nBalanced split'),
    ]

    n = len(steps)
    # Arrange in a single horizontal flow, wrapping to two rows
    top_y, bot_y = 5.8, 2.2
    positions = [
        (2.3, top_y), (5.5, top_y), (8.7, top_y),
        (11.5, bot_y), (8.3, bot_y), (5.1, bot_y),
    ]

    box_w, box_h = 2.6, 1.3

    for i, ((label, color, detail), (x, y)) in enumerate(zip(steps, positions)):
        _rounded_box(ax, x, y, box_w, box_h, label,
                     facecolor='#16213e', edgecolor=color, fontsize=10,
                     linewidth=2.5)
        # Detail text below/above
        if y == top_y:
            dy = -box_h / 2 - 0.5
        else:
            dy = box_h / 2 + 0.5
        ax.text(x, y + dy, detail, fontsize=9, ha='center', va='center',
                color='#aaaacc', style='italic')

        # Step badge
        badge = mpatches.Circle((x - box_w / 2 + 0.22, y + box_h / 2 - 0.18),
                                0.2, facecolor=color, edgecolor='none', zorder=4)
        ax.add_patch(badge)
        ax.text(x - box_w / 2 + 0.22, y + box_h / 2 - 0.18,
                str(i + 1), fontsize=9, ha='center', va='center',
                fontweight='bold', color='white', zorder=5)

    # Arrows: top row left-to-right
    for i in range(2):
        x1 = positions[i][0] + box_w / 2 + 0.05
        x2 = positions[i + 1][0] - box_w / 2 - 0.05
        _arrow(ax, x1, top_y, x2, top_y, color='#e94560', lw=2.5)

    # Arrow: top-right down to bottom-right
    _arrow(ax, positions[2][0] + box_w / 2 + 0.05, top_y,
           positions[3][0] + box_w / 2 + 0.05, bot_y,
           color='#e94560', lw=2.5)

    # Arrows: bottom row right-to-left
    for i in range(3, 5):
        x1 = positions[i][0] - box_w / 2 - 0.05
        x2 = positions[i + 1][0] + box_w / 2 + 0.05
        _arrow(ax, x1, bot_y, x2, bot_y, color='#e94560', lw=2.5)

    ax.text(7, 0.4,
            'Preprocessing ensures clean, numeric, balanced data for ML training',
            fontsize=10, ha='center', color='#888899', style='italic')

    _save(fig, 'fig_data_preprocessing.png')


# ===================================================================
# 5. Model Performance Comparison (Grouped Bar Chart)
# ===================================================================

def fig_model_comparison():
    fig, ax = plt.subplots(figsize=(12, 8))

    models = ['Random\nForest', 'Gradient\nBoosting', 'SVM', 'Logistic\nRegression']
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']

    # From models_info.json
    accuracy  = [90.10, 91.95, 91.10, 90.25]
    precision = [86.10, 89.45, 85.62, 83.92]
    recall    = [73.85, 78.27, 79.04, 77.31]
    f1        = [79.50, 83.49, 82.20, 80.48]

    data = np.array([accuracy, precision, recall, f1])
    colors = [RED, BLUE, GREEN, ORANGE]

    n_models = len(models)
    n_metrics = len(metrics_names)
    x = np.arange(n_models)
    bar_width = 0.18
    offsets = np.arange(n_metrics) - (n_metrics - 1) / 2

    for i, (metric_vals, color, name) in enumerate(
            zip(data, colors, metrics_names)):
        bars = ax.bar(x + offsets[i] * bar_width, metric_vals,
                      bar_width * 0.9, label=name, color=color,
                      edgecolor='white', linewidth=0.5, alpha=0.9)
        # Value labels on top
        for bar, val in zip(bars, metric_vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=8,
                    color=color, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=12, fontweight='bold')
    ax.set_ylabel('Score (%)', fontsize=13, fontweight='bold')
    ax.set_title('Model Performance Comparison', fontsize=18,
                 fontweight='bold', pad=15)
    ax.set_ylim(65, 100)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.3,
              edgecolor='#444466')
    ax.grid(axis='y', alpha=0.2)

    # Highlight best model
    ax.annotate('Best Model', xy=(1, 92.5), xytext=(2.2, 96),
                fontsize=11, fontweight='bold', color=GREEN,
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=2),
                ha='center')

    plt.tight_layout()
    _save(fig, 'fig_model_comparison.png')


# ===================================================================
# 6. Confusion Matrix (Gradient Boosting)
# ===================================================================

def fig_confusion_matrix():
    fig, ax = plt.subplots(figsize=(12, 8))

    cm = np.array([[1432, 48],
                   [113, 407]])
    labels = ['No Claim', 'Claim']

    # Normalised version for color intensity
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

    # Custom colormap from dark blue -> red
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(
        'custom', ['#16213e', '#0f3460', '#e94560', RED], N=256)

    im = ax.imshow(cm_norm, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    # Annotations
    for i in range(2):
        for j in range(2):
            val = cm[i, j]
            pct = cm_norm[i, j] * 100
            txt_color = 'white'
            ax.text(j, i, f'{val}\n({pct:.1f}%)',
                    ha='center', va='center', fontsize=16,
                    fontweight='bold', color=txt_color)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=13, fontweight='bold')
    ax.set_yticklabels(labels, fontsize=13, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=14, fontweight='bold', labelpad=10)
    ax.set_ylabel('Actual Label', fontsize=14, fontweight='bold', labelpad=10)
    ax.set_title('Confusion Matrix  -  Gradient Boosting (91.95% Accuracy)',
                 fontsize=16, fontweight='bold', pad=15)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Normalized Proportion', fontsize=12, color=TEXT_COLOR)
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=TEXT_COLOR)

    # Summary text
    total = cm.sum()
    correct = cm[0, 0] + cm[1, 1]
    ax.text(0.5, -0.18, f'Total Predictions: {total}   |   '
            f'Correct: {correct}   |   Incorrect: {total - correct}',
            transform=ax.transAxes, fontsize=11, ha='center',
            color='#aabbcc', style='italic')

    plt.tight_layout()
    _save(fig, 'fig_confusion_matrix.png')


# ===================================================================
# 7. Feature Importance
# ===================================================================

def fig_feature_importance():
    fig, ax = plt.subplots(figsize=(12, 8))

    # Approximate importance values ranked (from Random Forest)
    features = [
        'POSTAL_CODE', 'RACE', 'CHILDREN', 'MARRIED',
        'VEHICLE_OWNERSHIP', 'GENDER', 'EDUCATION', 'INCOME',
        'VEHICLE_YEAR', 'VEHICLE_TYPE', 'ANNUAL_MILEAGE',
        'CREDIT_SCORE', 'DUIS', 'PAST_ACCIDENTS', 'AGE',
        'SPEEDING_VIOLATIONS', 'DRIVING_EXPERIENCE',
    ]
    importances = [
        0.012, 0.015, 0.018, 0.020,
        0.022, 0.028, 0.032, 0.038,
        0.042, 0.048, 0.062,
        0.072, 0.082, 0.098, 0.108,
        0.142, 0.168,
    ]

    # Gradient colors from low to high importance
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(
        'importance', [BLUE, '#e94560', RED], N=len(features))
    norm_vals = np.array(importances) / max(importances)
    colors = [cmap(v) for v in norm_vals]

    y_pos = np.arange(len(features))
    bars = ax.barh(y_pos, importances, color=colors, edgecolor='white',
                   linewidth=0.5, height=0.7, alpha=0.9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(features, fontsize=11, fontweight='bold')
    ax.set_xlabel('Importance Score', fontsize=13, fontweight='bold')
    ax.set_title('Feature Importance  (Random Forest)',
                 fontsize=18, fontweight='bold', pad=15)

    # Value labels
    for bar, val in zip(bars, importances):
        ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height() / 2,
                f'{val:.3f}', va='center', fontsize=10, color=TEXT_COLOR,
                fontweight='bold')

    ax.set_xlim(0, max(importances) * 1.18)
    ax.grid(axis='x', alpha=0.2)

    # Top-3 annotation
    ax.axhline(y=len(features) - 3.5, color=GREEN, linestyle='--',
               alpha=0.4, lw=1.5)
    ax.text(max(importances) * 0.65, len(features) - 3.2,
            'Top 3 Features', fontsize=10, color=GREEN,
            fontweight='bold', style='italic')

    plt.tight_layout()
    _save(fig, 'fig_feature_importance.png')


# ===================================================================
# Main
# ===================================================================

if __name__ == '__main__':
    print('=' * 55)
    print('Generating Project Report Figures (Dark Theme)')
    print('=' * 55)

    fig_system_architecture()
    fig_use_case_diagram()
    fig_ml_pipeline()
    fig_data_preprocessing()
    fig_model_comparison()
    fig_confusion_matrix()
    fig_feature_importance()

    print('\n' + '=' * 55)
    print(f'All 7 figures saved to {OUT_DIR}/')
    print('=' * 55)
