"""
generate_figures.py
Social Media Forensics: Cyberbullying & Hate Speech Analysis

Generates 7 dark-themed matplotlib figures for the project report.
All figures are saved to the figures/ subdirectory at 150 DPI.

Usage:
    python generate_figures.py
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import seaborn as sns

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Dark theme settings
# ---------------------------------------------------------------------------
BG_COLOR = "#0d1b2a"
TEXT_COLOR = "white"
RED = "#ef4444"
ORANGE = "#f59e0b"
GREEN = "#22c55e"
BLUE = "#3b82f6"
LIGHT_BLUE = "#60a5fa"
PURPLE = "#a78bfa"
CYAN = "#22d3ee"
GRAY = "#94a3b8"
DARK_GRAY = "#1e293b"
BORDER_COLOR = "#334155"

DPI = 150


def apply_dark_theme():
    """Apply consistent dark theme to all figures."""
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': BG_COLOR,
        'savefig.facecolor': BG_COLOR,
        'text.color': TEXT_COLOR,
        'axes.labelcolor': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'axes.edgecolor': BORDER_COLOR,
        'grid.color': BORDER_COLOR,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
    })


# ===========================================================================
# Helper: draw a rounded box with centered text
# ===========================================================================

def draw_box(ax, x, y, w, h, text, facecolor=DARK_GRAY, edgecolor=BLUE,
             fontsize=9, textcolor=TEXT_COLOR, linewidth=1.5, zorder=2,
             bold=False):
    """Draw a rounded rectangle with centered text on the given axes."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.15",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder,
    )
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=textcolor, fontweight=weight, zorder=zorder + 1,
            wrap=True)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color=GRAY, linewidth=1.5,
               arrowstyle='->', connectionstyle='arc3,rad=0'):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=arrowstyle,
        color=color,
        linewidth=linewidth,
        mutation_scale=15,
        connectionstyle=connectionstyle,
        zorder=1,
    )
    ax.add_patch(arrow)
    return arrow


# ===========================================================================
# Figure 1: System Architecture Diagram
# ===========================================================================

