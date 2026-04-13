#!/usr/bin/env python3
"""
Generate 9 architectural/UML diagram figures for the B12 AI Medical Chatbot project.
Uses matplotlib with a medical/healthcare color theme.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ── Color Theme ──
BLUE_PRIMARY = '#2196F3'
BLUE_DARK = '#1565C0'
GREEN_PRIMARY = '#4CAF50'
GREEN_DARK = '#388E3C'
BLUE_LIGHT = '#E3F2FD'
GREEN_LIGHT = '#E8F5E9'
WHITE = '#FFFFFF'
GRAY_LIGHT = '#F5F5F5'
GRAY_MED = '#BDBDBD'
GRAY_DARK = '#616161'
ORANGE = '#FF9800'
RED_SOFT = '#EF5350'
PURPLE = '#7E57C2'
TEAL = '#26A69A'

OUTPUT_DIR = '/Users/shoukathali/lord-major-projects/IV-B Projects/IV-B Projects/B12/figures'
DPI = 200


def draw_rounded_box(ax, x, y, w, h, text, facecolor=BLUE_LIGHT, edgecolor=BLUE_PRIMARY,
                     fontsize=9, fontweight='normal', textcolor='#212121', lw=1.5, alpha=1.0,
                     zorder=2, text_y_offset=0, ha='center', va='center', radius=0.02):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                         facecolor=facecolor, edgecolor=edgecolor, linewidth=lw,
                         alpha=alpha, zorder=zorder)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2 + text_y_offset, text, ha=ha, va=va,
            fontsize=fontsize, fontweight=fontweight, color=textcolor, zorder=zorder + 1,
            wrap=True)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color=GRAY_DARK, lw=1.5, style='->', zorder=1):
    """Draw an arrow between two points."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw),
                zorder=zorder)


