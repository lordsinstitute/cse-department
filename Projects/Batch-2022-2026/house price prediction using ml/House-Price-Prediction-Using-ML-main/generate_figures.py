"""
generate_figures.py
Generates architectural and UML diagrams for the C4 House Price Prediction project.
All figures are saved as PNG files in the figures/ directory.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from matplotlib.lines import Line2D
import numpy as np
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

DPI = 150

# Color palette
BLUE_DARK   = "#1a365d"
BLUE_MED    = "#2b6cb0"
BLUE_LIGHT  = "#bee3f8"
GREEN_DARK  = "#22543d"
GREEN_MED   = "#38a169"
GREEN_LIGHT = "#c6f6d5"
ORANGE_DARK = "#7b341e"
ORANGE_MED  = "#dd6b20"
ORANGE_LIGHT = "#feebc8"
PURPLE_MED  = "#805ad5"
PURPLE_LIGHT = "#e9d8fd"
RED_MED     = "#e53e3e"
RED_LIGHT   = "#fed7d7"
GRAY_LIGHT  = "#edf2f7"
GRAY_MED    = "#a0aec0"
GRAY_DARK   = "#2d3748"
WHITE       = "#ffffff"
TEAL_MED    = "#319795"
TEAL_LIGHT  = "#b2f5ea"
YELLOW_MED  = "#d69e2e"
YELLOW_LIGHT = "#fefcbf"
PINK_MED    = "#d53f8c"
PINK_LIGHT  = "#fed7e2"


def _save(fig, filename):
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  Saved: {path}")


def _add_fancy_box(ax, xy, width, height, text, facecolor, edgecolor,
                   fontsize=10, fontweight="normal", text_color="black",
                   boxstyle="round,pad=0.3", linewidth=1.5, alpha=1.0):
    """Draw a rounded-rect box with centered text."""
    x, y = xy
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle=boxstyle,
                         facecolor=facecolor, edgecolor=edgecolor,
                         linewidth=linewidth, alpha=alpha,
                         transform=ax.transData, zorder=2)
    ax.add_patch(box)
    cx, cy = x + width / 2, y + height / 2
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=text_color,
            zorder=3, wrap=True)
    return box


def _arrow(ax, x1, y1, x2, y2, color=GRAY_DARK, style="->", lw=1.5, connectionstyle="arc3,rad=0"):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style, color=color,
                            linewidth=lw, mutation_scale=15,
                            connectionstyle=connectionstyle,
                            zorder=4)
    ax.add_patch(arrow)
    return arrow


def _arrow_label(ax, x1, y1, x2, y2, label="", color=GRAY_DARK, style="->",
                 lw=1.5, connectionstyle="arc3,rad=0", fontsize=8):
    _arrow(ax, x1, y1, x2, y2, color=color, style=style, lw=lw,
           connectionstyle=connectionstyle)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if label:
        ax.text(mx, my + 0.15, label, ha="center", va="bottom",
                fontsize=fontsize, color=color, style="italic", zorder=5)


# ===========================================================================
# FIGURE 1.1 - Traditional vs ML-Based Comparison
# ===========================================================================
def fig_1_1_comparison():
    print("Generating fig_1_1_comparison.png ...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    fig.patch.set_facecolor(WHITE)
    fig.suptitle("Traditional vs ML-Based House Price Estimation",
                 fontsize=18, fontweight="bold", color=BLUE_DARK, y=0.97)

    # --- Left panel: Traditional ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Traditional Appraisal", fontsize=14, fontweight="bold",
                 color=ORANGE_DARK, pad=15)

    # Background panel
    bg = FancyBboxPatch((0.3, 0.3), 9.4, 9.0, boxstyle="round,pad=0.3",
                        facecolor=ORANGE_LIGHT, edgecolor=ORANGE_MED,
                        linewidth=2, alpha=0.3)
    ax.add_patch(bg)

    # Icon: person
    _add_fancy_box(ax, (3.0, 7.8), 4.0, 1.2, "Human Appraiser",
                   ORANGE_LIGHT, ORANGE_MED, fontsize=13, fontweight="bold",
                   text_color=ORANGE_DARK)

    steps = [
        ("Physical Inspection", "Subjective assessment"),
        ("Market Research", "Limited comparables"),
        ("Manual Calculation", "Few features considered"),
        ("Report Generation", "Days to complete"),
    ]
    y_pos = 6.3
    for title, desc in steps:
        _add_fancy_box(ax, (1.5, y_pos - 0.1), 7.0, 1.0,
                       f"{title}\n({desc})",
                       WHITE, ORANGE_MED, fontsize=10, text_color=GRAY_DARK)
        y_pos -= 1.5

    # Limitations
    lim_y = 0.8
    ax.text(5.0, lim_y, "Slow  |  Subjective  |  Inconsistent  |  Expensive",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color=RED_MED,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=RED_LIGHT,
                      edgecolor=RED_MED, linewidth=1.5))

    # --- Right panel: ML-Based ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("ML-Based Prediction", fontsize=14, fontweight="bold",
                 color=GREEN_DARK, pad=15)

    bg2 = FancyBboxPatch((0.3, 0.3), 9.4, 9.0, boxstyle="round,pad=0.3",
                         facecolor=GREEN_LIGHT, edgecolor=GREEN_MED,
                         linewidth=2, alpha=0.3)
    ax.add_patch(bg2)

    _add_fancy_box(ax, (3.0, 7.8), 4.0, 1.2, "ML Pipeline",
                   GREEN_LIGHT, GREEN_MED, fontsize=13, fontweight="bold",
                   text_color=GREEN_DARK)

    ml_steps = [
        ("10,000 Data Points", "9 features + target"),
        ("5 Trained Models", "LR, Ridge, DT, RF, GB"),
        ("Instant Prediction", "Sub-second response"),
        ("Result + History", "Stored in SQLite DB"),
    ]
    y_pos = 6.3
    for title, desc in ml_steps:
        _add_fancy_box(ax, (1.5, y_pos - 0.1), 7.0, 1.0,
                       f"{title}\n({desc})",
                       WHITE, GREEN_MED, fontsize=10, text_color=GRAY_DARK)
        y_pos -= 1.5

    ax.text(5.0, 0.8, "Fast  |  Objective  |  Consistent  |  Scalable",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color=GREEN_DARK,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=GREEN_LIGHT,
                      edgecolor=GREEN_MED, linewidth=1.5))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    _save(fig, "fig_1_1_comparison.png")


# ===========================================================================
# FIGURE 4.1 - System Architecture
# ===========================================================================
def fig_4_1_architecture():
    print("Generating fig_4_1_architecture.png ...")
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("System Architecture - 3-Tier Web Application",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # ---- Tier 1: Client / Presentation ----
    _add_fancy_box(ax, (0.5, 8.0), 13.0, 1.5,
                   "", BLUE_LIGHT, BLUE_MED, alpha=0.25)
    ax.text(7.0, 9.2, "PRESENTATION TIER", ha="center", fontsize=11,
            fontweight="bold", color=BLUE_DARK)

    _add_fancy_box(ax, (1.0, 8.15), 3.5, 1.1, "Web Browser\n(Chrome / Firefox)",
                   WHITE, BLUE_MED, fontsize=10, text_color=BLUE_DARK)
    _add_fancy_box(ax, (5.3, 8.15), 3.5, 1.1, "Bootstrap 5 UI\n(HTML / CSS / JS)",
                   WHITE, BLUE_MED, fontsize=10, text_color=BLUE_DARK)
    _add_fancy_box(ax, (9.6, 8.15), 3.5, 1.1, "Responsive Templates\n(Jinja2)",
                   WHITE, BLUE_MED, fontsize=10, text_color=BLUE_DARK)

    # ---- Tier 2: Application / Logic ----
    _add_fancy_box(ax, (0.5, 4.3), 13.0, 3.2,
                   "", GREEN_LIGHT, GREEN_MED, alpha=0.2)
    ax.text(7.0, 7.2, "APPLICATION TIER (Flask Server)", ha="center",
            fontsize=11, fontweight="bold", color=GREEN_DARK)

    # Routes
    routes = ["/login", "/register", "/predict", "/history", "/visualize",
              "/dashboard", "/about", "/logout"]
    rx = 1.0
    for i, r in enumerate(routes):
        _add_fancy_box(ax, (rx, 6.1), 1.4, 0.7, r,
                       WHITE, GREEN_MED, fontsize=8, text_color=GREEN_DARK)
        rx += 1.5

    # Business logic modules
    modules = [
        ("Authentication\nModule", TEAL_LIGHT, TEAL_MED),
        ("Prediction\nEngine", GREEN_LIGHT, GREEN_MED),
        ("History\nManager", YELLOW_LIGHT, YELLOW_MED),
        ("Visualization\nEngine", PURPLE_LIGHT, PURPLE_MED),
    ]
    mx = 1.3
    for label, fc, ec in modules:
        _add_fancy_box(ax, (mx, 4.5), 2.6, 1.2, label,
                       fc, ec, fontsize=10, fontweight="bold",
                       text_color=GRAY_DARK)
        mx += 3.0

    # Arrows Tier 1 -> Tier 2
    _arrow(ax, 7.0, 8.15, 7.0, 7.3, color=BLUE_MED, lw=2)
    ax.text(7.3, 7.7, "HTTP Requests", fontsize=8, color=BLUE_MED, style="italic")

    # ---- Tier 3: Data ----
    _add_fancy_box(ax, (0.5, 0.5), 13.0, 3.3,
                   "", ORANGE_LIGHT, ORANGE_MED, alpha=0.2)
    ax.text(7.0, 3.5, "DATA TIER", ha="center",
            fontsize=11, fontweight="bold", color=ORANGE_DARK)

    _add_fancy_box(ax, (1.0, 0.8), 3.0, 2.2,
                   "SQLite Database\n\nusers table\npredictions table",
                   WHITE, ORANGE_MED, fontsize=10, text_color=ORANGE_DARK)
    _add_fancy_box(ax, (5.0, 0.8), 3.0, 2.2,
                   "housing.csv\n\n10,000 rows\n9 features + target",
                   WHITE, ORANGE_MED, fontsize=10, text_color=ORANGE_DARK)
    _add_fancy_box(ax, (9.5, 0.8), 3.5, 2.2,
                   "ML Models (.pkl)\n\nLR | Ridge | DT\nRF | Gradient Boosting",
                   WHITE, ORANGE_MED, fontsize=10, text_color=ORANGE_DARK)

    # Arrows Tier 2 -> Tier 3
    _arrow(ax, 2.6, 4.5, 2.5, 3.0, color=ORANGE_MED, lw=2)
    _arrow(ax, 5.8, 4.5, 6.5, 3.0, color=ORANGE_MED, lw=2)
    _arrow(ax, 9.3, 4.5, 11.0, 3.0, color=ORANGE_MED, lw=2)

    _save(fig, "fig_4_1_architecture.png")


# ===========================================================================
# FIGURE 4.2 - Use Case Diagram
# ===========================================================================
def fig_4_2_usecase():
    print("Generating fig_4_2_usecase.png ...")
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Use Case Diagram - House Price Prediction System",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # System boundary
    sys_box = FancyBboxPatch((3.5, 0.3), 7.5, 9.2, boxstyle="round,pad=0.4",
                             facecolor=GRAY_LIGHT, edgecolor=BLUE_MED,
                             linewidth=2, linestyle="--")
    ax.add_patch(sys_box)
    ax.text(7.25, 9.2, "House Price Prediction System", ha="center",
            fontsize=13, fontweight="bold", color=BLUE_DARK)

    # User actor (left)
    def draw_stick_figure(ax, cx, cy, label):
        head = Circle((cx, cy + 0.35), 0.2, facecolor=WHITE,
                      edgecolor=BLUE_DARK, linewidth=2, zorder=5)
        ax.add_patch(head)
        # body
        ax.plot([cx, cx], [cy + 0.15, cy - 0.3], color=BLUE_DARK, lw=2, zorder=5)
        # arms
        ax.plot([cx - 0.25, cx + 0.25], [cy, cy], color=BLUE_DARK, lw=2, zorder=5)
        # legs
        ax.plot([cx, cx - 0.2], [cy - 0.3, cy - 0.6], color=BLUE_DARK, lw=2, zorder=5)
        ax.plot([cx, cx + 0.2], [cy - 0.3, cy - 0.6], color=BLUE_DARK, lw=2, zorder=5)
        ax.text(cx, cy - 0.85, label, ha="center", va="top", fontsize=11,
                fontweight="bold", color=BLUE_DARK, zorder=5)

    draw_stick_figure(ax, 1.5, 5.5, "User")

    # Admin actor (right)
    draw_stick_figure(ax, 12.8, 5.5, "Admin")

    # Use cases - ovals
    def draw_usecase(ax, cx, cy, text, fc=WHITE, ec=BLUE_MED):
        ellipse = mpatches.Ellipse((cx, cy), 3.0, 0.9,
                                   facecolor=fc, edgecolor=ec,
                                   linewidth=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha="center", va="center",
                fontsize=9, fontweight="bold", color=GRAY_DARK, zorder=4)

    user_cases = [
        (7.25, 8.5, "Register Account"),
        (7.25, 7.4, "Login"),
        (7.25, 6.3, "Enter House Features"),
        (7.25, 5.2, "Get Price Prediction"),
        (7.25, 4.1, "View Prediction History"),
        (7.25, 3.0, "View EDA Charts"),
        (7.25, 1.9, "Compare ML Models"),
        (7.25, 0.8, "Logout"),
    ]

    for cx, cy, text in user_cases:
        draw_usecase(ax, cx, cy, text)
        # Line from User to use case
        ax.plot([2.0, cx - 1.5], [5.2, cy], color=GRAY_MED, lw=1.2,
                linestyle="-", zorder=1)

    # Admin lines - admin can do everything user can + View Stats
    admin_cases_idx = [0, 1, 2, 3, 4, 5, 6, 7]
    for idx in admin_cases_idx:
        cx, cy, _ = user_cases[idx]
        ax.plot([12.3, cx + 1.5], [5.2, cy], color=GRAY_MED, lw=1.0,
                linestyle=":", zorder=1, alpha=0.5)

    # Inheritance arrow (Admin inherits User)
    ax.annotate("", xy=(2.0, 5.2), xytext=(12.3, 5.2),
                arrowprops=dict(arrowstyle="-|>", color=BLUE_MED,
                                lw=2, linestyle="dashed"))
    ax.text(7.25, 5.55, "<<inherits>>", ha="center", fontsize=8,
            color=BLUE_MED, style="italic")

    _save(fig, "fig_4_2_usecase.png")


# ===========================================================================
# FIGURE 4.3 - Class Diagram
# ===========================================================================
def fig_4_3_class():
    print("Generating fig_4_3_class.png ...")
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Class Diagram - House Price Prediction System",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    def draw_class_box(ax, x, y, w, h, class_name, attributes, methods,
                       header_color=BLUE_MED, header_text_color=WHITE):
        # Total height calculation
        n_attr = len(attributes)
        n_meth = len(methods)
        header_h = 0.6
        line_h = 0.35
        attr_h = max(n_attr * line_h, 0.4)
        meth_h = max(n_meth * line_h, 0.4)
        total_h = header_h + attr_h + meth_h

        # Header
        header = FancyBboxPatch((x, y + attr_h + meth_h), w, header_h,
                                boxstyle="round,pad=0.05",
                                facecolor=header_color, edgecolor=GRAY_DARK,
                                linewidth=1.5, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + attr_h + meth_h + header_h/2, class_name,
                ha="center", va="center", fontsize=11, fontweight="bold",
                color=header_text_color, zorder=4)

        # Attributes section
        attr_box = Rectangle((x, y + meth_h), w, attr_h,
                             facecolor=WHITE, edgecolor=GRAY_DARK,
                             linewidth=1.5, zorder=2)
        ax.add_patch(attr_box)
        for i, attr in enumerate(attributes):
            ax.text(x + 0.15, y + meth_h + attr_h - (i + 0.5) * line_h,
                    attr, ha="left", va="center", fontsize=8,
                    fontfamily="monospace", color=GRAY_DARK, zorder=3)

        # Methods section
        meth_box = Rectangle((x, y), w, meth_h,
                             facecolor=GRAY_LIGHT, edgecolor=GRAY_DARK,
                             linewidth=1.5, zorder=2)
        ax.add_patch(meth_box)
        for i, meth in enumerate(methods):
            ax.text(x + 0.15, y + meth_h - (i + 0.5) * line_h,
                    meth, ha="left", va="center", fontsize=8,
                    fontfamily="monospace", color=GRAY_DARK, zorder=3)

        return total_h

    # User class
    draw_class_box(ax, 0.5, 6.0, 3.2, 3.0, "User",
                   ["- id: Integer (PK)", "- username: String",
                    "- password: String (hash)", "- role: String"],
                   ["+ register()", "+ login()", "+ logout()"],
                   header_color=BLUE_MED)

    # Prediction class
    draw_class_box(ax, 5.2, 5.6, 3.5, 4.0, "Prediction",
                   ["- id: Integer (PK)", "- user_id: Integer (FK)",
                    "- longitude: Float", "- latitude: Float",
                    "- housing_median_age: Float",
                    "- total_rooms: Float", "- median_income: Float",
                    "- ocean_proximity: String",
                    "- predicted_price: Float", "- timestamp: DateTime"],
                   ["+ save()", "+ get_by_user()", "+ to_dict()"],
                   header_color=GREEN_MED)

    # MLModel class
    draw_class_box(ax, 10.0, 6.0, 3.5, 3.0, "MLModel",
                   ["- model_name: String", "- model_path: String",
                    "- r2_score: Float", "- mae: Float", "- rmse: Float"],
                   ["+ load()", "+ predict(features)",
                    "+ evaluate(X, y)", "+ get_metrics()"],
                   header_color=PURPLE_MED)

    # FlaskApp class (bottom center)
    draw_class_box(ax, 3.5, 0.5, 7.0, 3.0, "FlaskApp",
                   ["- app: Flask", "- db: SQLite", "- models: dict",
                    "- secret_key: String", "- dataset: DataFrame"],
                   ["+ init_routes()", "+ init_db()",
                    "+ load_models()", "+ run()"],
                   header_color=ORANGE_MED)

    # Relationships
    # User --1:N--> Prediction
    ax.annotate("", xy=(5.2, 7.5), xytext=(3.7, 7.5),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=1.5))
    ax.text(4.45, 7.7, "1       *", ha="center", fontsize=9,
            fontweight="bold", color=GRAY_DARK)
    ax.text(4.45, 7.25, "makes", ha="center", fontsize=8,
            style="italic", color=GRAY_MED)

    # MLModel <-- FlaskApp
    ax.annotate("", xy=(11.75, 6.0), xytext=(9.0, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=1.5,
                                linestyle="dashed"))
    ax.text(10.6, 5.0, "<<uses>>", ha="center", fontsize=8,
            style="italic", color=GRAY_MED, rotation=30)

    # User <-- FlaskApp
    ax.annotate("", xy=(2.1, 6.0), xytext=(5.0, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=1.5,
                                linestyle="dashed"))
    ax.text(3.3, 5.0, "<<manages>>", ha="center", fontsize=8,
            style="italic", color=GRAY_MED, rotation=-30)

    # Prediction <-- FlaskApp
    ax.annotate("", xy=(6.95, 5.6), xytext=(6.95, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=1.5,
                                linestyle="dashed"))
    ax.text(7.4, 4.7, "<<creates>>", ha="center", fontsize=8,
            style="italic", color=GRAY_MED)

    _save(fig, "fig_4_3_class.png")


# ===========================================================================
# FIGURE 4.4 - Sequence Diagram
# ===========================================================================
def fig_4_4_sequence():
    print("Generating fig_4_4_sequence.png ...")
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title("Sequence Diagram - Price Prediction Request",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # Lifeline positions
    actors = [
        (1.5, "User", BLUE_LIGHT, BLUE_MED),
        (4.5, "Browser", GREEN_LIGHT, GREEN_MED),
        (7.5, "Flask Server", ORANGE_LIGHT, ORANGE_MED),
        (10.5, "ML Model", PURPLE_LIGHT, PURPLE_MED),
        (13.0, "SQLite DB", TEAL_LIGHT, TEAL_MED),
    ]

    top_y = 10.0
    bottom_y = 0.5

    for cx, label, fc, ec in actors:
        box = FancyBboxPatch((cx - 0.7, top_y - 0.3), 1.4, 0.6,
                             boxstyle="round,pad=0.1",
                             facecolor=fc, edgecolor=ec, linewidth=2, zorder=3)
        ax.add_patch(box)
        ax.text(cx, top_y, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=GRAY_DARK, zorder=4)
        # Lifeline
        ax.plot([cx, cx], [top_y - 0.3, bottom_y], color=ec,
                linewidth=1.5, linestyle="--", zorder=1)
        # Bottom box copy
        box2 = FancyBboxPatch((cx - 0.7, bottom_y - 0.3), 1.4, 0.5,
                              boxstyle="round,pad=0.1",
                              facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=3)
        ax.add_patch(box2)
        ax.text(cx, bottom_y - 0.05, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color=GRAY_DARK, zorder=4)

    # Messages
    messages = [
        (9.2, 1.5, 4.5, "1. Fill prediction form", "->", BLUE_MED),
        (8.7, 4.5, 7.5, "2. POST /predict (features)", "->", GREEN_MED),
        (8.2, 7.5, 7.5, "3. Validate & preprocess", "->", ORANGE_MED),
        (7.7, 7.5, 10.5, "4. predict(features)", "->", PURPLE_MED),
        (7.2, 10.5, 7.5, "5. predicted_price", "<-", PURPLE_MED),
        (6.7, 7.5, 13.0, "6. INSERT prediction", "->", TEAL_MED),
        (6.2, 13.0, 7.5, "7. success", "<-", TEAL_MED),
        (5.7, 7.5, 4.5, "8. render result.html", "<-", GREEN_MED),
        (5.2, 4.5, 1.5, "9. Display prediction", "<-", BLUE_MED),
    ]

    for y, x1, x2, label, direction, color in messages:
        if direction == "->":
            ax.annotate("", xy=(x2 - 0.1, y), xytext=(x1 + 0.1, y),
                        arrowprops=dict(arrowstyle="-|>", color=color,
                                        lw=1.8))
        else:
            ax.annotate("", xy=(x2 + 0.1, y), xytext=(x1 - 0.1, y),
                        arrowprops=dict(arrowstyle="-|>", color=color,
                                        lw=1.8, linestyle="dashed"))

        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.15, label, ha="center", va="bottom",
                fontsize=8, color=GRAY_DARK, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", facecolor=WHITE,
                          edgecolor="none", alpha=0.85),
                zorder=5)

    # Activation bars
    for cx, _, _, _ in actors[1:]:
        activation = Rectangle((cx - 0.08, 5.0), 0.16, 4.5,
                               facecolor=GRAY_LIGHT, edgecolor=GRAY_MED,
                               linewidth=1, zorder=2, alpha=0.6)
        ax.add_patch(activation)

    _save(fig, "fig_4_4_sequence.png")


# ===========================================================================
# FIGURE 4.5 - Activity Diagram
# ===========================================================================
def fig_4_5_activity():
    print("Generating fig_4_5_activity.png ...")
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title("Activity Diagram - User Prediction Workflow",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # Start node
    start = Circle((6, 11.3), 0.2, facecolor=GRAY_DARK, edgecolor=GRAY_DARK,
                   linewidth=2, zorder=3)
    ax.add_patch(start)

    activities = [
        (6, 10.3, "Login / Register", BLUE_LIGHT, BLUE_MED),
        (6, 9.0, "Navigate to Predict Page", GREEN_LIGHT, GREEN_MED),
        (6, 7.7, "Enter House Features\n(9 input fields)", GREEN_LIGHT, GREEN_MED),
        (6, 6.4, "Submit Form", ORANGE_LIGHT, ORANGE_MED),
    ]

    for cx, cy, text, fc, ec in activities:
        _add_fancy_box(ax, (cx - 2.0, cy - 0.4), 4.0, 0.8, text,
                       fc, ec, fontsize=10, fontweight="bold", text_color=GRAY_DARK)

    # Decision diamond - Validate
    diamond_y = 5.3
    diamond = plt.Polygon([(6, 5.7), (7.2, 5.3), (6, 4.9), (4.8, 5.3)],
                          facecolor=YELLOW_LIGHT, edgecolor=YELLOW_MED,
                          linewidth=2, zorder=3)
    ax.add_patch(diamond)
    ax.text(6, 5.3, "Valid?", ha="center", va="center",
            fontsize=10, fontweight="bold", color=GRAY_DARK, zorder=4)

    # No path - back to Enter Features
    ax.annotate("", xy=(4.0, 7.3), xytext=(4.8, 5.3),
                arrowprops=dict(arrowstyle="-|>", color=RED_MED, lw=2))
    ax.text(3.5, 6.3, "No\n(Show Error)", ha="center", fontsize=9,
            color=RED_MED, fontweight="bold")

    # Yes path continues
    more_activities = [
        (6, 4.1, "Run ML Prediction\n(Gradient Boosting)", PURPLE_LIGHT, PURPLE_MED),
        (6, 2.8, "Display Predicted Price", TEAL_LIGHT, TEAL_MED),
        (6, 1.5, "Save to Prediction History", ORANGE_LIGHT, ORANGE_MED),
    ]

    for cx, cy, text, fc, ec in more_activities:
        _add_fancy_box(ax, (cx - 2.0, cy - 0.4), 4.0, 0.8, text,
                       fc, ec, fontsize=10, fontweight="bold", text_color=GRAY_DARK)

    ax.text(6.4, 4.85, "Yes", ha="left", fontsize=9, color=GREEN_DARK,
            fontweight="bold")

    # Decision: New prediction or Logout
    diamond2_y = 0.4
    diamond2 = plt.Polygon([(6, 0.8), (7.5, 0.4), (6, 0.0), (4.5, 0.4)],
                           facecolor=YELLOW_LIGHT, edgecolor=YELLOW_MED,
                           linewidth=2, zorder=3)
    ax.add_patch(diamond2)
    ax.text(6, 0.4, "Again?", ha="center", va="center",
            fontsize=10, fontweight="bold", color=GRAY_DARK, zorder=4)

    # Yes - loop back
    ax.annotate("", xy=(10.0, 9.0), xytext=(10.0, 0.4),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_MED, lw=2))
    ax.plot([7.5, 10.0], [0.4, 0.4], color=GREEN_MED, lw=2)
    ax.plot([10.0, 10.0], [9.0, 9.0], color=GREEN_MED, lw=2)
    ax.annotate("", xy=(8.0, 9.0), xytext=(10.0, 9.0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_MED, lw=2))
    ax.text(10.3, 4.5, "Yes", ha="left", fontsize=9, color=GREEN_DARK,
            fontweight="bold")

    # No - Logout / End
    ax.plot([4.5, 2.0], [0.4, 0.4], color=RED_MED, lw=2)
    _add_fancy_box(ax, (0.5, 0.0), 1.8, 0.8, "Logout",
                   RED_LIGHT, RED_MED, fontsize=10, fontweight="bold",
                   text_color=RED_MED)
    ax.text(3.5, 0.6, "No", ha="center", fontsize=9, color=RED_MED,
            fontweight="bold")

    # End node
    end = Circle((1.4, -0.6), 0.2, facecolor=WHITE, edgecolor=GRAY_DARK,
                 linewidth=3, zorder=3)
    ax.add_patch(end)
    end_inner = Circle((1.4, -0.6), 0.12, facecolor=GRAY_DARK,
                       edgecolor=GRAY_DARK, linewidth=1, zorder=4)
    ax.add_patch(end_inner)
    ax.plot([1.4, 1.4], [0.0, -0.4], color=GRAY_DARK, lw=2)

    # Vertical arrows between sequential activities
    arrow_pairs = [
        (6, 11.1, 6, 10.7),
        (6, 9.9, 6, 9.4),
        (6, 8.6, 6, 8.1),
        (6, 7.3, 6, 6.8),
        (6, 6.0, 6, 5.7),
        (6, 4.9, 6, 4.5),
        (6, 3.7, 6, 3.2),
        (6, 2.4, 6, 1.9),
        (6, 1.1, 6, 0.8),
    ]
    for x1, y1, x2, y2 in arrow_pairs:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=1.5))

    ax.set_ylim(-1, 12)
    _save(fig, "fig_4_5_activity.png")


# ===========================================================================
# FIGURE 4.6 - UI Wireframe
# ===========================================================================
def fig_4_6_wireframe():
    print("Generating fig_4_6_wireframe.png ...")
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title("UI Wireframe - Price Prediction Page",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # Browser chrome
    browser = FancyBboxPatch((0.5, 0.3), 11.0, 11.2, boxstyle="round,pad=0.2",
                             facecolor="#1a202c", edgecolor=GRAY_MED,
                             linewidth=2, zorder=1)
    ax.add_patch(browser)

    # Title bar
    title_bar = Rectangle((0.5, 10.8), 11.0, 0.7,
                           facecolor="#2d3748", edgecolor=GRAY_MED,
                           linewidth=1, zorder=2)
    ax.add_patch(title_bar)
    # Window buttons
    for i, c in enumerate(["#fc8181", "#fefcbf", "#9ae6b4"]):
        dot = Circle((1.0 + i * 0.4, 11.15), 0.1, facecolor=c,
                     edgecolor="none", zorder=3)
        ax.add_patch(dot)
    ax.text(6.0, 11.15, "localhost:5000/predict", ha="center", va="center",
            fontsize=9, color=GRAY_MED, fontfamily="monospace", zorder=3)

    # Navbar
    navbar = Rectangle((0.7, 10.0), 10.6, 0.7,
                        facecolor=BLUE_MED, edgecolor="none", zorder=2)
    ax.add_patch(navbar)
    nav_items = ["Home", "Predict", "History", "Visualize", "Dashboard", "About", "Logout"]
    nx = 1.5
    for item in nav_items:
        weight = "bold" if item == "Predict" else "normal"
        bg_c = BLUE_DARK if item == "Predict" else BLUE_MED
        _add_fancy_box(ax, (nx - 0.05, 10.1), 1.3, 0.5, item,
                       bg_c, "none", fontsize=8, fontweight=weight,
                       text_color=WHITE, boxstyle="round,pad=0.1")
        nx += 1.5

    # Page title
    ax.text(6.0, 9.5, "Predict House Price", ha="center", va="center",
            fontsize=16, fontweight="bold", color=WHITE, zorder=3)
    ax.text(6.0, 9.1, "Enter housing features below to get an instant prediction",
            ha="center", va="center", fontsize=9, color=GRAY_MED, zorder=3)

    # Form card
    form_card = FancyBboxPatch((1.5, 2.2), 9.0, 6.6, boxstyle="round,pad=0.3",
                               facecolor="#2d3748", edgecolor="#4a5568",
                               linewidth=1.5, zorder=2)
    ax.add_patch(form_card)

    # Input fields - 2 columns
    fields_left = [
        "Longitude", "Latitude", "Housing Median Age",
        "Total Rooms", "Total Bedrooms"
    ]
    fields_right = [
        "Population", "Households", "Median Income",
        "Ocean Proximity", ""
    ]

    fy = 8.3
    for i, (fl, fr) in enumerate(zip(fields_left, fields_right)):
        if fl:
            ax.text(2.0, fy + 0.25, fl, fontsize=8, color="#a0aec0",
                    fontweight="bold", zorder=3)
            inp_l = FancyBboxPatch((2.0, fy - 0.25), 3.6, 0.4,
                                   boxstyle="round,pad=0.1",
                                   facecolor="#4a5568", edgecolor="#718096",
                                   linewidth=1, zorder=3)
            ax.add_patch(inp_l)
            placeholder = "-122.23" if fl == "Longitude" else "37.88" if fl == "Latitude" else ""
            ax.text(2.2, fy - 0.05, placeholder, fontsize=8, color="#718096",
                    zorder=4)

        if fr:
            ax.text(6.5, fy + 0.25, fr, fontsize=8, color="#a0aec0",
                    fontweight="bold", zorder=3)
            if fr == "Ocean Proximity":
                # Dropdown
                inp_r = FancyBboxPatch((6.5, fy - 0.25), 3.6, 0.4,
                                       boxstyle="round,pad=0.1",
                                       facecolor="#4a5568", edgecolor="#718096",
                                       linewidth=1, zorder=3)
                ax.add_patch(inp_r)
                ax.text(6.7, fy - 0.05, "NEAR BAY  v", fontsize=8,
                        color="#a0aec0", zorder=4)
            else:
                inp_r = FancyBboxPatch((6.5, fy - 0.25), 3.6, 0.4,
                                       boxstyle="round,pad=0.1",
                                       facecolor="#4a5568", edgecolor="#718096",
                                       linewidth=1, zorder=3)
                ax.add_patch(inp_r)

        fy -= 1.1

    # Predict button
    predict_btn = FancyBboxPatch((3.5, 2.5), 5.0, 0.7,
                                 boxstyle="round,pad=0.15",
                                 facecolor=GREEN_MED, edgecolor=GREEN_DARK,
                                 linewidth=2, zorder=3)
    ax.add_patch(predict_btn)
    ax.text(6.0, 2.85, "Predict Price", ha="center", va="center",
            fontsize=13, fontweight="bold", color=WHITE, zorder=4)

    # Result area
    result_card = FancyBboxPatch((2.5, 0.6), 7.0, 1.3, boxstyle="round,pad=0.2",
                                 facecolor="#22543d", edgecolor=GREEN_MED,
                                 linewidth=2, zorder=2)
    ax.add_patch(result_card)
    ax.text(6.0, 1.55, "Predicted Price", ha="center", va="center",
            fontsize=10, color="#9ae6b4", zorder=3)
    ax.text(6.0, 1.05, "$256,430.00", ha="center", va="center",
            fontsize=20, fontweight="bold", color=WHITE, zorder=3)

    _save(fig, "fig_4_6_wireframe.png")


# ===========================================================================
# FIGURE 4.7 - ML Pipeline
# ===========================================================================
def fig_4_7_ml_pipeline():
    print("Generating fig_4_7_ml_pipeline.png ...")
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Machine Learning Pipeline - House Price Prediction",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    # Pipeline stages
    stages = [
        {
            "x": 0.3, "y": 6.5, "w": 2.4, "h": 2.5,
            "title": "Raw Data",
            "desc": "housing.csv\n10,000 rows\n9 features\n+ target",
            "fc": BLUE_LIGHT, "ec": BLUE_MED, "tc": BLUE_DARK,
        },
        {
            "x": 3.2, "y": 6.5, "w": 2.6, "h": 2.5,
            "title": "Preprocessing",
            "desc": "Handle NaN\nEncode categories\nRemove outliers\nScale features",
            "fc": GREEN_LIGHT, "ec": GREEN_MED, "tc": GREEN_DARK,
        },
        {
            "x": 6.3, "y": 6.5, "w": 2.4, "h": 2.5,
            "title": "Feature\nEngineering",
            "desc": "One-Hot Encoding\n(ocean_proximity)\nFeature selection\nCorrelation check",
            "fc": TEAL_LIGHT, "ec": TEAL_MED, "tc": GRAY_DARK,
        },
        {
            "x": 9.2, "y": 6.5, "w": 2.2, "h": 2.5,
            "title": "Train/Test\nSplit",
            "desc": "80% Training\n20% Testing\nRandom state=42",
            "fc": YELLOW_LIGHT, "ec": YELLOW_MED, "tc": GRAY_DARK,
        },
        {
            "x": 11.9, "y": 6.5, "w": 3.5, "h": 2.5,
            "title": "Train 5 Models",
            "desc": "Linear Regression\nRidge Regression\nDecision Tree\nRandom Forest\nGradient Boosting",
            "fc": ORANGE_LIGHT, "ec": ORANGE_MED, "tc": ORANGE_DARK,
        },
    ]

    for s in stages:
        # Title box
        title_box = FancyBboxPatch((s["x"], s["y"] + s["h"] - 0.7),
                                   s["w"], 0.7,
                                   boxstyle="round,pad=0.1",
                                   facecolor=s["ec"], edgecolor=s["ec"],
                                   linewidth=1.5, zorder=3)
        ax.add_patch(title_box)
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 0.35, s["title"],
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=WHITE, zorder=4)

        # Body box
        body_box = FancyBboxPatch((s["x"], s["y"]),
                                  s["w"], s["h"] - 0.7,
                                  boxstyle="round,pad=0.1",
                                  facecolor=s["fc"], edgecolor=s["ec"],
                                  linewidth=1.5, zorder=2)
        ax.add_patch(body_box)
        ax.text(s["x"] + s["w"]/2, s["y"] + (s["h"] - 0.7)/2, s["desc"],
                ha="center", va="center", fontsize=8.5, color=s["tc"],
                zorder=3, linespacing=1.4)

    # Arrows between top stages
    arrow_positions = [
        (2.7, 7.75, 3.2, 7.75),
        (5.8, 7.75, 6.3, 7.75),
        (8.7, 7.75, 9.2, 7.75),
        (11.4, 7.75, 11.9, 7.75),
    ]
    for x1, y1, x2, y2 in arrow_positions:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK,
                                    lw=2.5))

    # Bottom row: Evaluate -> Select -> Deploy
    bottom_stages = [
        {
            "x": 3.0, "y": 1.5, "w": 3.0, "h": 2.5,
            "title": "Evaluate Models",
            "desc": "R-squared (R2)\nMean Absolute Error\nRoot Mean Sq Error\nCross Validation",
            "fc": PURPLE_LIGHT, "ec": PURPLE_MED, "tc": GRAY_DARK,
        },
        {
            "x": 7.0, "y": 1.5, "w": 2.8, "h": 2.5,
            "title": "Select Best",
            "desc": "Gradient Boosting\nHighest R2 Score\nLowest RMSE\nBest Generalization",
            "fc": GREEN_LIGHT, "ec": GREEN_MED, "tc": GREEN_DARK,
        },
        {
            "x": 10.8, "y": 1.5, "w": 2.8, "h": 2.5,
            "title": "Deploy Model",
            "desc": "Save with joblib\n(.pkl file)\nLoad in Flask\nServe predictions",
            "fc": BLUE_LIGHT, "ec": BLUE_MED, "tc": BLUE_DARK,
        },
    ]

    for s in bottom_stages:
        title_box = FancyBboxPatch((s["x"], s["y"] + s["h"] - 0.7),
                                   s["w"], 0.7,
                                   boxstyle="round,pad=0.1",
                                   facecolor=s["ec"], edgecolor=s["ec"],
                                   linewidth=1.5, zorder=3)
        ax.add_patch(title_box)
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 0.35, s["title"],
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=WHITE, zorder=4)

        body_box = FancyBboxPatch((s["x"], s["y"]),
                                  s["w"], s["h"] - 0.7,
                                  boxstyle="round,pad=0.1",
                                  facecolor=s["fc"], edgecolor=s["ec"],
                                  linewidth=1.5, zorder=2)
        ax.add_patch(body_box)
        ax.text(s["x"] + s["w"]/2, s["y"] + (s["h"] - 0.7)/2, s["desc"],
                ha="center", va="center", fontsize=8.5, color=s["tc"],
                zorder=3, linespacing=1.4)

    # Arrow from Train 5 Models down to Evaluate
    ax.annotate("", xy=(4.5, 4.0), xytext=(13.65, 6.5),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=2.5,
                                connectionstyle="arc3,rad=0.3"))

    # Arrow Evaluate -> Select
    ax.annotate("", xy=(7.0, 2.75), xytext=(6.0, 2.75),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=2.5))

    # Arrow Select -> Deploy
    ax.annotate("", xy=(10.8, 2.75), xytext=(9.8, 2.75),
                arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK, lw=2.5))

    # Pipeline flow label
    ax.text(8.0, 5.5, "MODEL TRAINING & EVALUATION PIPELINE",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=GRAY_MED, style="italic", zorder=1)

    _save(fig, "fig_4_7_ml_pipeline.png")


# ===========================================================================
# FIGURE 5.1 - Development Phases
# ===========================================================================
def fig_5_1_phases():
    print("Generating fig_5_1_phases.png ...")
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Development Phases - Software Development Life Cycle",
                 fontsize=16, fontweight="bold", color=BLUE_DARK, pad=20)

    phases = [
        {
            "title": "Phase 1\nRequirements",
            "desc": "Gather functional &\nnon-functional requirements.\nDefine scope, features,\nand user stories.",
            "color_bg": BLUE_LIGHT, "color_border": BLUE_MED,
            "color_title": BLUE_DARK,
            "icon_items": ["User stories", "Feature list", "Tech stack selection"],
        },
        {
            "title": "Phase 2\nDesign",
            "desc": "System architecture,\nUML diagrams, database\nschema, UI mockups.",
            "color_bg": GREEN_LIGHT, "color_border": GREEN_MED,
            "color_title": GREEN_DARK,
            "icon_items": ["Architecture diagram", "Class/Use case diagrams", "DB schema design"],
        },
        {
            "title": "Phase 3\nImplementation",
            "desc": "Build Flask app, train ML\nmodels, create database,\nimplement all routes.",
            "color_bg": ORANGE_LIGHT, "color_border": ORANGE_MED,
            "color_title": ORANGE_DARK,
            "icon_items": ["Flask routes & templates", "ML model training", "SQLite database setup"],
        },
        {
            "title": "Phase 4\nTesting",
            "desc": "Unit tests, integration\ntests, model validation,\nuser acceptance testing.",
            "color_bg": PURPLE_LIGHT, "color_border": PURPLE_MED,
            "color_title": GRAY_DARK,
            "icon_items": ["Model accuracy tests", "Route testing", "UI/UX validation"],
        },
        {
            "title": "Phase 5\nDeployment",
            "desc": "Deploy application,\nconfigure server,\nmonitor performance.",
            "color_bg": TEAL_LIGHT, "color_border": TEAL_MED,
            "color_title": GRAY_DARK,
            "icon_items": ["Server configuration", "Model deployment", "User training"],
        },
    ]

    n = len(phases)
    card_w = 2.2
    gap = 0.35
    total_w = n * card_w + (n - 1) * gap
    start_x = (14 - total_w) / 2

    # Connecting arrow line across top
    arrow_y = 8.8
    for i in range(n - 1):
        x1 = start_x + (i + 1) * card_w + i * gap
        x2 = x1 + gap
        ax.annotate("", xy=(x2, arrow_y), xytext=(x1, arrow_y),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY_DARK,
                                    lw=3))

    for i, phase in enumerate(phases):
        x = start_x + i * (card_w + gap)

        # Phase number circle
        circle = Circle((x + card_w / 2, arrow_y), 0.35,
                        facecolor=phase["color_border"],
                        edgecolor=WHITE, linewidth=3, zorder=5)
        ax.add_patch(circle)
        ax.text(x + card_w / 2, arrow_y, str(i + 1), ha="center", va="center",
                fontsize=14, fontweight="bold", color=WHITE, zorder=6)

        # Card
        card_h = 7.0
        card_y = 1.0

        # Header
        header = FancyBboxPatch((x, card_y + card_h - 1.3), card_w, 1.3,
                                boxstyle="round,pad=0.15",
                                facecolor=phase["color_border"],
                                edgecolor=phase["color_border"],
                                linewidth=2, zorder=3)
        ax.add_patch(header)
        ax.text(x + card_w / 2, card_y + card_h - 0.65, phase["title"],
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=WHITE, zorder=4, linespacing=1.3)

        # Body
        body = FancyBboxPatch((x, card_y), card_w, card_h - 1.3,
                              boxstyle="round,pad=0.15",
                              facecolor=phase["color_bg"],
                              edgecolor=phase["color_border"],
                              linewidth=2, zorder=2)
        ax.add_patch(body)

        # Description
        ax.text(x + card_w / 2, card_y + card_h - 2.2, phase["desc"],
                ha="center", va="top", fontsize=8, color=GRAY_DARK,
                zorder=3, linespacing=1.5)

        # Separator line
        sep_y = card_y + card_h - 4.0
        ax.plot([x + 0.2, x + card_w - 0.2], [sep_y, sep_y],
                color=phase["color_border"], lw=1, alpha=0.5, zorder=3)

        # Deliverables / Key items
        ax.text(x + card_w / 2, sep_y - 0.2, "Key Deliverables:",
                ha="center", va="top", fontsize=7.5, fontweight="bold",
                color=phase["color_title"], zorder=3)

        item_y = sep_y - 0.6
        for item in phase["icon_items"]:
            ax.text(x + 0.25, item_y, f"  {item}", ha="left", va="top",
                    fontsize=7, color=GRAY_DARK, zorder=3)
            # bullet
            bullet = Circle((x + 0.25, item_y - 0.05), 0.06,
                            facecolor=phase["color_border"],
                            edgecolor="none", zorder=3)
            ax.add_patch(bullet)
            item_y -= 0.5

        # Vertical line from circle to card
        ax.plot([x + card_w / 2, x + card_w / 2],
                [arrow_y - 0.35, card_y + card_h],
                color=phase["color_border"], lw=2, linestyle=":", zorder=1)

    _save(fig, "fig_5_1_phases.png")


# ===========================================================================
# Main
# ===========================================================================
def main():
    print("=" * 60)
    print("  Generating figures for C4 House Price Prediction Project")
    print("=" * 60)
    print()

    fig_1_1_comparison()
    fig_4_1_architecture()
    fig_4_2_usecase()
    fig_4_3_class()
    fig_4_4_sequence()
    fig_4_5_activity()
    fig_4_6_wireframe()
    fig_4_7_ml_pipeline()
    fig_5_1_phases()

    print()
    print("=" * 60)
    print(f"  All 9 figures generated in: {FIGURES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
