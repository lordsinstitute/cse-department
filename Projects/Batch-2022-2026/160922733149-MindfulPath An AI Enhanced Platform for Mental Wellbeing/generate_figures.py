"""
MindfulPath: AI Enhanced Platform for Mental Wellbeing
------------------------------------------------------
Generates 7 professional dark-theme figures for the project report.

Run:
    python generate_figures.py

All figures are saved to ./figures/ with dpi=150.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ──────────────────────────────────────────────
# Common palette / constants
# ──────────────────────────────────────────────
DARK_BG    = '#1a1a2e'
ACCENT     = '#7c3aed'
LIGHT_TEXT = '#e0e0e0'
CARD_BG    = '#16213e'
SECONDARY  = '#0f3460'
HIGHLIGHT  = '#a78bfa'   # lighter purple for emphasis
SUCCESS    = '#10b981'   # green accent (crisis / positive)
WARNING    = '#f59e0b'   # amber accent
DANGER     = '#ef4444'   # red accent
MUTED_TEXT = '#94a3b8'

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)


# ──────────────────────────────────────────────
# Helper utilities
# ──────────────────────────────────────────────

def _new_figure(width=14, height=8):
    """Create a figure+axes with dark background and axes off."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.axis('off')
    return fig, ax


def _save(fig, filename):
    """Save figure to SAVE_DIR."""
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print(f"  Saved {path}")


def _fancy_box(ax, x, y, w, h, text, color=CARD_BG, text_color=LIGHT_TEXT,
               fontsize=10, edge_color=ACCENT, linewidth=1.5, style='round,pad=0.1',
               zorder=2, alpha=1.0, bold=False):
    """Draw a rounded box with centered text."""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=style,
                         facecolor=color, edgecolor=edge_color,
                         linewidth=linewidth, zorder=zorder, alpha=alpha)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w / 2, y + h / 2, text,
            ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight=weight, zorder=zorder + 1,
            wrap=True)
    return box


def _arrow(ax, x_start, y_start, x_end, y_end, color=HIGHLIGHT, lw=1.5,
           style='->', mutation_scale=15):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch(
        (x_start, y_start), (x_end, y_end),
        arrowstyle=style, color=color,
        linewidth=lw, mutation_scale=mutation_scale,
        zorder=5
    )
    ax.add_patch(arrow)
    return arrow


def _arrow_label(ax, x_start, y_start, x_end, y_end, label='',
                 color=HIGHLIGHT, lw=1.5, fontsize=8):
    """Arrow with a label at its midpoint."""
    _arrow(ax, x_start, y_start, x_end, y_end, color=color, lw=lw)
    mx = (x_start + x_end) / 2
    my = (y_start + y_end) / 2
    if label:
        ax.text(mx, my + 0.02, label, ha='center', va='bottom',
                fontsize=fontsize, color=MUTED_TEXT, style='italic', zorder=6)


# ====================================================================
# Figure 1.1  System Architecture (3-Tier)
# ====================================================================