def fig_system_architecture():
    """System Architecture Diagram showing major components and data flow."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title("System Architecture Diagram", fontsize=18, fontweight='bold',
                 color=TEXT_COLOR, pad=20)

    # --- Row 1: User -> Browser -> Flask Web App ---
    draw_box(ax, 1.5, 6.5, 2.0, 1.0, "User", facecolor="#1e3a5f",
             edgecolor=CYAN, fontsize=12, bold=True)
    draw_box(ax, 4.5, 6.5, 2.2, 1.0, "Web Browser", facecolor=DARK_GRAY,
             edgecolor=LIGHT_BLUE, fontsize=11, bold=True)
    draw_box(ax, 8.5, 6.5, 3.0, 1.2, "Flask Web App\n(Port 5007)",
             facecolor="#1e3a5f", edgecolor=BLUE, fontsize=12, bold=True)

    # Arrows: User -> Browser -> Flask
    draw_arrow(ax, 2.5, 6.5, 3.4, 6.5, color=CYAN, linewidth=2)
    draw_arrow(ax, 5.6, 6.5, 7.0, 6.5, color=LIGHT_BLUE, linewidth=2)

    # --- Row 2: NLP Pipeline ---
    draw_box(ax, 3.0, 4.3, 3.5, 1.0,
             "NLP Pipeline\n(Preprocessing + TF-IDF Vectorization)",
             facecolor="#1a2e1a", edgecolor=GREEN, fontsize=10, bold=True)

    # --- Row 2: ML Classification ---
    draw_box(ax, 8.5, 4.3, 3.2, 1.0,
             "ML Classification\n(Logistic Regression)",
             facecolor="#2d1a1a", edgecolor=RED, fontsize=10, bold=True)

    # Flask -> NLP Pipeline
    draw_arrow(ax, 7.5, 5.9, 4.5, 4.8, color=GREEN, linewidth=2,
               connectionstyle='arc3,rad=-0.1')
    # NLP -> ML
    draw_arrow(ax, 4.75, 4.3, 6.9, 4.3, color=ORANGE, linewidth=2)

    # --- Row 3: SQLite DB ---
    draw_box(ax, 1.5, 2.3, 2.8, 1.0,
             "SQLite Database\n(users, predictions)",
             facecolor="#1a1a2e", edgecolor=PURPLE, fontsize=10, bold=True)
    # Flask -> SQLite
    draw_arrow(ax, 7.5, 5.9, 2.5, 2.8, color=PURPLE, linewidth=2,
               connectionstyle='arc3,rad=0.3')

    # --- Row 3: EDA Visualization Module ---
    draw_box(ax, 5.5, 2.3, 3.4, 1.0,
             "EDA Visualization Module\n(matplotlib / seaborn / wordcloud)",
             facecolor="#1a2e2e", edgecolor=CYAN, fontsize=9, bold=True)
    # Flask -> EDA
    draw_arrow(ax, 8.0, 5.9, 5.8, 2.8, color=CYAN, linewidth=2,
               connectionstyle='arc3,rad=0.15')

    # --- Row 3: Chart.js Dashboard ---
    draw_box(ax, 10.0, 2.3, 2.8, 1.0,
             "Chart.js Dashboard\n(Interactive Charts)",
             facecolor="#2e2e1a", edgecolor=ORANGE, fontsize=10, bold=True)
    # Flask -> Dashboard
    draw_arrow(ax, 9.5, 5.9, 10.0, 2.8, color=ORANGE, linewidth=2,
               connectionstyle='arc3,rad=-0.2')

    # --- ML -> Flask (result back) ---
    draw_arrow(ax, 8.5, 4.8, 8.5, 5.9, color=RED, linewidth=1.5,
               arrowstyle='->', connectionstyle='arc3,rad=0.3')

    # --- Legend / labels ---
    ax.text(7.0, 0.5, "Data Flow", fontsize=10, color=GRAY,
            ha='center', style='italic')

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_system_architecture.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [1/7] System Architecture Diagram -> {path}")


# ===========================================================================
# Figure 2: Use Case Diagram
# ===========================================================================

def fig_use_case_diagram():
    """Use Case Diagram with User and Admin actors."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title("Use Case Diagram", fontsize=18, fontweight='bold',
                 color=TEXT_COLOR, pad=20)

    # --- System boundary ---
    system_box = FancyBboxPatch(
        (3.5, 0.4), 7.0, 7.2,
        boxstyle="round,pad=0.3",
        facecolor='none',
        edgecolor=BORDER_COLOR,
        linewidth=2,
        linestyle='--',
        zorder=0,
    )
    ax.add_patch(system_box)
    ax.text(7.0, 7.35, "Cyberbullying & Hate Speech Analysis System",
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            color=LIGHT_BLUE)

    # --- Actors ---
    # User (left side)
    ax.text(1.5, 5.5, "USER", ha='center', fontsize=12, fontweight='bold',
            color=CYAN)
    # Simple stick figure
    circle_user = plt.Circle((1.5, 5.0), 0.25, fill=False, edgecolor=CYAN,
                             linewidth=2, zorder=3)
    ax.add_patch(circle_user)
    ax.plot([1.5, 1.5], [4.75, 4.2], color=CYAN, linewidth=2, zorder=3)
    ax.plot([1.1, 1.9], [4.55, 4.55], color=CYAN, linewidth=2, zorder=3)
    ax.plot([1.5, 1.2], [4.2, 3.7], color=CYAN, linewidth=2, zorder=3)
    ax.plot([1.5, 1.8], [4.2, 3.7], color=CYAN, linewidth=2, zorder=3)

    # Admin (right side)
    ax.text(12.5, 5.5, "ADMIN", ha='center', fontsize=12, fontweight='bold',
            color=ORANGE)
    circle_admin = plt.Circle((12.5, 5.0), 0.25, fill=False,
                              edgecolor=ORANGE, linewidth=2, zorder=3)
    ax.add_patch(circle_admin)
    ax.plot([12.5, 12.5], [4.75, 4.2], color=ORANGE, linewidth=2, zorder=3)
    ax.plot([12.1, 12.9], [4.55, 4.55], color=ORANGE, linewidth=2, zorder=3)
    ax.plot([12.5, 12.2], [4.2, 3.7], color=ORANGE, linewidth=2, zorder=3)
    ax.plot([12.5, 12.8], [4.2, 3.7], color=ORANGE, linewidth=2, zorder=3)

    # --- Use cases ---
    user_use_cases = [
        ("Register", 6.5),
        ("Login", 5.7),
        ("Analyze Text", 4.9),
        ("View History", 4.1),
        ("View Visualizations", 3.3),
        ("View Dashboard", 2.5),
        ("View About", 1.7),
    ]

    admin_use_case = ("View All Users Stats", 0.9)

    for name, y_pos in user_use_cases:
        # Ellipse for use case
        ellipse = mpatches.Ellipse(
            (7.0, y_pos), 3.2, 0.6,
            facecolor=DARK_GRAY, edgecolor=BLUE,
            linewidth=1.5, zorder=2
        )
        ax.add_patch(ellipse)
        ax.text(7.0, y_pos, name, ha='center', va='center', fontsize=10,
                color=TEXT_COLOR, fontweight='bold', zorder=3)
        # User -> use case
        draw_arrow(ax, 1.9, 4.5, 5.4, y_pos, color=CYAN, linewidth=1,
                   arrowstyle='-')

    # Admin-only use case
    ellipse_admin = mpatches.Ellipse(
        (7.0, admin_use_case[1]), 3.2, 0.6,
        facecolor="#2e1a00", edgecolor=ORANGE,
        linewidth=1.5, zorder=2
    )
    ax.add_patch(ellipse_admin)
    ax.text(7.0, admin_use_case[1], admin_use_case[0], ha='center',
            va='center', fontsize=10, color=ORANGE, fontweight='bold',
            zorder=3)

    # Admin -> all use cases (admin can do everything)
    for name, y_pos in user_use_cases:
        draw_arrow(ax, 12.1, 4.5, 8.6, y_pos, color=ORANGE, linewidth=0.8,
                   arrowstyle='-')
    draw_arrow(ax, 12.1, 4.5, 8.6, admin_use_case[1], color=ORANGE,
               linewidth=1.2, arrowstyle='-')

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_use_case_diagram.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [2/7] Use Case Diagram -> {path}")