def draw_arrow_label(ax, x1, y1, x2, y2, label='', color=GRAY_DARK, lw=1.5, fontsize=7):
    """Draw an arrow with a label at midpoint."""
    draw_arrow(ax, x1, y1, x2, y2, color=color, lw=lw)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if label:
        ax.text(mx + 0.01, my + 0.01, label, fontsize=fontsize, color=color,
                ha='center', va='bottom', zorder=5)


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1: Comparison - Traditional Healthcare vs AI Chatbot
# ═══════════════════════════════════════════════════════════════════════════════
def fig_1_1_comparison():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.5, 0.96, 'Traditional Healthcare vs AI Medical Chatbot',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.92, 'Figure 1.1 — Comparison of Patient Journey',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    # Divider
    ax.plot([0.5, 0.5], [0.05, 0.87], color=GRAY_MED, lw=1.5, ls='--', zorder=1)

    # ── LEFT: Traditional ──
    ax.text(0.25, 0.87, 'Traditional Healthcare', ha='center', va='top',
            fontsize=14, fontweight='bold', color=RED_SOFT)

    trad_steps = [
        ('Patient Feels\nUnwell', RED_SOFT, '#FFEBEE'),
        ('Search for\nNearby Clinic', RED_SOFT, '#FFEBEE'),
        ('Travel &\nWait in Queue', RED_SOFT, '#FFEBEE'),
        ('Describe Symptoms\nto Doctor', RED_SOFT, '#FFEBEE'),
        ('Doctor Examines\n& Diagnoses', RED_SOFT, '#FFEBEE'),
        ('Receive\nPrescription', RED_SOFT, '#FFEBEE'),
    ]
    bw, bh = 0.18, 0.08
    sx = 0.16
    times = ['', '~15 min', '~30-120 min', '~10 min', '~15 min', '~5 min']

    for i, (label, ec, fc) in enumerate(trad_steps):
        sy = 0.78 - i * 0.12
        draw_rounded_box(ax, sx, sy, bw, bh, label, facecolor=fc, edgecolor=ec,
                         fontsize=9, fontweight='bold', textcolor='#B71C1C')
        if i < len(trad_steps) - 1:
            draw_arrow(ax, sx + bw / 2, sy, sx + bw / 2, sy - 0.04, color=RED_SOFT, lw=2)
        # Time label
        ax.text(sx + bw + 0.01, sy + bh / 2, times[i], fontsize=7, color=GRAY_DARK, va='center')

    ax.text(0.25, 0.06, 'Total: 1–4 hours', ha='center', fontsize=11,
            fontweight='bold', color=RED_SOFT,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFCDD2', edgecolor=RED_SOFT))

    # ── RIGHT: AI Chatbot ──
    ax.text(0.75, 0.87, 'AI Medical Chatbot', ha='center', va='top',
            fontsize=14, fontweight='bold', color=GREEN_DARK)

    ai_steps = [
        ('Patient Feels\nUnwell', GREEN_DARK, GREEN_LIGHT),
        ('Open Chatbot\nApp / Website', GREEN_DARK, GREEN_LIGHT),
        ('Type Symptoms\nin Chat', GREEN_DARK, GREEN_LIGHT),
        ('NLP Processes\n& Matches', GREEN_DARK, GREEN_LIGHT),
        ('KNN Predicts\nDisease (k=5)', GREEN_DARK, GREEN_LIGHT),
        ('Instant Result +\nSeverity & Advice', GREEN_DARK, GREEN_LIGHT),
    ]
    sx2 = 0.66
    times2 = ['', 'Instant', '~1 min', '< 1 sec', '< 1 sec', 'Instant']

    for i, (label, ec, fc) in enumerate(ai_steps):
        sy = 0.78 - i * 0.12
        draw_rounded_box(ax, sx2, sy, bw, bh, label, facecolor=fc, edgecolor=ec,
                         fontsize=9, fontweight='bold', textcolor='#1B5E20')
        if i < len(ai_steps) - 1:
            draw_arrow(ax, sx2 + bw / 2, sy, sx2 + bw / 2, sy - 0.04, color=GREEN_DARK, lw=2)
        ax.text(sx2 + bw + 0.01, sy + bh / 2, times2[i], fontsize=7, color=GRAY_DARK, va='center')

    ax.text(0.75, 0.06, 'Total: ~2 minutes', ha='center', fontsize=11,
            fontweight='bold', color=GREEN_DARK,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#C8E6C9', edgecolor=GREEN_DARK))

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_1_1_comparison.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_1_1_comparison.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2: System Architecture (3-layer + Data)
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_1_architecture():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.97, 'System Architecture — AI Medical Chatbot',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.93, 'Figure 4.1 — Three-Layer Architecture with Data Store',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    # ── Layer 1: Web Layer ──
    layer_w, layer_h = 0.88, 0.15
    lx = 0.06

    # Web Layer background
    web_bg = FancyBboxPatch((lx, 0.74), layer_w, layer_h, boxstyle="round,pad=0.01",
                            facecolor=BLUE_LIGHT, edgecolor=BLUE_PRIMARY, linewidth=2, alpha=0.5)
    ax.add_patch(web_bg)
    ax.text(lx + 0.01, 0.74 + layer_h - 0.01, 'WEB LAYER', fontsize=12, fontweight='bold',
            color=BLUE_DARK, va='top')

    web_items = ['Flask Server\n(Port 5000)', 'Landing Page\n(index.html)', 'Chat UI\n(chat.html)',
                 'jQuery AJAX\n(Async Calls)']
    for i, item in enumerate(web_items):
        draw_rounded_box(ax, 0.09 + i * 0.22, 0.76, 0.18, 0.10, item,
                         facecolor=WHITE, edgecolor=BLUE_PRIMARY, fontsize=9, fontweight='bold',
                         textcolor=BLUE_DARK)

    # Arrow down
    draw_arrow(ax, 0.5, 0.74, 0.5, 0.70, color=BLUE_DARK, lw=2.5)
    ax.text(0.52, 0.72, 'HTTP POST /chat', fontsize=8, color=BLUE_DARK, va='center')

    # ── Layer 2: NLP Layer ──
    nlp_bg = FancyBboxPatch((lx, 0.50), layer_w, layer_h + 0.03, boxstyle="round,pad=0.01",
                            facecolor=GREEN_LIGHT, edgecolor=GREEN_PRIMARY, linewidth=2, alpha=0.5)
    ax.add_patch(nlp_bg)
    ax.text(lx + 0.01, 0.50 + layer_h + 0.03 - 0.01, 'NLP PROCESSING LAYER', fontsize=12,
            fontweight='bold', color=GREEN_DARK, va='top')

    nlp_items = ['spaCy\nPreprocessor', 'Jaccard Set\nMatcher', 'WordNet WUP\nSimilarity',
                 'Synonym\nSuggester']
    for i, item in enumerate(nlp_items):
        draw_rounded_box(ax, 0.09 + i * 0.22, 0.52, 0.18, 0.10, item,
                         facecolor=WHITE, edgecolor=GREEN_PRIMARY, fontsize=9, fontweight='bold',
                         textcolor=GREEN_DARK)

    # Arrow down
    draw_arrow(ax, 0.5, 0.50, 0.5, 0.46, color=GREEN_DARK, lw=2.5)
    ax.text(0.52, 0.48, 'Matched Symptoms', fontsize=8, color=GREEN_DARK, va='center')

    # ── Layer 3: ML Layer ──
    ml_bg = FancyBboxPatch((lx, 0.28), 0.42, 0.14, boxstyle="round,pad=0.01",
                           facecolor='#EDE7F6', edgecolor=PURPLE, linewidth=2, alpha=0.5)
    ax.add_patch(ml_bg)
    ax.text(lx + 0.01, 0.28 + 0.14 - 0.01, 'ML CLASSIFICATION LAYER', fontsize=11,
            fontweight='bold', color=PURPLE, va='top')

    ml_items = ['One-Hot\nEncoder (132-D)', 'KNN Classifier\n(k=5, Distance)']
    for i, item in enumerate(ml_items):
        draw_rounded_box(ax, 0.09 + i * 0.22, 0.30, 0.18, 0.09, item,
                         facecolor=WHITE, edgecolor=PURPLE, fontsize=9, fontweight='bold',
                         textcolor=PURPLE)

    # ── Data Layer ──
    data_bg = FancyBboxPatch((0.50, 0.28), 0.44, 0.14, boxstyle="round,pad=0.01",
                             facecolor='#FFF3E0', edgecolor=ORANGE, linewidth=2, alpha=0.5)
    ax.add_patch(data_bg)
    ax.text(0.51, 0.28 + 0.14 - 0.01, 'DATA LAYER', fontsize=11,
            fontweight='bold', color='#E65100', va='top')

    data_items = ['Training.csv\n(4920 Records)', 'symptom_severity\n& description.csv',
                  'knn.pkl\n(Saved Model)', 'DATA.json\n(Intents)']
    for i, item in enumerate(data_items):
        draw_rounded_box(ax, 0.52 + i * 0.105, 0.295, 0.09, 0.09, item,
                         facecolor=WHITE, edgecolor=ORANGE, fontsize=7, fontweight='bold',
                         textcolor='#E65100')

    # Arrow between ML and Data
    draw_arrow(ax, 0.48, 0.35, 0.50, 0.35, color=GRAY_DARK, lw=2, style='<->')

    # ── Result arrow ──
    draw_arrow(ax, 0.27, 0.28, 0.27, 0.22, color=PURPLE, lw=2.5)

    # Result box
    draw_rounded_box(ax, 0.12, 0.10, 0.76, 0.10, 
                     'PREDICTION OUTPUT:  Disease Name  |  Description  |  Severity Score  |  Precautions',
                     facecolor='#E0F7FA', edgecolor=TEAL, fontsize=11, fontweight='bold',
                     textcolor='#00695C')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_1_architecture.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_1_architecture.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Use Case Diagram
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_2_usecase():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.97, 'Use Case Diagram — AI Medical Chatbot',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.93, 'Figure 4.2 — Actor–Use Case Relationships',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    # System boundary
    sys_box = FancyBboxPatch((0.22, 0.05), 0.56, 0.84, boxstyle="round,pad=0.02",
                             facecolor=GRAY_LIGHT, edgecolor=BLUE_DARK, linewidth=2, 
                             linestyle='--', alpha=0.3)
    ax.add_patch(sys_box)
    ax.text(0.5, 0.88, 'AI Medical Chatbot System', ha='center', fontsize=13,
            fontweight='bold', color=BLUE_DARK,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BLUE_LIGHT, edgecolor=BLUE_DARK))

    def draw_actor(ax, x, y, label, color):
        # Head
        circle = plt.Circle((x, y + 0.04), 0.015, facecolor=color, edgecolor=color, lw=1.5, zorder=5)
        ax.add_patch(circle)
        # Body
        ax.plot([x, x], [y + 0.025, y - 0.01], color=color, lw=2, zorder=5)
        # Arms
        ax.plot([x - 0.02, x + 0.02], [y + 0.015, y + 0.015], color=color, lw=2, zorder=5)
        # Legs
        ax.plot([x, x - 0.015], [y - 0.01, y - 0.035], color=color, lw=2, zorder=5)
        ax.plot([x, x + 0.015], [y - 0.01, y - 0.035], color=color, lw=2, zorder=5)
        ax.text(x, y - 0.055, label, ha='center', fontsize=10, fontweight='bold', color=color)

    # Actors
    draw_actor(ax, 0.08, 0.65, 'Patient', BLUE_DARK)
    draw_actor(ax, 0.92, 0.72, 'NLP Engine', GREEN_DARK)
    draw_actor(ax, 0.92, 0.35, 'ML Classifier', PURPLE)

    # Use cases — ellipses
    def draw_usecase(ax, cx, cy, text, color=BLUE_PRIMARY):
        ellipse = mpatches.Ellipse((cx, cy), 0.22, 0.07, facecolor=WHITE,
                                    edgecolor=color, linewidth=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=color, zorder=4)

    # Patient use cases (left-center)
    patient_ucs = [
        (0.38, 0.82, 'Provide Personal Info'),
        (0.38, 0.72, 'Describe Symptom'),
        (0.38, 0.62, 'Answer Follow-up'),
        (0.38, 0.52, 'View Prediction'),
        (0.38, 0.42, 'Get Severity & Advice'),
    ]
    for cx, cy, text in patient_ucs:
        draw_usecase(ax, cx, cy, text, BLUE_PRIMARY)
        ax.plot([0.12, cx - 0.11], [0.65, cy], color=BLUE_DARK, lw=1, zorder=2)

    # NLP use cases (right-center)
    nlp_ucs = [
        (0.62, 0.82, 'Tokenize & Lemmatize'),
        (0.62, 0.72, 'Jaccard Set Match'),
        (0.62, 0.62, 'WUP Similarity Match'),
        (0.62, 0.52, 'Suggest Synonym'),
    ]
    for cx, cy, text in nlp_ucs:
        draw_usecase(ax, cx, cy, text, GREEN_PRIMARY)
        ax.plot([0.88, cx + 0.11], [0.72, cy], color=GREEN_DARK, lw=1, zorder=2)

    # ML use cases
    ml_ucs = [
        (0.62, 0.35, 'Encode One-Hot Vector'),
        (0.62, 0.25, 'KNN Predict (k=5)'),
        (0.62, 0.15, 'Filter by Possible\nDiseases'),
    ]
    for cx, cy, text in ml_ucs:
        draw_usecase(ax, cx, cy, text, PURPLE)
        ax.plot([0.88, cx + 0.11], [0.35, cy], color=PURPLE, lw=1, zorder=2)

    # Connection lines between use cases (<<include>>)
    ax.annotate('', xy=(0.51, 0.72), xytext=(0.49, 0.72),
                arrowprops=dict(arrowstyle='->', color=GRAY_DARK, lw=1, ls='--'))
    ax.text(0.50, 0.74, '<<include>>', ha='center', fontsize=7, color=GRAY_DARK, style='italic')

    ax.annotate('', xy=(0.51, 0.52), xytext=(0.49, 0.42),
                arrowprops=dict(arrowstyle='->', color=GRAY_DARK, lw=1, ls='--'))
    ax.text(0.505, 0.47, '<<include>>', ha='center', fontsize=7, color=GRAY_DARK, style='italic')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_2_usecase.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_2_usecase.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 4: Class Diagram
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_3_class():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.98, 'Class Diagram — AI Medical Chatbot',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.94, 'Figure 4.3 — Key Classes and Relationships',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    def draw_class_box(ax, x, y, w, h_name, name, attrs, methods, color, text_color):
        total_lines = 1 + len(attrs) + len(methods) + 0.5  # +0.5 for separators
        line_h = 0.022
        total_h = total_lines * line_h + 0.03

        # Background
        bg = FancyBboxPatch((x, y - total_h), w, total_h, boxstyle="round,pad=0.005",
                            facecolor=WHITE, edgecolor=color, linewidth=2, zorder=3)
        ax.add_patch(bg)

        # Header
        header = FancyBboxPatch((x, y - line_h - 0.015), w, line_h + 0.015,
                                boxstyle="round,pad=0.005",
                                facecolor=color, edgecolor=color, linewidth=0, zorder=4,
                                alpha=0.2)
        ax.add_patch(header)
        ax.text(x + w / 2, y - 0.01, name, ha='center', va='top', fontsize=10,
                fontweight='bold', color=text_color, zorder=5)

        # Separator after name
        cy = y - line_h - 0.02
        ax.plot([x + 0.005, x + w - 0.005], [cy, cy], color=color, lw=0.8, zorder=4)

        # Attributes
        for i, attr in enumerate(attrs):
            cy -= line_h
            ax.text(x + 0.008, cy, f'- {attr}', ha='left', va='top', fontsize=7.5,
                    color=GRAY_DARK, family='monospace', zorder=5)

        # Separator
        cy -= 0.008
        ax.plot([x + 0.005, x + w - 0.005], [cy, cy], color=color, lw=0.8, zorder=4)

        # Methods
        for i, method in enumerate(methods):
            cy -= line_h
            ax.text(x + 0.008, cy, f'+ {method}', ha='left', va='top', fontsize=7.5,
                    color='#212121', family='monospace', zorder=5)

        return x, y, x + w, y - total_h

    # Class 1: NLPProcessor (top-left)
    draw_class_box(ax, 0.02, 0.88, 0.22, 0.03, 'NLPProcessor',
                   ['nlp: spacy.Language', 'lemmatizer: Lemmatizer', 'stop_words: set'],
                   ['clean_symp(sym): str', 'preprocess(text): list', 'jaccard_set(a,b): float',
                    'syntactic_similarity(a,b): int', 'semantic_similarity(a,b): int',
                    'suggest_syn(sym): list'],
                   GREEN_PRIMARY, GREEN_DARK)

    # Class 2: DiseasePredictor (top-right)
    draw_class_box(ax, 0.27, 0.88, 0.22, 0.03, 'DiseasePredictor',
                   ['knn_model: KNeighbors', 'cols: list[132]', 'le: LabelEncoder'],
                   ['OHV(symptoms): ndarray', 'possible_diseases(syms): list',
                    'predict(vector): str', 'filter_diseases(syms): list'],
                   PURPLE, PURPLE)

    # Class 3: MedicalInfoProvider (top-far-right)
    draw_class_box(ax, 0.52, 0.88, 0.22, 0.03, 'MedicalInfoProvider',
                   ['desc_df: DataFrame', 'severity_df: DataFrame', 'precaution_df: DataFrame'],
                   ['getDescription(disease): str', 'getSeverityDict(): dict',
                    'calc_condition(syms,days): str', 'getPrecautions(disease): list'],
                   TEAL, '#00695C')

    # Class 4: ChatbotEngine (bottom-left)
    draw_class_box(ax, 0.10, 0.46, 0.22, 0.03, 'ChatbotEngine',
                   ['nlp_proc: NLPProcessor', 'predictor: DiseasePredictor',
                    'info_prov: MedicalInfoProvider', 'session: dict'],
                   ['get_bot_response(msg): str', 'handle_state(msg): str',
                    'reset_session(): None'],
                   BLUE_PRIMARY, BLUE_DARK)

    # Class 5: FlaskApp (bottom-right)
    draw_class_box(ax, 0.55, 0.46, 0.22, 0.03, 'FlaskApp',
                   ['app: Flask', 'chatbot: ChatbotEngine', 'host: str', 'port: int'],
                   ['route_home(): Response', 'route_chat(): Response',
                    'route_get_response(): JSON', 'render_template(t): HTML'],
                   ORANGE, '#E65100')

    # Relationships
    # ChatbotEngine --> NLPProcessor (uses)
    ax.annotate('', xy=(0.13, 0.88 - 0.26), xytext=(0.21, 0.46 - 0.22 + 0.22),
                arrowprops=dict(arrowstyle='->', color=GREEN_DARK, lw=1.5, ls='--'))
    ax.text(0.08, 0.55, 'uses', fontsize=8, color=GREEN_DARK, rotation=90, ha='center')

    # ChatbotEngine --> DiseasePredictor
    ax.annotate('', xy=(0.38, 0.62), xytext=(0.32, 0.46),
                arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.5, ls='--'))
    ax.text(0.37, 0.54, 'uses', fontsize=8, color=PURPLE, ha='center')

    # ChatbotEngine --> MedicalInfoProvider
    ax.annotate('', xy=(0.58, 0.62), xytext=(0.32, 0.42),
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.5, ls='--'))
    ax.text(0.48, 0.50, 'uses', fontsize=8, color=TEAL, ha='center')

    # FlaskApp --> ChatbotEngine
    ax.annotate('', xy=(0.32, 0.38), xytext=(0.55, 0.38),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5, ls='--'))
    ax.text(0.44, 0.39, 'owns', fontsize=8, color=ORANGE, ha='center')

    # Legend
    ax.text(0.78, 0.88, 'Legend', fontsize=10, fontweight='bold', color=GRAY_DARK)
    styles = [
        ('Composition (owns)', ORANGE, '-'),
        ('Dependency (uses)', GREEN_DARK, '--'),
    ]
    for i, (label, color, ls) in enumerate(styles):
        yy = 0.84 - i * 0.04
        ax.plot([0.78, 0.85], [yy, yy], color=color, lw=1.5, ls=ls)
        ax.annotate('', xy=(0.85, yy), xytext=(0.84, yy),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        ax.text(0.86, yy, label, fontsize=8, color=GRAY_DARK, va='center')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_3_class.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_3_class.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Sequence Diagram
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_4_sequence():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.98, 'Sequence Diagram — Symptom-to-Prediction Flow',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.94, 'Figure 4.4 — Message Passing Between Components',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    # Lifeline positions
    actors = [
        ('Patient', 0.10, BLUE_DARK, BLUE_LIGHT),
        ('Flask\nServer', 0.28, BLUE_PRIMARY, BLUE_LIGHT),
        ('NLP\nEngine', 0.46, GREEN_PRIMARY, GREEN_LIGHT),
        ('KNN\nModel', 0.64, PURPLE, '#EDE7F6'),
        ('CSV\nData', 0.82, ORANGE, '#FFF3E0'),
    ]

    for name, x, color, bg in actors:
        # Actor box
        draw_rounded_box(ax, x - 0.06, 0.87, 0.12, 0.06, name,
                         facecolor=bg, edgecolor=color, fontsize=9, fontweight='bold',
                         textcolor=color)
        # Lifeline
        ax.plot([x, x], [0.87, 0.08], color=color, lw=1, ls='--', zorder=1)
        # Activation bar
        bar_w = 0.015
        ax.add_patch(FancyBboxPatch((x - bar_w / 2, 0.10), bar_w, 0.77,
                                     boxstyle="round,pad=0.002",
                                     facecolor=bg, edgecolor=color, linewidth=1, alpha=0.6, zorder=2))

    # Messages
    messages = [
        (0.10, 0.28, 0.82, '1. Type symptom in chat', BLUE_DARK),
        (0.28, 0.46, 0.77, '2. preprocess(user_input)', GREEN_DARK),
        (0.46, 0.46, 0.72, '3. tokenize & lemmatize', GREEN_DARK),
        (0.46, 0.28, 0.67, '4. return cleaned tokens', GREEN_DARK),
        (0.28, 0.46, 0.62, '5. syntactic_similarity(token, symptoms)', GREEN_DARK),
        (0.46, 0.28, 0.57, '6. return Jaccard match / no match', GREEN_DARK),
        (0.28, 0.46, 0.52, '7. semantic_similarity(token, symptoms)', GREEN_DARK),
        (0.46, 0.28, 0.47, '8. return WUP match / suggest synonym', GREEN_DARK),
        (0.28, 0.64, 0.42, '9. OHV(matched_symptoms)', PURPLE),
        (0.64, 0.64, 0.37, '10. encode one-hot vector (132-D)', PURPLE),
        (0.64, 0.28, 0.32, '11. predict(vector) → disease', PURPLE),
        (0.28, 0.82, 0.27, '12. load description & severity', ORANGE),
        (0.82, 0.28, 0.22, '13. return disease info', ORANGE),
        (0.28, 0.10, 0.17, '14. display result to patient', BLUE_DARK),
    ]

    for i, (x1, x2, y, label, color) in enumerate(messages):
        is_self = (x1 == x2)
        is_return = (x2 < x1) if not is_self else False

        if is_self:
            # Self-call
            ax.annotate('', xy=(x1 + 0.04, y - 0.02), xytext=(x1 + 0.04, y),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.2,
                                        connectionstyle='arc3,rad=0.3'))
            ax.text(x1 + 0.05, y - 0.01, label, fontsize=7.5, color=color, va='center')
        else:
            style = '->' if not is_return else '->'
            ls = '-' if not is_return else '--'
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle=style, color=color, lw=1.2, ls=ls))
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 0.012, label, fontsize=7.5, color=color,
                    ha='center', va='bottom')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_4_sequence.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_4_sequence.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 6: Activity Diagram
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_5_activity():
    fig, ax = plt.subplots(figsize=(14, 18))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.99, 'Activity Diagram — Chatbot Consultation Flow',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.97, 'Figure 4.5 — Complete Patient Interaction Workflow',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    cx = 0.5  # center x
    bw = 0.22
    bh = 0.028
    gap = 0.042

    activities = [
        ('start', 'START', None),
        ('action', 'Open Landing Page', BLUE_LIGHT),
        ('action', 'Navigate to Chat Interface', BLUE_LIGHT),
        ('action', 'Enter Name, Age, Gender', BLUE_LIGHT),
        ('action', 'Describe Primary Symptom', GREEN_LIGHT),
        ('diamond', 'Syntactic\nMatch?', None),
        ('action', 'Symptom Identified\n(Jaccard)', GREEN_LIGHT),          # yes branch
        ('diamond', 'Semantic\nMatch?', None),                              # no branch
        ('action', 'Symptom Identified\n(WordNet WUP)', GREEN_LIGHT),       # yes
        ('action', 'Suggest Synonyms\nto User', '#FFF3E0'),                 # no
        ('action', 'User Confirms\nSuggested Symptom', '#FFF3E0'),
        ('action', 'Enter Second Symptom', GREEN_LIGHT),
        ('action', 'Answer Follow-up\nQuestions', GREEN_LIGHT),
        ('action', 'KNN Predicts Disease\n(k=5, 132-D Vector)', '#EDE7F6'),
        ('action', 'Display Predicted\nDisease Name', BLUE_LIGHT),
        ('action', 'Show Description\n& Details', BLUE_LIGHT),
        ('action', 'Calculate & Show\nSeverity Score', BLUE_LIGHT),
        ('action', 'Show Precautions\n& Advice', BLUE_LIGHT),
        ('diamond', 'New\nConsult?', None),
        ('action', 'Reset Session', BLUE_LIGHT),
        ('end', 'END', None),
    ]

    y = 0.955
    positions = {}
    idx = 0
    
    for atype, label, bg in activities:
        y -= gap
        if atype == 'start':
            circle = plt.Circle((cx, y), 0.012, facecolor='#212121', edgecolor='#212121', zorder=5)
            ax.add_patch(circle)
            positions[idx] = (cx, y)
        elif atype == 'end':
            circle = plt.Circle((cx, y), 0.012, facecolor=WHITE, edgecolor='#212121', lw=2, zorder=5)
            ax.add_patch(circle)
            inner = plt.Circle((cx, y), 0.008, facecolor='#212121', edgecolor='#212121', zorder=6)
            ax.add_patch(inner)
            positions[idx] = (cx, y)
        elif atype == 'action':
            draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh, label,
                             facecolor=bg, edgecolor=BLUE_PRIMARY if bg == BLUE_LIGHT 
                             else GREEN_PRIMARY if bg == GREEN_LIGHT
                             else PURPLE if bg == '#EDE7F6' else ORANGE,
                             fontsize=8, fontweight='bold')
            positions[idx] = (cx, y)
        elif atype == 'diamond':
            size = 0.025
            diamond = plt.Polygon([(cx, y + size), (cx + size * 1.5, y),
                                    (cx, y - size), (cx - size * 1.5, y)],
                                   facecolor='#FFF9C4', edgecolor='#F9A825', lw=1.5, zorder=5)
            ax.add_patch(diamond)
            ax.text(cx, y, label, ha='center', va='center', fontsize=7,
                    fontweight='bold', color='#F57F17', zorder=6)
            positions[idx] = (cx, y)
        idx += 1

    # Draw sequential arrows
    for i in range(len(activities) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        
        # Special branching for diamonds
        atype = activities[i][0]
        atype_next = activities[i + 1][0]
        
        if atype == 'diamond':
            # "Yes" goes down (main flow)
            draw_arrow(ax, x1, y1 - 0.025, x2, y2 + bh / 2 + 0.005, color=GREEN_DARK, lw=1.5)
            ax.text(x1 + 0.005, y1 - 0.028, 'Yes', fontsize=7, color=GREEN_DARK, fontweight='bold')
            # "No" label to the right
            ax.text(x1 + 0.045, y1 + 0.005, 'No', fontsize=7, color=RED_SOFT, fontweight='bold')
        elif atype == 'start':
            draw_arrow(ax, x1, y1 - 0.012, x2, y2 + bh / 2 + 0.005, color=GRAY_DARK, lw=1.5)
        elif atype_next == 'end':
            draw_arrow(ax, x1, y1 - bh / 2, x2, y2 + 0.012, color=GRAY_DARK, lw=1.5)
        elif atype_next == 'diamond':
            draw_arrow(ax, x1, y1 - bh / 2, x2, y2 + 0.025, color=GRAY_DARK, lw=1.5)
        else:
            draw_arrow(ax, x1, y1 - bh / 2, x2, y2 + bh / 2 + 0.005, color=GRAY_DARK, lw=1.5)

    # New Consult "Yes" loops back (arrow from diamond 18 to Reset 19, then back to activity 3)
    # The "No" goes to END
    # Draw loop-back arrow from "Reset Session" back to "Enter Name..."
    x_reset, y_reset = positions[19]
    x_name, y_name = positions[3]
    # Draw curved arrow on the left side
    ax.annotate('', xy=(cx - bw / 2, y_name),
                xytext=(cx - bw / 2, y_reset),
                arrowprops=dict(arrowstyle='->', color=BLUE_PRIMARY, lw=1.5,
                                connectionstyle='arc3,rad=0.4'))
    ax.text(cx - bw / 2 - 0.06, (y_name + y_reset) / 2, 'Loop\nBack',
            fontsize=7, color=BLUE_PRIMARY, ha='center', fontweight='bold')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_5_activity.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_5_activity.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 7: Chat Interface Wireframe
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_6_wireframe():
    fig, ax = plt.subplots(figsize=(7, 12))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor('#ECEFF1')

    # Phone frame
    phone = FancyBboxPatch((0.08, 0.03), 0.84, 0.94, boxstyle="round,pad=0.03",
                           facecolor=WHITE, edgecolor='#37474F', linewidth=3, zorder=1)
    ax.add_patch(phone)

    # Status bar
    ax.add_patch(FancyBboxPatch((0.08, 0.93), 0.84, 0.04,
                                boxstyle="round,pad=0.01", facecolor='#37474F',
                                edgecolor='#37474F', linewidth=0, zorder=2))
    ax.text(0.5, 0.95, '9:41 AM', ha='center', va='center', fontsize=8,
            color=WHITE, fontweight='bold', zorder=3)

    # Header
    ax.add_patch(FancyBboxPatch((0.08, 0.87), 0.84, 0.06,
                                boxstyle="round,pad=0.005", facecolor=BLUE_DARK,
                                edgecolor=BLUE_DARK, linewidth=0, zorder=2))
    ax.text(0.5, 0.90, 'Medical-Chatbot', ha='center', va='center',
            fontsize=14, fontweight='bold', color=WHITE, zorder=3)
    ax.text(0.15, 0.90, '<', ha='center', va='center', fontsize=16,
            fontweight='bold', color=WHITE, zorder=3)

    # Chat area background
    ax.add_patch(plt.Rectangle((0.10, 0.10), 0.80, 0.77,
                               facecolor='#FAFAFA', edgecolor='none', zorder=1))

    def bot_msg(y, text):
        # Avatar
        circle = plt.Circle((0.16, y + 0.015), 0.02, facecolor=GREEN_PRIMARY,
                             edgecolor=GREEN_DARK, lw=1, zorder=4)
        ax.add_patch(circle)
        ax.text(0.16, y + 0.015, 'B', ha='center', va='center', fontsize=8,
                color=WHITE, fontweight='bold', zorder=5)
        # Bubble
        bub = FancyBboxPatch((0.20, y), 0.52, 0.035, boxstyle="round,pad=0.008",
                             facecolor='#E8E8E8', edgecolor='#BDBDBD', linewidth=0.8, zorder=3)
        ax.add_patch(bub)
        ax.text(0.46, y + 0.0175, text, ha='center', va='center', fontsize=7.5,
                color='#212121', zorder=4)

    def user_msg(y, text):
        # Avatar
        circle = plt.Circle((0.84, y + 0.015), 0.02, facecolor=BLUE_PRIMARY,
                             edgecolor=BLUE_DARK, lw=1, zorder=4)
        ax.add_patch(circle)
        ax.text(0.84, y + 0.015, 'U', ha='center', va='center', fontsize=8,
                color=WHITE, fontweight='bold', zorder=5)
        # Bubble
        bub = FancyBboxPatch((0.35, y), 0.45, 0.035, boxstyle="round,pad=0.008",
                             facecolor=BLUE_PRIMARY, edgecolor=BLUE_DARK, linewidth=0.8, zorder=3)
        ax.add_patch(bub)
        ax.text(0.575, y + 0.0175, text, ha='center', va='center', fontsize=7.5,
                color=WHITE, zorder=4)

    # Chat messages
    bot_msg(0.80, "Hello! I'm your Medical Assistant.")
    bot_msg(0.75, "What is your name?")
    user_msg(0.70, "My name is Shoukath")
    bot_msg(0.65, "Hi Shoukath! Your age?")
    user_msg(0.60, "22")
    bot_msg(0.55, "Describe your main symptom:")
    user_msg(0.50, "I have a headache")
    bot_msg(0.45, "Is headache related to your problem?")
    user_msg(0.40, "Yes")
    bot_msg(0.35, "Any other symptom?")
    user_msg(0.30, "I also feel dizzy")
    bot_msg(0.25, "Do you have nausea?")
    user_msg(0.20, "No")
    bot_msg(0.15, "Prediction: Hypertension")

    # Input field
    ax.add_patch(FancyBboxPatch((0.10, 0.04), 0.64, 0.05,
                                boxstyle="round,pad=0.01", facecolor=WHITE,
                                edgecolor=GRAY_MED, linewidth=1.5, zorder=3))
    ax.text(0.20, 0.065, 'Type your message...', ha='left', va='center',
            fontsize=9, color=GRAY_MED, zorder=4, style='italic')

    # Send button
    ax.add_patch(FancyBboxPatch((0.76, 0.04), 0.14, 0.05,
                                boxstyle="round,pad=0.01", facecolor=BLUE_PRIMARY,
                                edgecolor=BLUE_DARK, linewidth=1.5, zorder=3))
    ax.text(0.83, 0.065, 'Send', ha='center', va='center', fontsize=10,
            color=WHITE, fontweight='bold', zorder=4)

    # Figure label
    ax.text(0.5, 0.01, 'Figure 4.6 — Chat Interface Wireframe', ha='center',
            fontsize=10, color=GRAY_DARK, style='italic')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_6_wireframe.png'), dpi=DPI,
                bbox_inches='tight', facecolor='#ECEFF1')
    plt.close(fig)
    print('[OK] fig_4_6_wireframe.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 8: NLP Pipeline
# ═══════════════════════════════════════════════════════════════════════════════
def fig_4_7_nlp_pipeline():
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.99, 'NLP Processing Pipeline',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.97, 'Figure 4.7 — Three-Stage Symptom Matching Pipeline',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    cx = 0.5
    bw = 0.35
    bh = 0.032
    gap = 0.048
    y = 0.94

    steps = [
        ('Raw User Input Text', BLUE_LIGHT, BLUE_PRIMARY, '"I have a really bad headache"'),
        ('spaCy Tokenizer', GREEN_LIGHT, GREEN_PRIMARY, '["I", "have", "a", "really", "bad", "headache"]'),
        ('Stop Word Filter', GREEN_LIGHT, GREEN_PRIMARY, '["really", "bad", "headache"]'),
        ('Lemmatizer', GREEN_LIGHT, GREEN_PRIMARY, '["really", "bad", "headache"]'),
        ('Cleaned Tokens', '#E0F7FA', TEAL, 'Preprocessed token list'),
    ]

    positions = []
    for i, (label, bg, ec, detail) in enumerate(steps):
        y -= gap
        draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh, label,
                         facecolor=bg, edgecolor=ec, fontsize=10, fontweight='bold')
        # Detail text on the right
        ax.text(cx + bw / 2 + 0.02, y, detail, fontsize=8, color=GRAY_DARK,
                va='center', style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY_LIGHT, edgecolor=GRAY_MED, alpha=0.7))
        positions.append(y)
        if i < len(steps) - 1:
            draw_arrow(ax, cx, y - bh / 2, cx, y - gap + bh / 2 + 0.005, color=GRAY_DARK, lw=2)

    # ── Stage separator ──
    y -= gap * 0.7
    ax.plot([0.1, 0.9], [y, y], color=BLUE_PRIMARY, lw=1, ls='--')
    ax.text(0.5, y + 0.008, 'THREE-STAGE MATCHING', ha='center', fontsize=10,
            fontweight='bold', color=BLUE_DARK,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BLUE_LIGHT, edgecolor=BLUE_PRIMARY))

    # Stage 1: Jaccard
    y -= gap
    draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh,
                     'STAGE 1: Jaccard Set Similarity',
                     facecolor='#C8E6C9', edgecolor=GREEN_DARK, fontsize=10, fontweight='bold',
                     textcolor=GREEN_DARK)
    ax.text(cx + bw / 2 + 0.02, y, 'J(A,B) = |A ∩ B| / |A ∪ B|', fontsize=8,
            color=GREEN_DARK, va='center', family='monospace',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GREEN_LIGHT, edgecolor=GREEN_PRIMARY))

    draw_arrow(ax, cx, y - bh / 2, cx, y - gap + 0.015, color=GRAY_DARK, lw=2)

    # Decision diamond 1
    y -= gap
    size = 0.018
    diamond = plt.Polygon([(cx, y + size), (cx + size * 2.5, y),
                            (cx, y - size), (cx - size * 2.5, y)],
                           facecolor='#FFF9C4', edgecolor='#F9A825', lw=1.5, zorder=5)
    ax.add_patch(diamond)
    ax.text(cx, y, 'Match ≥ threshold?', ha='center', va='center', fontsize=8,
            fontweight='bold', color='#F57F17', zorder=6)

    # Yes → Symptom ID
    ax.annotate('', xy=(cx + 0.22, y), xytext=(cx + 0.045, y),
                arrowprops=dict(arrowstyle='->', color=GREEN_DARK, lw=1.5))
    ax.text(cx + 0.06, y + 0.01, 'Yes', fontsize=8, color=GREEN_DARK, fontweight='bold')
    draw_rounded_box(ax, cx + 0.22, y - 0.015, 0.15, 0.03, 'Symptom ID\nResolved',
                     facecolor='#C8E6C9', edgecolor=GREEN_DARK, fontsize=8, fontweight='bold',
                     textcolor=GREEN_DARK)

    # No → Stage 2
    ax.text(cx + 0.005, y - 0.022, 'No', fontsize=8, color=RED_SOFT, fontweight='bold')
    draw_arrow(ax, cx, y - size, cx, y - gap + 0.018, color=RED_SOFT, lw=1.5)

    # Stage 2: WordNet WUP
    y -= gap
    draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh,
                     'STAGE 2: WordNet WUP Similarity',
                     facecolor='#D1C4E9', edgecolor=PURPLE, fontsize=10, fontweight='bold',
                     textcolor=PURPLE)
    ax.text(cx + bw / 2 + 0.02, y, 'WUP = 2*depth(LCS) / (d1+d2)', fontsize=8,
            color=PURPLE, va='center', family='monospace',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EDE7F6', edgecolor=PURPLE))

    draw_arrow(ax, cx, y - bh / 2, cx, y - gap + 0.015, color=GRAY_DARK, lw=2)

    # Decision diamond 2
    y -= gap
    diamond2 = plt.Polygon([(cx, y + size), (cx + size * 2.5, y),
                             (cx, y - size), (cx - size * 2.5, y)],
                            facecolor='#FFF9C4', edgecolor='#F9A825', lw=1.5, zorder=5)
    ax.add_patch(diamond2)
    ax.text(cx, y, 'Match ≥ threshold?', ha='center', va='center', fontsize=8,
            fontweight='bold', color='#F57F17', zorder=6)

    ax.annotate('', xy=(cx + 0.22, y), xytext=(cx + 0.045, y),
                arrowprops=dict(arrowstyle='->', color=GREEN_DARK, lw=1.5))
    ax.text(cx + 0.06, y + 0.01, 'Yes', fontsize=8, color=GREEN_DARK, fontweight='bold')
    draw_rounded_box(ax, cx + 0.22, y - 0.015, 0.15, 0.03, 'Symptom ID\nResolved',
                     facecolor='#C8E6C9', edgecolor=GREEN_DARK, fontsize=8, fontweight='bold',
                     textcolor=GREEN_DARK)

    ax.text(cx + 0.005, y - 0.022, 'No', fontsize=8, color=RED_SOFT, fontweight='bold')
    draw_arrow(ax, cx, y - size, cx, y - gap + 0.018, color=RED_SOFT, lw=1.5)

    # Stage 3: Synonym Suggestion
    y -= gap
    draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh,
                     'STAGE 3: Synonym Suggestion',
                     facecolor='#FFF3E0', edgecolor=ORANGE, fontsize=10, fontweight='bold',
                     textcolor='#E65100')
    ax.text(cx + bw / 2 + 0.02, y, 'WordNet synsets → user confirms', fontsize=8,
            color='#E65100', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', edgecolor=ORANGE))

    draw_arrow(ax, cx, y - bh / 2, cx, y - gap + bh / 2 + 0.005, color=GRAY_DARK, lw=2)

    # User Confirms
    y -= gap
    draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh, 'User Confirms / Selects Synonym',
                     facecolor=BLUE_LIGHT, edgecolor=BLUE_PRIMARY, fontsize=10, fontweight='bold',
                     textcolor=BLUE_DARK)

    draw_arrow(ax, cx, y - bh / 2, cx, y - gap + bh / 2 + 0.005, color=GRAY_DARK, lw=2)

    # Final: Symptom ID Resolved
    y -= gap
    draw_rounded_box(ax, cx - bw / 2, y - bh / 2, bw, bh + 0.008,
                     'SYMPTOM ID RESOLVED\n→ Continue to Next Symptom or KNN',
                     facecolor='#C8E6C9', edgecolor=GREEN_DARK, fontsize=10, fontweight='bold',
                     textcolor=GREEN_DARK)

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_4_7_nlp_pipeline.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_4_7_nlp_pipeline.png')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 9: Development Phases
# ═══════════════════════════════════════════════════════════════════════════════
def fig_5_1_phases():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    ax.text(0.5, 0.97, 'Development Phases — AI Medical Chatbot',
            ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE_DARK)
    ax.text(0.5, 0.93, 'Figure 5.1 — Four-Phase Implementation Methodology',
            ha='center', va='top', fontsize=11, color=GRAY_DARK)

    phases = [
        {
            'title': 'PHASE 1\nDataset Preparation',
            'color': BLUE_PRIMARY,
            'dark': BLUE_DARK,
            'light': BLUE_LIGHT,
            'items': [
                '6 CSV files collected',
                '132 unique symptoms',
                '41 disease classes',
                '4920 training records',
                'Severity mapping',
                'Description & precautions',
            ]
        },
        {
            'title': 'PHASE 2\nNLP Engine',
            'color': GREEN_PRIMARY,
            'dark': GREEN_DARK,
            'light': GREEN_LIGHT,
            'items': [
                'spaCy tokenizer & lemmatizer',
                'Stop word removal',
                'Jaccard similarity (Stage 1)',
                'WordNet WUP (Stage 2)',
                'Synonym suggestion (Stage 3)',
                'Three-stage matching pipeline',
            ]
        },
        {
            'title': 'PHASE 3\nML Classification',
            'color': PURPLE,
            'dark': '#4A148C',
            'light': '#EDE7F6',
            'items': [
                'One-hot encoding (132-D)',
                'KNN classifier (k=5)',
                'Distance-weighted voting',
                'Model training & saving',
                'knn.pkl serialization',
                'Disease filtering logic',
            ]
        },
        {
            'title': 'PHASE 4\nWeb Integration',
            'color': ORANGE,
            'dark': '#E65100',
            'light': '#FFF3E0',
            'items': [
                'Flask server (port 5000)',
                'Chat UI (HTML/CSS/JS)',
                'jQuery AJAX integration',
                'Session management',
                'Conversational state machine',
                'Docker containerization',
            ]
        },
    ]

    pw = 0.20  # phase box width
    ph = 0.65  # phase box height
    margin = 0.04
    start_x = 0.04

    for i, phase in enumerate(phases):
        x = start_x + i * (pw + margin)
        y_base = 0.15

        # Phase background
        bg = FancyBboxPatch((x, y_base), pw, ph, boxstyle="round,pad=0.01",
                            facecolor=phase['light'], edgecolor=phase['color'],
                            linewidth=2.5, alpha=0.7, zorder=2)
        ax.add_patch(bg)

        # Phase number circle at top
        circle = plt.Circle((x + pw / 2, y_base + ph - 0.02), 0.035,
                             facecolor=phase['color'], edgecolor=phase['dark'],
                             lw=2, zorder=5)
        ax.add_patch(circle)
        ax.text(x + pw / 2, y_base + ph - 0.02, str(i + 1), ha='center', va='center',
                fontsize=18, fontweight='bold', color=WHITE, zorder=6)

        # Title
        ax.text(x + pw / 2, y_base + ph - 0.09, phase['title'], ha='center', va='top',
                fontsize=11, fontweight='bold', color=phase['dark'], zorder=4)

        # Separator
        ax.plot([x + 0.02, x + pw - 0.02], [y_base + ph - 0.16, y_base + ph - 0.16],
                color=phase['color'], lw=1, zorder=3)

        # Items
        for j, item in enumerate(phase['items']):
            iy = y_base + ph - 0.20 - j * 0.065
            # Bullet
            bullet = plt.Circle((x + 0.025, iy), 0.006, facecolor=phase['color'],
                                edgecolor=phase['dark'], lw=0.5, zorder=5)
            ax.add_patch(bullet)
            ax.text(x + 0.04, iy, item, fontsize=8.5, color='#212121',
                    va='center', zorder=4)

        # Arrow to next phase
        if i < len(phases) - 1:
            ax.annotate('', xy=(x + pw + margin * 0.15, y_base + ph / 2),
                        xytext=(x + pw + 0.005, y_base + ph / 2),
                        arrowprops=dict(arrowstyle='->', color=GRAY_DARK, lw=2.5))

    # Timeline arrow at bottom
    ax.annotate('', xy=(0.92, 0.09), xytext=(0.04, 0.09),
                arrowprops=dict(arrowstyle='->', color=BLUE_DARK, lw=2.5))
    ax.text(0.5, 0.06, 'Development Timeline', ha='center', fontsize=12,
            fontweight='bold', color=BLUE_DARK)

    # Milestones
    milestones = ['Data Ready', 'NLP Ready', 'Model Trained', 'Deployed']
    for i, ms in enumerate(milestones):
        mx = 0.14 + i * 0.24
        ax.plot([mx, mx], [0.085, 0.095], color=BLUE_DARK, lw=2)
        ax.text(mx, 0.075, ms, ha='center', fontsize=8, color=BLUE_DARK, fontweight='bold')

    fig.savefig(os.path.join(OUTPUT_DIR, 'fig_5_1_phases.png'), dpi=DPI,
                bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print('[OK] fig_5_1_phases.png')


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Generate all 9 figures
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print(f'Output directory: {OUTPUT_DIR}')
    print('Generating 9 figures...\n')

    fig_1_1_comparison()
    fig_4_1_architecture()
    fig_4_2_usecase()
    fig_4_3_class()
    fig_4_4_sequence()
    fig_4_5_activity()
    fig_4_6_wireframe()
    fig_4_7_nlp_pipeline()
    fig_5_1_phases()

    print('\n=== ALL 9 FIGURES GENERATED SUCCESSFULLY ===')
    print(f'Saved to: {OUTPUT_DIR}')