def fig_1_1_system_architecture():
    fig, ax = _new_figure(16, 9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Title
    ax.text(0.50, 0.96, 'System Architecture  -  Three-Tier Overview',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    # ── Tier labels ──
    tier_y = 0.88
    for tx, label in [(0.15, 'CLIENT TIER'), (0.50, 'APPLICATION TIER'), (0.85, 'DATA TIER')]:
        ax.text(tx, tier_y, label, ha='center', va='center',
                fontsize=12, color=HIGHLIGHT, fontweight='bold')

    # ── Client tier ──
    _fancy_box(ax, 0.02, 0.62, 0.24, 0.18, '', color=SECONDARY, edge_color=ACCENT, linewidth=2)
    ax.text(0.14, 0.77, 'Browser / Client', ha='center', va='center',
            fontsize=12, color=LIGHT_TEXT, fontweight='bold')
    # sub-items
    for i, item in enumerate(['EJS Templates', 'Chart.js Visuals', 'Bootstrap 5 UI']):
        _fancy_box(ax, 0.04, 0.63 + (2 - i) * 0.043, 0.20, 0.035, item,
                   color=CARD_BG, fontsize=9, edge_color=ACCENT, linewidth=1)

    # Static assets box
    _fancy_box(ax, 0.02, 0.42, 0.24, 0.14, '', color=SECONDARY, edge_color=ACCENT, linewidth=2)
    ax.text(0.14, 0.53, 'Static Assets', ha='center', va='center',
            fontsize=11, color=LIGHT_TEXT, fontweight='bold')
    for i, item in enumerate(['CSS / JS', 'Images & Icons']):
        _fancy_box(ax, 0.04, 0.435 + (1 - i) * 0.043, 0.20, 0.035, item,
                   color=CARD_BG, fontsize=9, edge_color=ACCENT, linewidth=1)

    # ── Application tier ──
    app_x, app_w = 0.33, 0.34
    _fancy_box(ax, app_x, 0.12, app_w, 0.72, '', color=SECONDARY, edge_color=ACCENT, linewidth=2.5)
    ax.text(0.50, 0.81, 'Express.js Backend (Port 5006)', ha='center', va='center',
            fontsize=13, color=LIGHT_TEXT, fontweight='bold')

    components = [
        ('Routes Layer', 'Auth  |  Chat  |  Mood  |  Meditations  |  Sessions  |  Dashboard'),
        ('Middleware', 'JWT Auth  |  Session  |  Error Handling  |  CORS'),
        ('NLP Engine', 'AFINN Lexicon  |  Sentiment Scoring  |  Crisis Detection'),
        ('CBT Module', 'Technique Selection  |  Response Templates  |  Coping Strategies'),
        ('Services', 'Mood Analytics  |  Therapist Matching  |  Meditation Library'),
    ]
    cy = 0.71
    for title, desc in components:
        _fancy_box(ax, app_x + 0.02, cy, app_w - 0.04, 0.10, '', color=CARD_BG,
                   edge_color=ACCENT, linewidth=1.2)
        ax.text(0.50, cy + 0.065, title, ha='center', va='center',
                fontsize=10, color=HIGHLIGHT, fontweight='bold')
        ax.text(0.50, cy + 0.030, desc, ha='center', va='center',
                fontsize=8, color=MUTED_TEXT)
        cy -= 0.12

    # ── Data tier ──
    _fancy_box(ax, 0.74, 0.55, 0.24, 0.25, '', color=SECONDARY, edge_color=ACCENT, linewidth=2)
    ax.text(0.86, 0.77, 'SQLite Database', ha='center', va='center',
            fontsize=12, color=LIGHT_TEXT, fontweight='bold')
    tables = ['users', 'therapists', 'sessions', 'meditations',
              'mood_entries', 'chat_sessions', 'chat_messages']
    for i, t in enumerate(tables):
        _fancy_box(ax, 0.76, 0.565 + (6 - i) * 0.027, 0.20, 0.022, t,
                   color=CARD_BG, fontsize=8, edge_color=ACCENT, linewidth=0.8)

    _fancy_box(ax, 0.74, 0.30, 0.24, 0.18, '', color=SECONDARY, edge_color=ACCENT, linewidth=2)
    ax.text(0.86, 0.45, 'NLP Engine Store', ha='center', va='center',
            fontsize=12, color=LIGHT_TEXT, fontweight='bold')
    for i, item in enumerate(['AFINN Lexicon', 'CBT Templates', 'Crisis Keywords']):
        _fancy_box(ax, 0.76, 0.315 + (2 - i) * 0.04, 0.20, 0.032, item,
                   color=CARD_BG, fontsize=9, edge_color=ACCENT, linewidth=0.8)

    # ── Arrows between tiers ──
    _arrow(ax, 0.26, 0.70, 0.33, 0.70, color=HIGHLIGHT, lw=2.5)
    _arrow(ax, 0.33, 0.65, 0.26, 0.65, color=HIGHLIGHT, lw=2.5)
    ax.text(0.295, 0.72, 'HTTP', ha='center', va='bottom', fontsize=8, color=MUTED_TEXT)
    ax.text(0.295, 0.63, 'HTML', ha='center', va='top', fontsize=8, color=MUTED_TEXT)

    _arrow(ax, 0.67, 0.65, 0.74, 0.65, color=HIGHLIGHT, lw=2.5)
    _arrow(ax, 0.74, 0.60, 0.67, 0.60, color=HIGHLIGHT, lw=2.5)
    ax.text(0.705, 0.67, 'SQL', ha='center', va='bottom', fontsize=8, color=MUTED_TEXT)
    ax.text(0.705, 0.58, 'Results', ha='center', va='top', fontsize=8, color=MUTED_TEXT)

    _arrow(ax, 0.67, 0.40, 0.74, 0.40, color=HIGHLIGHT, lw=2.5)
    _arrow(ax, 0.74, 0.35, 0.67, 0.35, color=HIGHLIGHT, lw=2.5)
    ax.text(0.705, 0.42, 'Lookup', ha='center', va='bottom', fontsize=8, color=MUTED_TEXT)
    ax.text(0.705, 0.33, 'Scores', ha='center', va='top', fontsize=8, color=MUTED_TEXT)

    # Docker badge
    _fancy_box(ax, 0.38, 0.02, 0.24, 0.06, 'Dockerised Deployment',
               color=ACCENT, text_color='white', fontsize=10, edge_color=HIGHLIGHT,
               linewidth=2, bold=True)

    _save(fig, 'fig_1_1_system_architecture.png')


# ====================================================================
# Figure 3.1  Use-Case Diagram
# ====================================================================

def fig_3_1_use_case_diagram():
    fig, ax = _new_figure(16, 10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.97, 'Use-Case Diagram  -  MindfulPath',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    # System boundary
    boundary = FancyBboxPatch((0.25, 0.06), 0.50, 0.84,
                              boxstyle='round,pad=0.02',
                              facecolor='none', edgecolor=ACCENT,
                              linewidth=2.5, linestyle='--', zorder=1)
    ax.add_patch(boundary)
    ax.text(0.50, 0.91, 'MindfulPath System', ha='center', va='top',
            fontsize=14, color=HIGHLIGHT, fontweight='bold', style='italic')

    # ── Actors ──
    def _draw_actor(ax, x, y, label):
        head_r = 0.015
        circle = plt.Circle((x, y + 0.06), head_r, color=HIGHLIGHT,
                             fill=False, linewidth=2, zorder=10)
        ax.add_patch(circle)
        # body
        ax.plot([x, x], [y + 0.045, y + 0.015], color=HIGHLIGHT, lw=2, zorder=10)
        # arms
        ax.plot([x - 0.02, x + 0.02], [y + 0.035, y + 0.035], color=HIGHLIGHT, lw=2, zorder=10)
        # legs
        ax.plot([x, x - 0.015], [y + 0.015, y - 0.005], color=HIGHLIGHT, lw=2, zorder=10)
        ax.plot([x, x + 0.015], [y + 0.015, y - 0.005], color=HIGHLIGHT, lw=2, zorder=10)
        ax.text(x, y - 0.025, label, ha='center', va='top',
                fontsize=11, color=LIGHT_TEXT, fontweight='bold')

    # Patient / User (left)
    _draw_actor(ax, 0.10, 0.55, 'User / Patient')
    # Therapist (left-bottom)
    _draw_actor(ax, 0.10, 0.20, 'Therapist')
    # Admin (right)
    _draw_actor(ax, 0.90, 0.55, 'Admin')

    # ── Use cases ──
    def _use_case(ax, cx, cy, text, w=0.18, h=0.055):
        ellipse = mpatches.Ellipse((cx, cy), w, h,
                                    facecolor=CARD_BG, edgecolor=ACCENT,
                                    linewidth=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center',
                fontsize=9, color=LIGHT_TEXT, zorder=4)
        return cx, cy

    # User use cases (left side inside boundary)
    uc_chat     = _use_case(ax, 0.40, 0.82, 'Chat with AI Chatbot')
    uc_mood     = _use_case(ax, 0.40, 0.72, 'Track Mood')
    uc_meditate = _use_case(ax, 0.40, 0.62, 'Browse Meditations')
    uc_book     = _use_case(ax, 0.40, 0.52, 'Book Therapy Session')
    uc_udash    = _use_case(ax, 0.40, 0.42, 'View Dashboard')
    uc_register = _use_case(ax, 0.40, 0.32, 'Register / Login')

    # Therapist use cases (center-bottom)
    uc_tsess    = _use_case(ax, 0.40, 0.20, 'View Sessions')
    uc_tsched   = _use_case(ax, 0.40, 0.10, 'Manage Schedule')

    # Admin use cases (right side inside boundary)
    uc_adash    = _use_case(ax, 0.62, 0.70, 'View Admin Dashboard')
    uc_manage   = _use_case(ax, 0.62, 0.58, 'Manage Users')
    uc_reports  = _use_case(ax, 0.62, 0.46, 'View Reports')

    # Internal use case (shared)
    uc_nlp      = _use_case(ax, 0.62, 0.82, 'Analyze Sentiment\n(NLP)', w=0.17, h=0.06)

    # ── Connections ──
    # User connections
    for uc in [uc_chat, uc_mood, uc_meditate, uc_book, uc_udash, uc_register]:
        ax.plot([0.12, uc[0] - 0.09], [0.58, uc[1]], color=MUTED_TEXT,
                lw=1, zorder=2, alpha=0.7)

    # Therapist connections
    for uc in [uc_tsess, uc_tsched, uc_register]:
        ax.plot([0.12, uc[0] - 0.09], [0.23, uc[1]], color=MUTED_TEXT,
                lw=1, zorder=2, alpha=0.7)

    # Admin connections
    for uc in [uc_adash, uc_manage, uc_reports]:
        ax.plot([0.88, uc[0] + 0.09], [0.58, uc[1]], color=MUTED_TEXT,
                lw=1, zorder=2, alpha=0.7)

    # <<include>> from Chat -> NLP
    ax.annotate('', xy=(uc_nlp[0] - 0.085, uc_nlp[1]),
                xytext=(uc_chat[0] + 0.09, uc_chat[1]),
                arrowprops=dict(arrowstyle='->', color=WARNING, lw=1.5, linestyle='--'))
    ax.text(0.51, 0.84, '<<include>>', ha='center', va='bottom',
            fontsize=8, color=WARNING, style='italic')

    # <<include>> from Mood -> NLP
    ax.annotate('', xy=(uc_nlp[0] - 0.085, uc_nlp[1] - 0.02),
                xytext=(uc_mood[0] + 0.09, uc_mood[1] + 0.01),
                arrowprops=dict(arrowstyle='->', color=WARNING, lw=1.2, linestyle='--'))

    _save(fig, 'fig_3_1_use_case_diagram.png')


# ====================================================================
# Figure 3.2  ER Diagram
# ====================================================================

def fig_3_2_er_diagram():
    fig, ax = _new_figure(18, 11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.97, 'Entity-Relationship Diagram  -  MindfulPath Database',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    def _entity(ax, x, y, title, attrs, w=0.16, line_h=0.025):
        """Draw an ER entity box with attribute rows."""
        h = 0.045 + len(attrs) * line_h
        # Header
        _fancy_box(ax, x, y, w, 0.04, title,
                   color=ACCENT, text_color='white', fontsize=10,
                   edge_color=HIGHLIGHT, linewidth=2, bold=True)
        # Body
        body = FancyBboxPatch((x, y - (h - 0.04)), w, h - 0.04,
                              boxstyle='round,pad=0.005',
                              facecolor=CARD_BG, edgecolor=ACCENT,
                              linewidth=1.2, zorder=2)
        ax.add_patch(body)
        for i, attr in enumerate(attrs):
            ay = y - 0.01 - i * line_h
            color = HIGHLIGHT if attr.startswith('PK') or attr.startswith('FK') else LIGHT_TEXT
            fs = 8 if attr.startswith('PK') or attr.startswith('FK') else 8
            ax.text(x + 0.008, ay, attr, va='top', fontsize=fs,
                    color=color, zorder=3, family='monospace')
        # return center for connectors
        return (x + w / 2, y + 0.02, x, y - (h - 0.04), x + w, y + 0.04, w, h)

    # ── Users (center-top) ──
    u = _entity(ax, 0.42, 0.84, 'users', [
        'PK  id  INTEGER',
        '    username  TEXT',
        '    email  TEXT',
        '    password  TEXT',
        '    role  TEXT',
        '    created_at  DATETIME',
    ])

    # ── therapists (right-top) ──
    t = _entity(ax, 0.75, 0.84, 'therapists', [
        'PK  id  INTEGER',
        'FK  user_id  INTEGER',
        '    specialty  TEXT',
        '    bio  TEXT',
        '    available  BOOLEAN',
    ])

    # ── sessions (far right) ──
    s = _entity(ax, 0.75, 0.54, 'sessions', [
        'PK  id  INTEGER',
        'FK  user_id  INTEGER',
        'FK  therapist_id  INTEGER',
        '    date  DATETIME',
        '    status  TEXT',
        '    notes  TEXT',
    ])

    # ── meditations (far left) ──
    m = _entity(ax, 0.02, 0.84, 'meditations', [
        'PK  id  INTEGER',
        '    title  TEXT',
        '    description  TEXT',
        '    category  TEXT',
        '    duration  INTEGER',
        '    audio_url  TEXT',
    ])

    # ── mood_entries (left) ──
    me = _entity(ax, 0.02, 0.50, 'mood_entries', [
        'PK  id  INTEGER',
        'FK  user_id  INTEGER',
        '    mood  TEXT',
        '    score  INTEGER',
        '    note  TEXT',
        '    created_at  DATETIME',
    ])

    # ── chat_sessions (center) ──
    cs = _entity(ax, 0.30, 0.45, 'chat_sessions', [
        'PK  id  INTEGER',
        'FK  user_id  INTEGER',
        '    started_at  DATETIME',
        '    ended_at  DATETIME',
    ])

    # ── chat_messages (center-right) ──
    cm = _entity(ax, 0.55, 0.35, 'chat_messages', [
        'PK  id  INTEGER',
        'FK  session_id  INTEGER',
        '    sender  TEXT',
        '    message  TEXT',
        '    sentiment  REAL',
        '    created_at  DATETIME',
    ])

    # ── Relationships ──
    def _rel_line(ax, x1, y1, x2, y2, label='1 : M', color=HIGHLIGHT):
        ax.plot([x1, x2], [y1, y2], color=color, lw=1.8, zorder=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.015, label, ha='center', va='bottom',
                fontsize=9, color=WARNING, fontweight='bold',
                bbox=dict(facecolor=DARK_BG, edgecolor='none', pad=1), zorder=6)

    # users -> therapists (1:1)
    _rel_line(ax, 0.58, 0.86, 0.75, 0.86, '1 : 1')

    # users -> sessions (1:M)
    _rel_line(ax, 0.58, 0.80, 0.75, 0.60, '1 : M')

    # users -> mood_entries (1:M)
    _rel_line(ax, 0.42, 0.78, 0.18, 0.56, '1 : M')

    # users -> chat_sessions (1:M)
    _rel_line(ax, 0.48, 0.72, 0.38, 0.52, '1 : M')

    # chat_sessions -> chat_messages (1:M)
    _rel_line(ax, 0.46, 0.42, 0.55, 0.40, '1 : M')

    # therapists -> sessions (1:M)
    _rel_line(ax, 0.83, 0.72, 0.83, 0.60, '1 : M')

    # Legend
    ax.text(0.02, 0.08, 'PK = Primary Key    FK = Foreign Key',
            fontsize=9, color=MUTED_TEXT, style='italic')
    ax.text(0.02, 0.04, 'All tables use SQLite with WAL mode',
            fontsize=9, color=MUTED_TEXT, style='italic')

    _save(fig, 'fig_3_2_er_diagram.png')


# ====================================================================
# Figure 3.3  Data-Flow Diagram (Level 0)
# ====================================================================

def fig_3_3_data_flow_diagram():
    fig, ax = _new_figure(16, 10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.97, 'Data Flow Diagram (Level 0)  -  MindfulPath',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    # ── External entities (rectangles) ──
    def _entity_box(ax, x, y, label):
        _fancy_box(ax, x, y, 0.14, 0.08, label,
                   color=SECONDARY, text_color=LIGHT_TEXT, fontsize=11,
                   edge_color=HIGHLIGHT, linewidth=2, bold=True)

    _entity_box(ax, 0.02, 0.72, 'User /\nPatient')
    _entity_box(ax, 0.02, 0.42, 'Therapist')
    _entity_box(ax, 0.02, 0.14, 'Admin')

    # ── Central process (circle-like rounded box) ──
    central_x, central_y, central_w, central_h = 0.35, 0.35, 0.30, 0.30
    _fancy_box(ax, central_x, central_y, central_w, central_h, '',
               color=ACCENT, edge_color=HIGHLIGHT, linewidth=3,
               style='round,pad=0.03', alpha=0.85)
    ax.text(0.50, 0.54, 'MindfulPath', ha='center', va='center',
            fontsize=16, color='white', fontweight='bold')
    ax.text(0.50, 0.48, 'System', ha='center', va='center',
            fontsize=14, color='white', fontweight='bold')
    ax.text(0.50, 0.40, 'Express.js + NLP + CBT', ha='center', va='center',
            fontsize=10, color=LIGHT_TEXT)

    # ── Data stores (open rectangles) ──
    def _data_store(ax, x, y, label):
        # Two horizontal lines with label
        ax.plot([x, x + 0.17], [y + 0.05, y + 0.05], color=ACCENT, lw=2, zorder=3)
        ax.plot([x, x + 0.17], [y, y], color=ACCENT, lw=2, zorder=3)
        ax.plot([x + 0.03, x + 0.03], [y, y + 0.05], color=ACCENT, lw=1.5, zorder=3)
        bg = FancyBboxPatch((x, y), 0.17, 0.05,
                            boxstyle='square,pad=0',
                            facecolor=CARD_BG, edgecolor='none', zorder=2)
        ax.add_patch(bg)
        ax.text(x + 0.10, y + 0.025, label, ha='center', va='center',
                fontsize=10, color=LIGHT_TEXT, fontweight='bold', zorder=4)

    _data_store(ax, 0.78, 0.72, 'SQLite DB')
    _data_store(ax, 0.78, 0.50, 'NLP Engine')
    _data_store(ax, 0.78, 0.28, 'Session Store')

    # ── Flows: User ──
    _arrow_label(ax, 0.16, 0.78, 0.35, 0.58, 'Chat Messages\nMood Entries', color=HIGHLIGHT, lw=2, fontsize=8)
    _arrow_label(ax, 0.35, 0.54, 0.16, 0.74, 'AI Responses\nDashboard Data', color=SUCCESS, lw=2, fontsize=8)

    # ── Flows: Therapist ──
    _arrow_label(ax, 0.16, 0.48, 0.35, 0.48, 'Schedule\nUpdates', color=HIGHLIGHT, lw=2, fontsize=8)
    _arrow_label(ax, 0.35, 0.44, 0.16, 0.44, 'Session\nDetails', color=SUCCESS, lw=2, fontsize=8)

    # ── Flows: Admin ──
    _arrow_label(ax, 0.16, 0.20, 0.35, 0.38, 'Management\nRequests', color=HIGHLIGHT, lw=2, fontsize=8)
    _arrow_label(ax, 0.35, 0.36, 0.16, 0.16, 'Reports &\nAnalytics', color=SUCCESS, lw=2, fontsize=8)

    # ── Flows: Data stores ──
    _arrow_label(ax, 0.65, 0.58, 0.78, 0.74, 'Read/Write', color=HIGHLIGHT, lw=1.8, fontsize=8)
    _arrow_label(ax, 0.78, 0.72, 0.65, 0.56, 'Query Results', color=SUCCESS, lw=1.8, fontsize=8)

    _arrow_label(ax, 0.65, 0.50, 0.78, 0.53, 'Sentiment\nRequest', color=HIGHLIGHT, lw=1.8, fontsize=8)
    _arrow_label(ax, 0.78, 0.50, 0.65, 0.47, 'Scores &\nLabels', color=SUCCESS, lw=1.8, fontsize=8)

    _arrow_label(ax, 0.65, 0.40, 0.78, 0.32, 'JWT Token\nValidation', color=HIGHLIGHT, lw=1.8, fontsize=8)
    _arrow_label(ax, 0.78, 0.28, 0.65, 0.38, 'Auth\nStatus', color=SUCCESS, lw=1.8, fontsize=8)

    _save(fig, 'fig_3_3_data_flow_diagram.png')


# ====================================================================
# Figure 3.4  NLP / Sentiment Analysis Pipeline
# ====================================================================

def fig_3_4_nlp_pipeline():
    fig, ax = _new_figure(18, 7)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.95, 'NLP Sentiment Analysis Pipeline',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    # Pipeline stages (horizontal flow)
    stages = [
        ('User\nMessage',        'Incoming chat text\nfrom patient'),
        ('Tokenization',         'Split into words\nremove stopwords'),
        ('AFINN Lexicon\nLookup', 'Match tokens to\nsentiment scores'),
        ('Score\nCalculation',   'Sum & normalize\ntoken scores'),
        ('Sentiment\nLabel',     'Positive / Neutral\n/ Negative'),
        ('Crisis\nDetection',    'Flag high-risk\nkeywords'),
        ('CBT Response\nSelection', 'Pick technique:\nCognitive / Behavioral'),
    ]

    n = len(stages)
    box_w = 0.105
    box_h = 0.30
    gap = (1.0 - 0.06 - n * box_w) / (n - 1)  # evenly space

    start_x = 0.03
    base_y = 0.35

    for i, (title, desc) in enumerate(stages):
        x = start_x + i * (box_w + gap)

        # Alternate colors for visual interest
        bg = CARD_BG if i % 2 == 0 else SECONDARY
        ec = ACCENT if i != 5 else DANGER  # red border on Crisis Detection

        _fancy_box(ax, x, base_y, box_w, box_h, '',
                   color=bg, edge_color=ec, linewidth=2)

        # Stage number circle
        circle = plt.Circle((x + box_w / 2, base_y + box_h - 0.035), 0.018,
                             color=ACCENT, zorder=5)
        ax.add_patch(circle)
        ax.text(x + box_w / 2, base_y + box_h - 0.035, str(i + 1),
                ha='center', va='center', fontsize=10, color='white',
                fontweight='bold', zorder=6)

        # Title
        ax.text(x + box_w / 2, base_y + box_h - 0.10, title,
                ha='center', va='center', fontsize=10, color=HIGHLIGHT,
                fontweight='bold', zorder=4)

        # Description
        ax.text(x + box_w / 2, base_y + 0.07, desc,
                ha='center', va='center', fontsize=8, color=MUTED_TEXT, zorder=4)

        # Arrow to next
        if i < n - 1:
            ax.annotate('',
                        xy=(x + box_w + gap * 0.15, base_y + box_h / 2),
                        xytext=(x + box_w + 0.003, base_y + box_h / 2),
                        arrowprops=dict(arrowstyle='->', color=HIGHLIGHT,
                                        lw=2.5, mutation_scale=18),
                        zorder=7)

    # Bottom legend bar
    legend_items = [
        (ACCENT, 'Standard Stage'),
        (DANGER, 'Crisis Detection (Red Border)'),
        (HIGHLIGHT, 'Data Flow Direction'),
    ]
    for i, (c, lbl) in enumerate(legend_items):
        lx = 0.15 + i * 0.28
        ax.plot([lx, lx + 0.03], [0.15, 0.15], color=c, lw=3)
        ax.text(lx + 0.04, 0.15, lbl, va='center', fontsize=9, color=MUTED_TEXT)

    # Extra info
    ax.text(0.50, 0.07, 'AFINN lexicon assigns integer scores (-5 to +5) to ~2,500 English words.\n'
            'Crisis keywords (e.g., "suicide", "self-harm") trigger immediate safety resources.',
            ha='center', va='center', fontsize=9, color=MUTED_TEXT, style='italic')

    _save(fig, 'fig_3_4_nlp_pipeline.png')


# ====================================================================
# Figure 3.5  Activity Diagram  -  Chat Interaction Flow
# ====================================================================

def fig_3_5_activity_diagram():
    fig, ax = _new_figure(14, 12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.98, 'Activity Diagram  -  AI Chat Interaction',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    # Vertical flow, centered
    cx = 0.50

    # Start node (filled circle)
    start = plt.Circle((cx, 0.92), 0.015, color=HIGHLIGHT, zorder=5)
    ax.add_patch(start)

    # Activity boxes
    activities = [
        (0.86, 'User Opens Chat'),
        (0.78, 'New Chat Session Created'),
        (0.70, 'User Sends Message'),
        (0.61, 'Sentiment Analysis\n(AFINN Lexicon)'),
        (0.52, 'Crisis Keyword Check'),
        # Diamond decision at 0.44
        (0.34, 'Select CBT Technique'),
        (0.26, 'Generate AI Response'),
        (0.18, 'Display Response to User'),
    ]

    box_w, box_h = 0.28, 0.055

    for y_pos, label in activities:
        bg = CARD_BG
        ec = ACCENT
        if 'Crisis' in label:
            ec = DANGER
        if 'Sentiment' in label:
            ec = WARNING
        _fancy_box(ax, cx - box_w / 2, y_pos, box_w, box_h, label,
                   color=bg, edge_color=ec, linewidth=1.8, fontsize=10)

    # Decision diamond for crisis
    diamond_y = 0.445
    diamond_size = 0.032
    diamond = plt.Polygon([
        (cx, diamond_y + diamond_size),
        (cx + diamond_size * 1.5, diamond_y),
        (cx, diamond_y - diamond_size),
        (cx - diamond_size * 1.5, diamond_y),
    ], closed=True, facecolor=SECONDARY, edgecolor=DANGER, linewidth=2, zorder=5)
    ax.add_patch(diamond)
    ax.text(cx, diamond_y, 'Crisis?', ha='center', va='center',
            fontsize=9, color=LIGHT_TEXT, fontweight='bold', zorder=6)

    # Crisis branch (right) -> Show Emergency Resources
    _fancy_box(ax, 0.72, diamond_y - 0.025, 0.22, 0.05,
               'Show Emergency\nResources & Helplines',
               color=CARD_BG, edge_color=DANGER, linewidth=2, fontsize=9)
    ax.annotate('', xy=(0.72, diamond_y),
                xytext=(cx + diamond_size * 1.5, diamond_y),
                arrowprops=dict(arrowstyle='->', color=DANGER, lw=2))
    ax.text(cx + diamond_size * 1.5 + 0.04, diamond_y + 0.015, 'Yes',
            fontsize=9, color=DANGER, fontweight='bold')

    # No branch (down)
    ax.text(cx + 0.025, diamond_y - diamond_size - 0.01, 'No',
            fontsize=9, color=SUCCESS, fontweight='bold')

    # Arrows between activities
    arrow_props = dict(arrowstyle='->', color=HIGHLIGHT, lw=2, mutation_scale=15)

    # Start -> first activity
    ax.annotate('', xy=(cx, 0.86 + box_h), xytext=(cx, 0.92 - 0.015),
                arrowprops=arrow_props)

    # Between consecutive activities
    flow_ys = [0.86, 0.78, 0.70, 0.61, 0.52]
    for i in range(len(flow_ys) - 1):
        ax.annotate('', xy=(cx, flow_ys[i + 1] + box_h),
                    xytext=(cx, flow_ys[i]),
                    arrowprops=arrow_props)

    # Crisis check -> diamond
    ax.annotate('', xy=(cx, diamond_y + diamond_size),
                xytext=(cx, 0.52),
                arrowprops=arrow_props)

    # Diamond (no) -> Select CBT
    ax.annotate('', xy=(cx, 0.34 + box_h),
                xytext=(cx, diamond_y - diamond_size),
                arrowprops=arrow_props)

    # Select CBT -> Generate
    ax.annotate('', xy=(cx, 0.26 + box_h),
                xytext=(cx, 0.34),
                arrowprops=arrow_props)

    # Generate -> Display
    ax.annotate('', xy=(cx, 0.18 + box_h),
                xytext=(cx, 0.26),
                arrowprops=arrow_props)

    # Loop back arrow (Display -> User Sends Message)
    # Right side loop
    loop_x = 0.82
    ax.plot([cx + box_w / 2, loop_x], [0.205, 0.205], color=HIGHLIGHT, lw=1.8, zorder=3)
    ax.plot([loop_x, loop_x], [0.205, 0.725], color=HIGHLIGHT, lw=1.8, zorder=3)
    ax.annotate('', xy=(cx + box_w / 2, 0.725),
                xytext=(loop_x, 0.725),
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=1.8, mutation_scale=15))
    ax.text(loop_x + 0.02, 0.46, 'Continue\nConversation', ha='left', va='center',
            fontsize=9, color=MUTED_TEXT, style='italic', rotation=90)

    # Emergency resources also loops back
    ax.plot([0.83, 0.88], [diamond_y - 0.025, diamond_y - 0.025], color=DANGER, lw=1.2, zorder=3)
    ax.plot([0.88, 0.88], [diamond_y - 0.025, 0.205], color=DANGER, lw=1.2, zorder=3)
    ax.annotate('', xy=(loop_x + 0.001, 0.205),
                xytext=(0.88, 0.205),
                arrowprops=dict(arrowstyle='->', color=DANGER, lw=1.2, mutation_scale=12))

    # End node (circle with inner circle)
    end_y = 0.08
    end_outer = plt.Circle((cx, end_y), 0.018, color=HIGHLIGHT,
                            fill=False, linewidth=2.5, zorder=5)
    end_inner = plt.Circle((cx, end_y), 0.010, color=HIGHLIGHT, zorder=5)
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)
    ax.annotate('', xy=(cx, end_y + 0.018),
                xytext=(cx, 0.18),
                arrowprops=dict(arrowstyle='->', color=MUTED_TEXT, lw=1.5,
                                linestyle='--', mutation_scale=12))
    ax.text(cx - 0.04, 0.12, 'User\nCloses\nChat', ha='center', va='center',
            fontsize=8, color=MUTED_TEXT, style='italic')

    _save(fig, 'fig_3_5_activity_diagram.png')


# ====================================================================
# Figure 4.1  Agile Methodology  -  Sprint Timeline
# ====================================================================

def fig_4_1_agile_methodology():
    fig, ax = _new_figure(18, 9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.50, 0.96, 'Agile Development Methodology  -  Sprint Plan',
            ha='center', va='top', fontsize=18, color=LIGHT_TEXT, fontweight='bold')

    sprints = [
        {
            'name': 'Sprint 1',
            'weeks': 'Weeks 1-2',
            'title': 'Foundation',
            'tasks': [
                'Database Schema Design',
                'User Authentication',
                'JWT Token System',
                'Role-Based Access Control',
                'Project Setup & Config',
            ],
            'color': '#6366f1',  # indigo
        },
        {
            'name': 'Sprint 2',
            'weeks': 'Weeks 3-4',
            'title': 'NLP Engine & Chatbot',
            'tasks': [
                'AFINN Lexicon Integration',
                'Sentiment Analysis Module',
                'Crisis Detection System',
                'CBT Response Templates',
                'Chat Session Management',
            ],
            'color': ACCENT,
        },
        {
            'name': 'Sprint 3',
            'weeks': 'Weeks 5-6',
            'title': 'Mood & Meditations',
            'tasks': [
                'Mood Entry CRUD',
                'Mood Analytics Dashboard',
                'Chart.js Visualizations',
                'Meditation Library',
                'Category & Search Filters',
            ],
            'color': '#8b5cf6',
        },
        {
            'name': 'Sprint 4',
            'weeks': 'Weeks 7-8',
            'title': 'Therapist & Sessions',
            'tasks': [
                'Therapist Directory',
                'Session Booking System',
                'Schedule Management',
                'Email Notifications',
                'Therapist Dashboard',
            ],
            'color': '#a855f7',
        },
        {
            'name': 'Sprint 5',
            'weeks': 'Weeks 9-10',
            'title': 'Dashboard & Deploy',
            'tasks': [
                'Admin Dashboard',
                'User Analytics',
                'Integration Testing',
                'Docker Containerization',
                'Documentation & README',
            ],
            'color': '#c084fc',
        },
    ]

    n = len(sprints)
    col_w = 0.17
    gap = (1.0 - 0.04 - n * col_w) / (n - 1) if n > 1 else 0
    base_x = 0.02
    top_y = 0.82

    for i, sp in enumerate(sprints):
        x = base_x + i * (col_w + gap)

        # Sprint header
        _fancy_box(ax, x, top_y, col_w, 0.08, f"{sp['name']}\n{sp['weeks']}",
                   color=sp['color'], text_color='white', fontsize=11,
                   edge_color=HIGHLIGHT, linewidth=2, bold=True)

        # Sprint subtitle
        _fancy_box(ax, x, top_y - 0.055, col_w, 0.045, sp['title'],
                   color=SECONDARY, text_color=HIGHLIGHT, fontsize=10,
                   edge_color=sp['color'], linewidth=1.5, bold=True)

        # Task items
        for j, task in enumerate(sp['tasks']):
            ty = top_y - 0.12 - j * 0.065
            _fancy_box(ax, x + 0.005, ty, col_w - 0.01, 0.05, task,
                       color=CARD_BG, text_color=LIGHT_TEXT, fontsize=8.5,
                       edge_color=sp['color'], linewidth=1)

            # Checkmark
            ax.text(x + 0.015, ty + 0.025, '\u2713', ha='center', va='center',
                    fontsize=10, color=SUCCESS, fontweight='bold', zorder=5)

        # Arrow to next sprint
        if i < n - 1:
            ax.annotate('',
                        xy=(x + col_w + gap * 0.15, top_y - 0.20),
                        xytext=(x + col_w + 0.005, top_y - 0.20),
                        arrowprops=dict(arrowstyle='->', color=HIGHLIGHT,
                                        lw=2.5, mutation_scale=18),
                        zorder=7)

    # Timeline bar at bottom
    bar_y = 0.10
    ax.plot([0.05, 0.95], [bar_y, bar_y], color=ACCENT, lw=3, zorder=3)
    for i in range(n):
        dot_x = 0.05 + i * (0.90 / (n - 1))
        circle = plt.Circle((dot_x, bar_y), 0.012, color=sprints[i]['color'], zorder=5)
        ax.add_patch(circle)
        ax.text(dot_x, bar_y - 0.035, sprints[i]['name'],
                ha='center', va='top', fontsize=10, color=LIGHT_TEXT, fontweight='bold')
        ax.text(dot_x, bar_y - 0.06, sprints[i]['weeks'],
                ha='center', va='top', fontsize=8, color=MUTED_TEXT)

    # Methodology badges
    badges = ['Iterative Development', 'Continuous Testing', 'Sprint Reviews', 'Retrospectives']
    for i, b in enumerate(badges):
        bx = 0.12 + i * 0.22
        _fancy_box(ax, bx, 0.01, 0.16, 0.04, b,
                   color=SECONDARY, text_color=MUTED_TEXT, fontsize=8,
                   edge_color=ACCENT, linewidth=1)

    _save(fig, 'fig_4_1_agile_methodology.png')


# ====================================================================
# Main
# ====================================================================

def main():
    print("Generating MindfulPath project figures ...\n")

    fig_1_1_system_architecture()
    print()
    fig_3_1_use_case_diagram()
    print()
    fig_3_2_er_diagram()
    print()
    fig_3_3_data_flow_diagram()
    print()
    fig_3_4_nlp_pipeline()
    print()
    fig_3_5_activity_diagram()
    print()
    fig_4_1_agile_methodology()

    print(f"\nAll 7 figures saved to: {SAVE_DIR}")


if __name__ == '__main__':
    main()