# ===========================================================================
# Figure 3: NLP/ML Pipeline
# ===========================================================================

def fig_nlp_pipeline():
    """NLP/ML Pipeline from raw text to saved model."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title("NLP / ML Pipeline", fontsize=18, fontweight='bold',
                 color=TEXT_COLOR, pad=20)

    # Pipeline steps (arranged in a zigzag for readability)
    steps = [
        ("Raw Text", 1.5, 7.0, CYAN),
        ("Lowercase", 4.0, 7.0, LIGHT_BLUE),
        ("Remove URLs", 6.5, 7.0, LIGHT_BLUE),
        ("Remove\nMentions (@)", 9.0, 7.0, LIGHT_BLUE),
        ("Remove\nHashtags (#)", 11.5, 7.0, LIGHT_BLUE),
        ("Remove Special\nCharacters", 11.5, 5.2, LIGHT_BLUE),
        ("Remove\nStopwords", 9.0, 5.2, LIGHT_BLUE),
        ("TF-IDF Vectorization\n(5000 features, bigrams)", 6.0, 5.2, GREEN),
        ("Train 6 ML\nModels", 3.0, 5.2, ORANGE),
        ("Evaluate\nModels", 3.0, 3.2, RED),
        ("Select Best Model\nLogistic Regression\n(94.83% Accuracy)", 6.5, 3.2, GREEN),
        ("Save Model\n(.pkl)", 10.5, 3.2, BLUE),
    ]

    box_w, box_h = 2.0, 1.0

    for i, (label, x, y, color) in enumerate(steps):
        draw_box(ax, x, y, box_w, box_h, label, facecolor=DARK_GRAY,
                 edgecolor=color, fontsize=9, bold=True)

    # Arrows connecting sequential steps
    # Row 1: left to right (steps 0->1->2->3->4)
    for i in range(4):
        x1 = steps[i][1] + box_w / 2
        y1 = steps[i][2]
        x2 = steps[i + 1][1] - box_w / 2
        y2 = steps[i + 1][2]
        draw_arrow(ax, x1, y1, x2, y2, color=GRAY, linewidth=1.5)

    # Step 4 -> Step 5 (down)
    draw_arrow(ax, steps[4][1], steps[4][2] - box_h / 2,
               steps[5][1], steps[5][2] + box_h / 2, color=GRAY, linewidth=1.5)

    # Row 2: right to left (steps 5->6->7->8)
    for i in range(5, 8):
        x1 = steps[i][1] - box_w / 2
        y1 = steps[i][2]
        x2 = steps[i + 1][1] + box_w / 2
        y2 = steps[i + 1][2]
        draw_arrow(ax, x1, y1, x2, y2, color=GRAY, linewidth=1.5)

    # Step 8 -> Step 9 (down)
    draw_arrow(ax, steps[8][1], steps[8][2] - box_h / 2,
               steps[9][1], steps[9][2] + box_h / 2, color=GRAY, linewidth=1.5)

    # Row 3: left to right (steps 9->10->11)
    for i in range(9, 11):
        x1 = steps[i][1] + box_w / 2
        y1 = steps[i][2]
        x2 = steps[i + 1][1] - box_w / 2
        y2 = steps[i + 1][2]
        draw_arrow(ax, x1, y1, x2, y2, color=GRAY, linewidth=1.5)

    # Stage labels
    ax.text(0.3, 7.5, "Stage 1:\nText Cleaning", fontsize=8, color=GRAY,
            style='italic', va='center')
    ax.text(0.3, 5.2, "Stage 2:\nFeature\nExtraction\n& Training", fontsize=8,
            color=GRAY, style='italic', va='center')
    ax.text(0.3, 3.2, "Stage 3:\nEvaluation\n& Deployment", fontsize=8,
            color=GRAY, style='italic', va='center')

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_nlp_pipeline.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [3/7] NLP/ML Pipeline -> {path}")


# ===========================================================================
# Figure 4: Data Preprocessing Pipeline
# ===========================================================================

def fig_data_preprocessing():
    """Data Preprocessing Pipeline from dataset to training-ready features."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title("Data Preprocessing Pipeline", fontsize=18, fontweight='bold',
                 color=TEXT_COLOR, pad=20)

    # Center pipeline vertically
    y_center = 4.0
    box_w = 2.2
    box_h = 1.6

    pipeline_steps = [
        ("Dataset\n(15,000 samples\n3 classes)", 1.5, y_center, CYAN, "#0e2a3e"),
        ("Text Cleaning\n(lowercase, remove\nURLs, mentions,\nhashtags, special chars)", 4.2, y_center, LIGHT_BLUE, DARK_GRAY),
        ("Stopword\nRemoval\n(NLTK English\nstopwords)", 6.9, y_center, PURPLE, DARK_GRAY),
        ("TF-IDF\nVectorization\n(max_features=5000\nngram_range=(1,2))", 9.6, y_center, GREEN, "#1a2e1a"),
        ("Train-Test Split\n(80/20 stratified\nrandom_state=42)", 12.3, y_center, ORANGE, "#2e2e1a"),
    ]

    for label, x, y, edgecolor, facecolor in pipeline_steps:
        draw_box(ax, x, y, box_w, box_h, label, facecolor=facecolor,
                 edgecolor=edgecolor, fontsize=9, bold=True, linewidth=2)

    # Arrows between steps
    for i in range(len(pipeline_steps) - 1):
        x1 = pipeline_steps[i][1] + box_w / 2
        x2 = pipeline_steps[i + 1][1] - box_w / 2
        draw_arrow(ax, x1, y_center, x2, y_center, color=GRAY, linewidth=2)

    # Final output box below the last step
    draw_box(ax, 12.3, 1.8, 2.2, 1.0, "Ready for\nTraining",
             facecolor="#1a2e1a", edgecolor=GREEN, fontsize=11, bold=True,
             linewidth=2)
    draw_arrow(ax, 12.3, y_center - box_h / 2, 12.3, 2.3, color=GREEN,
               linewidth=2)

    # Sample counts annotation
    ax.text(1.5, y_center - box_h / 2 - 0.5,
            "Hate Speech: 3,000 (20%)\nOffensive: 3,750 (25%)\nClean: 8,250 (55%)",
            ha='center', va='top', fontsize=8, color=GRAY,
            style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_GRAY,
                      edgecolor=BORDER_COLOR, alpha=0.8))

    # Feature count annotation
    ax.text(9.6, y_center - box_h / 2 - 0.5,
            "Output: sparse matrix\n15,000 x 5,000",
            ha='center', va='top', fontsize=8, color=GRAY, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_GRAY,
                      edgecolor=BORDER_COLOR, alpha=0.8))

    # Split annotation
    ax.text(12.3, y_center + box_h / 2 + 0.5,
            "Train: 12,000 samples\nTest: 3,000 samples",
            ha='center', va='bottom', fontsize=8, color=GRAY, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_GRAY,
                      edgecolor=BORDER_COLOR, alpha=0.8))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_data_preprocessing.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [4/7] Data Preprocessing Pipeline -> {path}")


# ===========================================================================
# Figure 5: Model Performance Comparison (Grouped Bar Chart)
# ===========================================================================

def fig_model_comparison():
    """Grouped bar chart comparing 6 models across 4 metrics."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    models = [
        "Logistic\nRegression",
        "Naive\nBayes",
        "SVM",
        "KNN",
        "Gradient\nBoosting",
        "Random\nForest",
    ]

    # Metrics: Accuracy, Precision, Recall, F1
    accuracy  = [94.83, 94.83, 94.83, 94.73, 94.50, 94.17]
    precision = [94.83, 94.83, 94.83, 94.73, 94.51, 94.17]
    recall    = [94.83, 94.83, 94.83, 94.73, 94.50, 94.17]
    f1_score  = [94.81, 94.81, 94.81, 94.71, 94.47, 94.14]

    x = np.arange(len(models))
    width = 0.18

    colors = [BLUE, GREEN, ORANGE, RED]
    labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    data = [accuracy, precision, recall, f1_score]

    for i, (metric_data, color, label) in enumerate(zip(data, colors, labels)):
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, metric_data, width, label=label, color=color,
                      edgecolor='none', alpha=0.9, zorder=3)
        # Add value labels on top of each bar
        for bar, val in zip(bars, metric_data):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=6.5,
                    color=TEXT_COLOR, fontweight='bold')

    ax.set_xlabel('Model', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel('Score (%)', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_title('Model Performance Comparison', fontsize=18,
                 fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10)
    ax.set_ylim(93.5, 95.5)
    ax.yaxis.grid(True, alpha=0.2, color=GRAY, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.3,
              edgecolor=BORDER_COLOR)

    # Highlight best model
    ax.annotate('Best Model', xy=(0, 94.83), xytext=(0, 95.3),
                fontsize=10, color=GREEN, fontweight='bold',
                ha='center',
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_model_comparison.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [5/7] Model Performance Comparison -> {path}")


# ===========================================================================
# Figure 6: Confusion Matrix (Logistic Regression)
# ===========================================================================

def fig_confusion_matrix():
    """Annotated heatmap confusion matrix for the best model."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    cm = np.array([
        [576,  13,  46],
        [ 16, 716,  37],
        [ 27,  27, 1553],
    ])
    labels = ['Hate Speech', 'Offensive', 'Clean']

    # Use a custom colormap that works well on dark backgrounds
    cmap = sns.color_palette("blend:#1e293b,#ef4444", as_cmap=True)

    sns.heatmap(
        cm, annot=True, fmt='d', cmap=cmap,
        xticklabels=labels, yticklabels=labels, ax=ax,
        linewidths=2, linecolor=BG_COLOR,
        annot_kws={'size': 16, 'fontweight': 'bold', 'color': TEXT_COLOR},
        cbar_kws={'label': 'Count', 'shrink': 0.8},
        square=True,
    )

    ax.set_title('Confusion Matrix - Logistic Regression (Best Model)',
                 fontsize=18, fontweight='bold', pad=15, color=TEXT_COLOR)
    ax.set_xlabel('Predicted Label', fontsize=13, fontweight='bold',
                  labelpad=10)
    ax.set_ylabel('Actual Label', fontsize=13, fontweight='bold', labelpad=10)
    ax.tick_params(axis='both', labelsize=12, colors=TEXT_COLOR)

    # Colorbar text color
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    cbar.ax.yaxis.label.set_color(TEXT_COLOR)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_COLOR)

    # Add accuracy summary below
    total = cm.sum()
    correct = np.trace(cm)
    accuracy = correct / total * 100
    ax.text(1.5, 3.6,
            f"Overall Accuracy: {accuracy:.2f}%  |  "
            f"Correct: {correct}/{total}",
            ha='center', va='top', fontsize=11, color=GREEN,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=DARK_GRAY,
                      edgecolor=GREEN, alpha=0.9))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_confusion_matrix.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [6/7] Confusion Matrix -> {path}")


# ===========================================================================
# Figure 7: Dataset Class Distribution
# ===========================================================================

def fig_class_distribution():
    """Bar chart showing class distribution in the dataset."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    classes = ['Hate Speech', 'Offensive', 'Clean']
    counts = [3000, 3750, 8250]
    percentages = [20.0, 25.0, 55.0]
    colors = [RED, ORANGE, GREEN]

    bars = ax.bar(classes, counts, color=colors, edgecolor='none', width=0.55,
                  zorder=3, alpha=0.9)

    # Add count + percentage labels on each bar
    for bar, count, pct, color in zip(bars, counts, percentages, colors):
        # Count inside the bar near the top
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() - 200,
                f'{count:,}',
                ha='center', va='top', fontsize=18, fontweight='bold',
                color=TEXT_COLOR)
        # Percentage above the bar
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 150,
                f'{pct:.0f}%',
                ha='center', va='bottom', fontsize=16, fontweight='bold',
                color=color)

    ax.set_xlabel('Class Label', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel('Number of Samples', fontsize=13, fontweight='bold',
                  labelpad=10)
    ax.set_title('Dataset Class Distribution (15,000 Total Samples)',
                 fontsize=18, fontweight='bold', pad=15)
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=11)
    ax.yaxis.grid(True, alpha=0.2, color=GRAY, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylim(0, 9500)

    # Total samples annotation
    ax.text(0.98, 0.95, f'Total: 15,000 samples',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            color=LIGHT_BLUE, ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=DARK_GRAY,
                      edgecolor=LIGHT_BLUE, alpha=0.8))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_class_distribution.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print(f"  [7/7] Class Distribution -> {path}")


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 60)
    print("  Generating Report Figures (Dark Theme, 150 DPI)")
    print(f"  Output directory: {FIGURES_DIR}")
    print("=" * 60)

    apply_dark_theme()

    fig_system_architecture()
    fig_use_case_diagram()
    fig_nlp_pipeline()
    fig_data_preprocessing()
    fig_model_comparison()
    fig_confusion_matrix()
    fig_class_distribution()

    print("=" * 60)
    print(f"  All 7 figures saved to: {FIGURES_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
