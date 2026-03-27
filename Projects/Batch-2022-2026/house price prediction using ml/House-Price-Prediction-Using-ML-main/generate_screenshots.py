"""
generate_screenshots.py
Generates application screenshot mockups for the C4 House Price Prediction project.
Uses matplotlib to create professional dark-themed UI mockups resembling a Flask + Bootstrap 5 web app.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import os

# ─── Global Style Constants ─────────────────────────────────────────────────
BG_DARK      = '#1a1a2e'
BG_CARD      = '#16213e'
BG_NAVBAR    = '#0f3460'
BG_INPUT     = '#0d1b2a'
BG_TABLE_ROW = '#1b2838'
BG_TABLE_ALT = '#162032'
TEXT_WHITE    = '#ffffff'
TEXT_LIGHT    = '#c8d6e5'
TEXT_MUTED    = '#8395a7'
ACCENT_BLUE  = '#0d6efd'
ACCENT_GREEN = '#28a745'
ACCENT_RED   = '#dc3545'
ACCENT_GOLD  = '#ffc107'
BORDER_COLOR = '#2d4059'

OUTPUT_DIR = '/Users/shoukathali/lord-major-projects/IV-C Projects/C4/figures'
DPI = 150

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─── Helper Drawing Functions ────────────────────────────────────────────────

def draw_rounded_rect(ax, x, y, w, h, color, radius=0.02, alpha=1.0, edgecolor=None, linewidth=0):
    """Draw a rounded rectangle on the axes."""
    ec = edgecolor if edgecolor else color
    fancy = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor=ec, linewidth=linewidth, alpha=alpha,
        transform=ax.transAxes, clip_on=False
    )
    ax.add_patch(fancy)
    return fancy


def draw_input_field(ax, x, y, w, h, label='', placeholder='', label_size=8):
    """Draw a form input field with label."""
    if label:
        ax.text(x, y + h + 0.015, label, transform=ax.transAxes,
                fontsize=label_size, color=TEXT_LIGHT, va='bottom', ha='left',
                fontfamily='sans-serif')
    draw_rounded_rect(ax, x, y, w, h, BG_INPUT, radius=0.008,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    if placeholder:
        ax.text(x + 0.015, y + h / 2, placeholder, transform=ax.transAxes,
                fontsize=7, color=TEXT_MUTED, va='center', ha='left',
                fontfamily='sans-serif')


def draw_button(ax, x, y, w, h, text, color=ACCENT_BLUE, text_color=TEXT_WHITE, fontsize=9):
    """Draw a styled button."""
    draw_rounded_rect(ax, x, y, w, h, color, radius=0.008)
    ax.text(x + w / 2, y + h / 2, text, transform=ax.transAxes,
            fontsize=fontsize, color=text_color, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')


def draw_navbar(ax, active='Home'):
    """Draw the top navigation bar."""
    draw_rounded_rect(ax, 0, 0.92, 1.0, 0.08, BG_NAVBAR, radius=0.0)
    ax.text(0.03, 0.96, 'House Price Predictor', transform=ax.transAxes,
            fontsize=11, color=TEXT_WHITE, va='center', ha='left',
            fontweight='bold', fontfamily='sans-serif')

    nav_items = ['Home', 'Predict', 'History', 'Visualize', 'Dashboard', 'About', 'Logout']
    start_x = 0.38
    for i, item in enumerate(nav_items):
        xp = start_x + i * 0.09
        c = ACCENT_BLUE if item == active else TEXT_LIGHT
        fw = 'bold' if item == active else 'normal'
        ax.text(xp, 0.96, item, transform=ax.transAxes,
                fontsize=7.5, color=c, va='center', ha='center',
                fontweight=fw, fontfamily='sans-serif')


def new_figure(figsize=(10, 7)):
    """Create a new figure with dark background."""
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig, ax


def save_figure(fig, filename):
    """Save figure to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor(),
                edgecolor='none', pad_inches=0.05)
    plt.close(fig)
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def gen_login():
    fig, ax = new_figure()
    # Center card
    cw, ch = 0.36, 0.52
    cx, cy = 0.5 - cw / 2, 0.5 - ch / 2
    draw_rounded_rect(ax, cx, cy, cw, ch, BG_CARD, radius=0.015,
                      edgecolor=BORDER_COLOR, linewidth=1)

    # Title
    ax.text(0.5, cy + ch - 0.06, 'Login', transform=ax.transAxes,
            fontsize=20, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')

    # Divider line
    ax.plot([cx + 0.04, cx + cw - 0.04], [cy + ch - 0.10, cy + ch - 0.10],
            color=BORDER_COLOR, linewidth=0.8, transform=ax.transAxes)

    # Fields
    fw = cw - 0.08
    fx = cx + 0.04
    draw_input_field(ax, fx, cy + ch - 0.24, fw, 0.055, 'Username or Email', 'Enter your username or email')
    draw_input_field(ax, fx, cy + ch - 0.38, fw, 0.055, 'Password', 'Enter your password')

    # Login button
    draw_button(ax, fx, cy + 0.08, fw, 0.055, 'Login')

    # Register link
    ax.text(0.5, cy + 0.035, "Don't have an account? Register here",
            transform=ax.transAxes, fontsize=7.5, color=ACCENT_BLUE,
            va='center', ha='center', fontfamily='sans-serif')

    # Subtle app title at top
    ax.text(0.5, 0.90, 'House Price Predictor', transform=ax.transAxes,
            fontsize=14, color=TEXT_MUTED, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif', alpha=0.6)

    save_figure(fig, 'fig_7_1_login.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 2. REGISTER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def gen_register():
    fig, ax = new_figure()
    cw, ch = 0.38, 0.68
    cx, cy = 0.5 - cw / 2, 0.5 - ch / 2 - 0.02
    draw_rounded_rect(ax, cx, cy, cw, ch, BG_CARD, radius=0.015,
                      edgecolor=BORDER_COLOR, linewidth=1)

    ax.text(0.5, cy + ch - 0.055, 'Register', transform=ax.transAxes,
            fontsize=20, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.plot([cx + 0.04, cx + cw - 0.04], [cy + ch - 0.095, cy + ch - 0.095],
            color=BORDER_COLOR, linewidth=0.8, transform=ax.transAxes)

    fw = cw - 0.08
    fx = cx + 0.04
    fields = [('Username', 'Choose a username'),
              ('Email', 'Enter your email address'),
              ('Password', 'Create a password'),
              ('Confirm Password', 'Re-enter your password')]

    for i, (lbl, ph) in enumerate(fields):
        fy = cy + ch - 0.22 - i * 0.125
        draw_input_field(ax, fx, fy, fw, 0.05, lbl, ph)

    draw_button(ax, fx, cy + 0.07, fw, 0.055, 'Register')
    ax.text(0.5, cy + 0.03, 'Already have an account? Login here',
            transform=ax.transAxes, fontsize=7.5, color=ACCENT_BLUE,
            va='center', ha='center', fontfamily='sans-serif')

    ax.text(0.5, 0.93, 'House Price Predictor', transform=ax.transAxes,
            fontsize=14, color=TEXT_MUTED, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif', alpha=0.6)

    save_figure(fig, 'fig_7_2_register.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 3. HOME / DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def gen_home():
    fig, ax = new_figure()
    draw_navbar(ax, active='Home')

    # Welcome
    ax.text(0.5, 0.84, 'Welcome back, User!', transform=ax.transAxes,
            fontsize=18, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, 0.79, 'Predict California house prices using advanced Machine Learning models.',
            transform=ax.transAxes, fontsize=9, color=TEXT_MUTED, va='center', ha='center',
            fontfamily='sans-serif')

    # Quick stats cards
    stats = [
        ('Total Predictions', '1,247', ACCENT_BLUE),
        ('Your Predictions', '38', ACCENT_GREEN),
        ('Best Model', 'Gradient Boosting', ACCENT_GOLD),
    ]
    card_w, card_h = 0.26, 0.18
    gap = 0.035
    total_w = 3 * card_w + 2 * gap
    sx = (1 - total_w) / 2

    for i, (title, value, color) in enumerate(stats):
        cx = sx + i * (card_w + gap)
        cy = 0.52
        draw_rounded_rect(ax, cx, cy, card_w, card_h, BG_CARD, radius=0.012,
                          edgecolor=BORDER_COLOR, linewidth=0.8)
        # Colored top bar
        draw_rounded_rect(ax, cx, cy + card_h - 0.015, card_w, 0.015, color, radius=0.005)
        ax.text(cx + card_w / 2, cy + card_h - 0.055, title, transform=ax.transAxes,
                fontsize=9, color=TEXT_MUTED, va='center', ha='center', fontfamily='sans-serif')
        ax.text(cx + card_w / 2, cy + 0.055, value, transform=ax.transAxes,
                fontsize=16, color=TEXT_WHITE, va='center', ha='center',
                fontweight='bold', fontfamily='sans-serif')

    # Quick actions
    ax.text(0.5, 0.44, 'Quick Actions', transform=ax.transAxes,
            fontsize=13, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')

    actions = [('Make a Prediction', ACCENT_BLUE), ('View History', '#6c757d'),
               ('Explore Data', '#17a2b8')]
    bw, bh = 0.20, 0.05
    total_bw = 3 * bw + 2 * 0.03
    bsx = (1 - total_bw) / 2
    for i, (label, col) in enumerate(actions):
        bx = bsx + i * (bw + 0.03)
        draw_button(ax, bx, 0.34, bw, bh, label, color=col, fontsize=8)

    # Footer
    ax.text(0.5, 0.05, 'House Price Predictor v1.0  |  Built with Flask & Scikit-Learn',
            transform=ax.transAxes, fontsize=7, color=TEXT_MUTED, va='center', ha='center',
            fontfamily='sans-serif', alpha=0.7)

    save_figure(fig, 'fig_7_3_home.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PREDICTION FORM
# ═══════════════════════════════════════════════════════════════════════════════
def gen_predict():
    fig, ax = new_figure((10, 8))
    draw_navbar(ax, active='Predict')

    # Title
    ax.text(0.5, 0.87, 'Predict House Price', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, 0.835, 'Enter the property details below to get an estimated price.',
            transform=ax.transAxes, fontsize=8, color=TEXT_MUTED, va='center', ha='center',
            fontfamily='sans-serif')

    # Form card
    cw, ch = 0.82, 0.68
    cx = (1 - cw) / 2
    cy = 0.10
    draw_rounded_rect(ax, cx, cy, cw, ch, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)

    fields = [
        ('Longitude', '-122.23'),
        ('Latitude', '37.88'),
        ('Housing Median Age', '41'),
        ('Total Rooms', '880'),
        ('Total Bedrooms', '129'),
        ('Population', '322'),
        ('Households', '126'),
        ('Median Income', '8.3252'),
        ('Ocean Proximity', '<1H OCEAN  v'),
    ]

    col_w = 0.34
    fh = 0.042
    row_gap = 0.085
    margin_x = cx + 0.04
    top_y = cy + ch - 0.06

    for i, (label, placeholder) in enumerate(fields):
        col = i % 2
        row = i // 2
        fx = margin_x + col * (col_w + 0.06)
        fy = top_y - (row + 1) * row_gap
        draw_input_field(ax, fx, fy, col_w, fh, label, placeholder, label_size=7.5)

    # Predict button
    bw = 0.22
    draw_button(ax, 0.5 - bw / 2, cy + 0.03, bw, 0.05, 'Predict Price', fontsize=10)

    save_figure(fig, 'fig_7_4_predict.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 5. PREDICTION RESULT
# ═══════════════════════════════════════════════════════════════════════════════
def gen_result():
    fig, ax = new_figure((10, 8))
    draw_navbar(ax, active='Predict')

    ax.text(0.5, 0.87, 'Prediction Result', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')

    # Result card
    rw, rh = 0.55, 0.20
    rx = (1 - rw) / 2
    ry = 0.65
    draw_rounded_rect(ax, rx, ry, rw, rh, '#0b2e1a', radius=0.012,
                      edgecolor=ACCENT_GREEN, linewidth=1.5)
    ax.text(0.5, ry + rh - 0.045, 'Predicted House Price',
            transform=ax.transAxes, fontsize=10, color=TEXT_LIGHT,
            va='center', ha='center', fontfamily='sans-serif')
    ax.text(0.5, ry + 0.065, '$245,678', transform=ax.transAxes,
            fontsize=32, color=ACCENT_GREEN, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, ry + 0.02, 'Model: Gradient Boosting  |  Confidence: High',
            transform=ax.transAxes, fontsize=7.5, color=TEXT_MUTED,
            va='center', ha='center', fontfamily='sans-serif')

    # Input summary card
    sw, sh = 0.72, 0.38
    sx_card = (1 - sw) / 2
    sy = 0.18
    draw_rounded_rect(ax, sx_card, sy, sw, sh, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    ax.text(0.5, sy + sh - 0.035, 'Input Summary', transform=ax.transAxes,
            fontsize=10, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.plot([sx_card + 0.03, sx_card + sw - 0.03],
            [sy + sh - 0.06, sy + sh - 0.06],
            color=BORDER_COLOR, linewidth=0.6, transform=ax.transAxes)

    summary_items = [
        ('Longitude', '-122.23'), ('Latitude', '37.88'),
        ('Housing Median Age', '41'), ('Total Rooms', '880'),
        ('Total Bedrooms', '129'), ('Population', '322'),
        ('Households', '126'), ('Median Income', '8.3252'),
        ('Ocean Proximity', '<1H OCEAN'),
    ]
    col1_x = sx_card + 0.05
    col2_x = sx_card + 0.27
    col3_x = sx_card + 0.49
    for i, (k, v) in enumerate(summary_items):
        col = i // 3
        row = i % 3
        if col == 0:
            kx, vx = col1_x, col1_x + 0.12
        elif col == 1:
            kx, vx = col2_x, col2_x + 0.12
        else:
            kx, vx = col3_x, col3_x + 0.12
        yy = sy + sh - 0.10 - row * 0.075
        ax.text(kx, yy, f'{k}:', transform=ax.transAxes, fontsize=7,
                color=TEXT_MUTED, va='center', ha='left', fontfamily='sans-serif')
        ax.text(vx, yy, v, transform=ax.transAxes, fontsize=7.5,
                color=TEXT_WHITE, va='center', ha='left', fontweight='bold',
                fontfamily='sans-serif')

    # Buttons
    draw_button(ax, 0.30, 0.08, 0.18, 0.045, 'New Prediction', ACCENT_BLUE, fontsize=8)
    draw_button(ax, 0.52, 0.08, 0.18, 0.045, 'Save to History', '#6c757d', fontsize=8)

    save_figure(fig, 'fig_7_5_result.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 6. PREDICTION HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
def gen_history():
    fig, ax = new_figure((10, 7))
    draw_navbar(ax, active='History')

    ax.text(0.5, 0.87, 'Prediction History', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, 0.835, 'Your past prediction records',
            transform=ax.transAxes, fontsize=8, color=TEXT_MUTED, va='center', ha='center',
            fontfamily='sans-serif')

    # Table card
    tw, th = 0.92, 0.62
    tx = (1 - tw) / 2
    ty = 0.14
    draw_rounded_rect(ax, tx, ty, tw, th, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)

    headers = ['Date', 'Longitude', 'Latitude', 'Age', 'Rooms', 'Income',
               'Ocean Proximity', 'Predicted Price']
    col_widths = [0.13, 0.10, 0.09, 0.06, 0.08, 0.08, 0.16, 0.14]
    col_x = [tx + 0.02]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    header_y = ty + th - 0.05
    # Header bg
    draw_rounded_rect(ax, tx + 0.01, header_y - 0.015, tw - 0.02, 0.04, BG_NAVBAR, radius=0.005)
    for j, hdr in enumerate(headers):
        ax.text(col_x[j] + col_widths[j] / 2, header_y, hdr, transform=ax.transAxes,
                fontsize=7, color=TEXT_WHITE, va='center', ha='center',
                fontweight='bold', fontfamily='sans-serif')

    rows = [
        ['2025-03-01', '-122.23', '37.88', '41', '880', '8.33', '<1H OCEAN', '$245,678'],
        ['2025-02-28', '-118.49', '34.26', '29', '2,125', '5.64', 'NEAR BAY', '$198,340'],
        ['2025-02-27', '-121.97', '37.35', '52', '1,467', '3.85', 'INLAND', '$142,560'],
        ['2025-02-25', '-117.23', '32.75', '15', '3,200', '7.12', 'NEAR OCEAN', '$312,450'],
        ['2025-02-24', '-119.78', '36.78', '36', '950', '4.21', 'INLAND', '$156,890'],
    ]

    row_h = 0.065
    for i, row in enumerate(rows):
        ry = header_y - 0.065 - i * row_h
        bg = BG_TABLE_ROW if i % 2 == 0 else BG_TABLE_ALT
        draw_rounded_rect(ax, tx + 0.01, ry - 0.015, tw - 0.02, row_h - 0.005,
                          bg, radius=0.004)
        for j, val in enumerate(row):
            c = ACCENT_GREEN if j == len(row) - 1 else TEXT_LIGHT
            fw = 'bold' if j == len(row) - 1 else 'normal'
            ax.text(col_x[j] + col_widths[j] / 2, ry + 0.012, val,
                    transform=ax.transAxes, fontsize=6.5, color=c,
                    va='center', ha='center', fontweight=fw, fontfamily='sans-serif')

    # Pagination
    ax.text(0.5, ty + 0.03, 'Showing 1 - 5 of 38 predictions',
            transform=ax.transAxes, fontsize=7, color=TEXT_MUTED,
            va='center', ha='center', fontfamily='sans-serif')

    save_figure(fig, 'fig_7_6_history.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 7. EDA VISUALIZATION PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def gen_visualize():
    fig, ax = new_figure((10, 7))
    draw_navbar(ax, active='Visualize')

    ax.text(0.5, 0.87, 'Exploratory Data Analysis', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, 0.835, 'Visual insights from the California Housing dataset',
            transform=ax.transAxes, fontsize=8, color=TEXT_MUTED, va='center', ha='center',
            fontfamily='sans-serif')

    charts = [
        ('Price Distribution', 'histogram'),
        ('Correlation Heatmap', 'heatmap'),
        ('Feature Importance', 'bar'),
        ('Ocean Proximity Impact', 'box'),
        ('Geographic Map', 'scatter'),
        ('Income vs Price', 'scatter2'),
    ]

    card_w, card_h = 0.27, 0.30
    gap_x, gap_y = 0.04, 0.05
    cols, rows = 3, 2
    total_w = cols * card_w + (cols - 1) * gap_x
    total_h = rows * card_h + (rows - 1) * gap_y
    start_x = (1 - total_w) / 2
    start_y = 0.80 - total_h

    np.random.seed(42)

    for idx, (title, chart_type) in enumerate(charts):
        col = idx % cols
        row = idx // cols
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + (1 - row) * (card_h + gap_y)

        draw_rounded_rect(ax, cx, cy, card_w, card_h, BG_CARD, radius=0.012,
                          edgecolor=BORDER_COLOR, linewidth=0.8)

        ax.text(cx + card_w / 2, cy + card_h - 0.03, title,
                transform=ax.transAxes, fontsize=8, color=TEXT_WHITE,
                va='center', ha='center', fontweight='bold', fontfamily='sans-serif')

        # Mini chart area
        chart_x = cx + 0.02
        chart_y = cy + 0.025
        chart_w = card_w - 0.04
        chart_h = card_h - 0.08

        # Draw mini chart thumbnails
        if chart_type == 'histogram':
            n_bars = 15
            heights = np.random.exponential(0.6, n_bars)
            heights = heights / heights.max() * chart_h * 0.85
            bw = chart_w / (n_bars + 1)
            for bi in range(n_bars):
                bx = chart_x + bi * bw + bw * 0.1
                bh = heights[bi]
                draw_rounded_rect(ax, bx, chart_y, bw * 0.8, bh, ACCENT_BLUE,
                                  radius=0.002, alpha=0.8)

        elif chart_type == 'heatmap':
            n = 5
            cell_w = chart_w / n
            cell_h = chart_h / n
            for r in range(n):
                for c in range(n):
                    val = np.random.uniform(0.2, 1.0) if r != c else 1.0
                    if abs(r - c) <= 1:
                        val = np.random.uniform(0.6, 1.0)
                    color_val = plt.cm.RdYlBu_r(val)
                    rect = Rectangle((chart_x + c * cell_w, chart_y + r * cell_h),
                                     cell_w * 0.95, cell_h * 0.95,
                                     facecolor=color_val, transform=ax.transAxes)
                    ax.add_patch(rect)

        elif chart_type == 'bar':
            vals = [0.9, 0.55, 0.45, 0.40, 0.35, 0.20, 0.15]
            bh_each = chart_h / (len(vals) + 1)
            for bi, v in enumerate(vals):
                bar_y = chart_y + chart_h - (bi + 1) * bh_each
                bar_w = v * chart_w * 0.85
                draw_rounded_rect(ax, chart_x, bar_y, bar_w, bh_each * 0.7,
                                  ACCENT_GREEN, radius=0.002, alpha=0.8)

        elif chart_type == 'box':
            for bi in range(4):
                bx = chart_x + bi * chart_w / 4 + chart_w / 16
                bw_box = chart_w / 6
                median_y = chart_y + np.random.uniform(0.3, 0.7) * chart_h
                q1 = median_y - np.random.uniform(0.05, 0.08)
                q3 = median_y + np.random.uniform(0.05, 0.08)
                draw_rounded_rect(ax, bx, q1, bw_box, q3 - q1, ACCENT_GOLD,
                                  radius=0.002, alpha=0.7)
                ax.plot([bx, bx + bw_box], [median_y, median_y],
                        color=TEXT_WHITE, linewidth=1.2, transform=ax.transAxes)

        elif chart_type == 'scatter':
            n_pts = 40
            xs = np.random.uniform(chart_x + 0.01, chart_x + chart_w - 0.01, n_pts)
            ys = np.random.uniform(chart_y + 0.01, chart_y + chart_h - 0.01, n_pts)
            colors = plt.cm.plasma(np.random.uniform(0.2, 0.9, n_pts))
            for pi in range(n_pts):
                ax.plot(xs[pi], ys[pi], 'o', color=colors[pi], markersize=2.5,
                        transform=ax.transAxes, alpha=0.8)

        elif chart_type == 'scatter2':
            n_pts = 35
            xs = np.linspace(chart_x + 0.01, chart_x + chart_w - 0.01, n_pts)
            ys = chart_y + 0.02 + (xs - chart_x) / chart_w * chart_h * 0.7 + \
                 np.random.normal(0, chart_h * 0.08, n_pts)
            for pi in range(n_pts):
                ax.plot(xs[pi], ys[pi], 'o', color=ACCENT_BLUE, markersize=2.5,
                        transform=ax.transAxes, alpha=0.7)
            # Trend line
            ax.plot([chart_x + 0.01, chart_x + chart_w - 0.01],
                    [chart_y + 0.03, chart_y + chart_h * 0.75],
                    color=ACCENT_RED, linewidth=1.2, transform=ax.transAxes,
                    linestyle='--', alpha=0.8)

    save_figure(fig, 'fig_7_7_visualize.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 8. MODEL DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def gen_dashboard():
    fig, ax = new_figure((10, 8))
    draw_navbar(ax, active='Dashboard')

    ax.text(0.5, 0.87, 'Model Performance Dashboard', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')

    # Model comparison table
    tw, th_table = 0.88, 0.30
    tx = (1 - tw) / 2
    ty_table = 0.52
    draw_rounded_rect(ax, tx, ty_table, tw, th_table, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)

    ax.text(tx + 0.03, ty_table + th_table - 0.03, 'Model Comparison',
            transform=ax.transAxes, fontsize=10, color=TEXT_WHITE,
            va='center', ha='left', fontweight='bold', fontfamily='sans-serif')

    headers = ['Model', 'R\u00b2 Score', 'MAE ($)', 'RMSE ($)', 'Status']
    col_widths = [0.22, 0.14, 0.16, 0.16, 0.14]
    col_x = [tx + 0.03]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    header_y = ty_table + th_table - 0.075
    draw_rounded_rect(ax, tx + 0.01, header_y - 0.012, tw - 0.02, 0.035,
                      BG_NAVBAR, radius=0.004)
    for j, hdr in enumerate(headers):
        ax.text(col_x[j] + col_widths[j] / 2, header_y, hdr,
                transform=ax.transAxes, fontsize=7.5, color=TEXT_WHITE,
                va='center', ha='center', fontweight='bold', fontfamily='sans-serif')

    models = [
        ('Gradient Boosting',  '0.8420', '35,240', '48,120', True),
        ('Random Forest',      '0.8150', '37,680', '52,340', False),
        ('XGBoost',            '0.8380', '35,890', '49,010', False),
        ('Linear Regression',  '0.6340', '52,100', '71,450', False),
        ('Decision Tree',      '0.7220', '45,670', '62,890', False),
    ]

    row_h = 0.042
    for i, (name, r2, mae, rmse, best) in enumerate(models):
        ry = header_y - 0.048 - i * row_h
        bg = '#0b2e1a' if best else (BG_TABLE_ROW if i % 2 == 0 else BG_TABLE_ALT)
        ec = ACCENT_GREEN if best else bg
        draw_rounded_rect(ax, tx + 0.01, ry - 0.01, tw - 0.02, row_h - 0.004,
                          bg, radius=0.004, edgecolor=ec, linewidth=1 if best else 0)

        vals = [name, r2, mae, rmse]
        for j, val in enumerate(vals):
            c = ACCENT_GREEN if best and j == 0 else TEXT_LIGHT
            fw = 'bold' if best else 'normal'
            ax.text(col_x[j] + col_widths[j] / 2, ry + 0.007, val,
                    transform=ax.transAxes, fontsize=7, color=c,
                    va='center', ha='center', fontweight=fw, fontfamily='sans-serif')

        # Status badge
        badge_text = 'Best' if best else 'Active'
        badge_color = ACCENT_GREEN if best else '#6c757d'
        badge_x = col_x[4] + col_widths[4] / 2
        draw_rounded_rect(ax, badge_x - 0.03, ry + 0.001, 0.06, 0.018,
                          badge_color, radius=0.004, alpha=0.8)
        ax.text(badge_x, ry + 0.01, badge_text, transform=ax.transAxes,
                fontsize=6, color=TEXT_WHITE, va='center', ha='center',
                fontweight='bold', fontfamily='sans-serif')

    # Bar chart - R2 comparison
    chart_w, chart_h_bar = 0.88, 0.32
    cx_chart = (1 - chart_w) / 2
    cy_chart = 0.10
    draw_rounded_rect(ax, cx_chart, cy_chart, chart_w, chart_h_bar, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    ax.text(cx_chart + 0.03, cy_chart + chart_h_bar - 0.03, 'R\u00b2 Score Comparison',
            transform=ax.transAxes, fontsize=10, color=TEXT_WHITE,
            va='center', ha='left', fontweight='bold', fontfamily='sans-serif')

    model_names = ['Gradient\nBoosting', 'Random\nForest', 'XGBoost',
                   'Linear\nRegression', 'Decision\nTree']
    r2_vals = [0.842, 0.815, 0.838, 0.634, 0.722]
    bar_colors = [ACCENT_GREEN, ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE]

    n_bars = len(model_names)
    bar_area_x = cx_chart + 0.08
    bar_area_w = chart_w - 0.14
    bar_area_y = cy_chart + 0.05
    bar_area_h = chart_h_bar - 0.12
    bar_w_each = bar_area_w / (n_bars * 1.6)

    for i in range(n_bars):
        bx = bar_area_x + i * (bar_area_w / n_bars) + bar_area_w / n_bars * 0.15
        bh = r2_vals[i] * bar_area_h
        draw_rounded_rect(ax, bx, bar_area_y, bar_w_each, bh,
                          bar_colors[i], radius=0.005, alpha=0.85)
        ax.text(bx + bar_w_each / 2, bar_area_y + bh + 0.01, f'{r2_vals[i]:.3f}',
                transform=ax.transAxes, fontsize=6.5, color=TEXT_WHITE,
                va='bottom', ha='center', fontweight='bold', fontfamily='sans-serif')
        ax.text(bx + bar_w_each / 2, bar_area_y - 0.02, model_names[i],
                transform=ax.transAxes, fontsize=5.5, color=TEXT_MUTED,
                va='top', ha='center', fontfamily='sans-serif')

    # Y-axis labels
    for tick in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        yy = bar_area_y + tick * bar_area_h
        ax.text(bar_area_x - 0.015, yy, f'{tick:.1f}', transform=ax.transAxes,
                fontsize=5.5, color=TEXT_MUTED, va='center', ha='right',
                fontfamily='sans-serif')
        ax.plot([bar_area_x - 0.005, bar_area_x + bar_area_w], [yy, yy],
                color=BORDER_COLOR, linewidth=0.3, transform=ax.transAxes, alpha=0.5)

    save_figure(fig, 'fig_7_8_dashboard.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 9. ABOUT PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def gen_about():
    fig, ax = new_figure()
    draw_navbar(ax, active='About')

    ax.text(0.5, 0.87, 'About This Project', transform=ax.transAxes,
            fontsize=16, color=TEXT_WHITE, va='center', ha='center',
            fontweight='bold', fontfamily='sans-serif')

    # Project description card
    cw, ch_card = 0.88, 0.22
    cx_card = (1 - cw) / 2
    cy1 = 0.60
    draw_rounded_rect(ax, cx_card, cy1, cw, ch_card, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    draw_rounded_rect(ax, cx_card, cy1 + ch_card - 0.012, cw, 0.012, ACCENT_BLUE, radius=0.005)
    ax.text(cx_card + 0.04, cy1 + ch_card - 0.045, 'Project Description',
            transform=ax.transAxes, fontsize=11, color=TEXT_WHITE,
            va='center', ha='left', fontweight='bold', fontfamily='sans-serif')
    desc_lines = [
        'This application predicts California house prices using advanced Machine Learning algorithms.',
        'Built on the California Housing dataset, it provides accurate price estimations based on',
        'geographical location, demographics, and property features. Users can make predictions,',
        'view historical data, and explore insightful visualizations of the housing market.'
    ]
    for i, line in enumerate(desc_lines):
        ax.text(cx_card + 0.04, cy1 + ch_card - 0.09 - i * 0.035, line,
                transform=ax.transAxes, fontsize=7.5, color=TEXT_LIGHT,
                va='center', ha='left', fontfamily='sans-serif')

    # Tech stack card
    cy2 = 0.34
    ch2 = 0.22
    draw_rounded_rect(ax, cx_card, cy2, cw, ch2, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    draw_rounded_rect(ax, cx_card, cy2 + ch2 - 0.012, cw, 0.012, ACCENT_GREEN, radius=0.005)
    ax.text(cx_card + 0.04, cy2 + ch2 - 0.045, 'Technology Stack',
            transform=ax.transAxes, fontsize=11, color=TEXT_WHITE,
            va='center', ha='left', fontweight='bold', fontfamily='sans-serif')

    techs = [
        ('Backend:', 'Python, Flask, SQLAlchemy'),
        ('Frontend:', 'HTML5, Bootstrap 5, JavaScript'),
        ('ML Models:', 'Scikit-Learn, XGBoost, Gradient Boosting'),
        ('Database:', 'SQLite'),
        ('Visualization:', 'Matplotlib, Seaborn, Plotly'),
    ]
    for i, (label, value) in enumerate(techs):
        yy = cy2 + ch2 - 0.09 - i * 0.03
        ax.text(cx_card + 0.04, yy, label, transform=ax.transAxes,
                fontsize=7.5, color=ACCENT_BLUE, va='center', ha='left',
                fontweight='bold', fontfamily='sans-serif')
        ax.text(cx_card + 0.16, yy, value, transform=ax.transAxes,
                fontsize=7.5, color=TEXT_LIGHT, va='center', ha='left',
                fontfamily='sans-serif')

    # Team info card
    cy3 = 0.08
    ch3 = 0.22
    draw_rounded_rect(ax, cx_card, cy3, cw, ch3, BG_CARD, radius=0.012,
                      edgecolor=BORDER_COLOR, linewidth=0.8)
    draw_rounded_rect(ax, cx_card, cy3 + ch3 - 0.012, cw, 0.012, ACCENT_GOLD, radius=0.005)
    ax.text(cx_card + 0.04, cy3 + ch3 - 0.045, 'Team Information',
            transform=ax.transAxes, fontsize=11, color=TEXT_WHITE,
            va='center', ha='left', fontweight='bold', fontfamily='sans-serif')

    team = [
        ('Department:', 'Computer Science & Engineering'),
        ('Institution:', 'Vignana Bharathi Institute of Technology (VBIT)'),
        ('Project Type:', 'Major Project - B.Tech IV Year'),
        ('Guided By:', 'Department Faculty'),
    ]
    for i, (label, value) in enumerate(team):
        yy = cy3 + ch3 - 0.09 - i * 0.035
        ax.text(cx_card + 0.04, yy, label, transform=ax.transAxes,
                fontsize=7.5, color=ACCENT_GOLD, va='center', ha='left',
                fontweight='bold', fontfamily='sans-serif')
        ax.text(cx_card + 0.18, yy, value, transform=ax.transAxes,
                fontsize=7.5, color=TEXT_LIGHT, va='center', ha='left',
                fontfamily='sans-serif')

    save_figure(fig, 'fig_7_9_about.png')


# ═══════════════════════════════════════════════════════════════════════════════
# 10. FEATURE IMPORTANCE CHART
# ═══════════════════════════════════════════════════════════════════════════════
def gen_feature_importance():
    fig, ax = new_figure((10, 7))
    ax.set_facecolor(BG_DARK)

    # Title
    ax.text(0.5, 0.95, 'Feature Importance - Gradient Boosting Model',
            transform=ax.transAxes, fontsize=16, color=TEXT_WHITE,
            va='center', ha='center', fontweight='bold', fontfamily='sans-serif')
    ax.text(0.5, 0.91, 'Relative contribution of each feature to the house price prediction',
            transform=ax.transAxes, fontsize=8, color=TEXT_MUTED,
            va='center', ha='center', fontfamily='sans-serif')

    features = [
        ('median_income', 0.52),
        ('ocean_proximity', 0.18),
        ('longitude', 0.08),
        ('latitude', 0.07),
        ('housing_median_age', 0.05),
        ('total_rooms', 0.035),
        ('population', 0.025),
        ('households', 0.02),
        ('total_bedrooms', 0.015),
    ]

    # Reverse for bottom-to-top display
    features_rev = list(reversed(features))

    n = len(features_rev)
    chart_left = 0.22
    chart_right = 0.92
    chart_bottom = 0.12
    chart_top = 0.85
    bar_area_w = chart_right - chart_left
    bar_area_h = chart_top - chart_bottom
    bar_h = bar_area_h / (n * 1.3)
    bar_gap = bar_area_h / n

    max_val = max(v for _, v in features_rev)

    # Grid lines
    for tick in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
        gx = chart_left + (tick / max_val) * bar_area_w * 0.9
        ax.plot([gx, gx], [chart_bottom, chart_top], color=BORDER_COLOR,
                linewidth=0.4, transform=ax.transAxes, alpha=0.5)
        ax.text(gx, chart_bottom - 0.025, f'{tick:.1f}', transform=ax.transAxes,
                fontsize=7, color=TEXT_MUTED, va='center', ha='center',
                fontfamily='sans-serif')

    ax.text(0.5 * (chart_left + chart_right), chart_bottom - 0.06,
            'Importance Score', transform=ax.transAxes,
            fontsize=9, color=TEXT_LIGHT, va='center', ha='center',
            fontfamily='sans-serif')

    # Color gradient for bars
    colors_list = plt.cm.viridis(np.linspace(0.25, 0.95, n))

    for i, (feat, val) in enumerate(features_rev):
        by = chart_bottom + i * bar_gap + (bar_gap - bar_h) / 2
        bw = (val / max_val) * bar_area_w * 0.9

        # Bar
        color = colors_list[i]
        draw_rounded_rect(ax, chart_left, by, bw, bar_h, color,
                          radius=0.005, alpha=0.9)

        # Feature label
        ax.text(chart_left - 0.015, by + bar_h / 2, feat,
                transform=ax.transAxes, fontsize=8, color=TEXT_LIGHT,
                va='center', ha='right', fontfamily='monospace')

        # Value label
        ax.text(chart_left + bw + 0.012, by + bar_h / 2, f'{val:.3f}',
                transform=ax.transAxes, fontsize=7.5, color=TEXT_WHITE,
                va='center', ha='left', fontweight='bold', fontfamily='sans-serif')

    # Border box around chart area
    border = FancyBboxPatch(
        (chart_left - 0.005, chart_bottom - 0.005),
        bar_area_w + 0.01, bar_area_h + 0.01,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor='none', edgecolor=BORDER_COLOR, linewidth=0.8,
        transform=ax.transAxes
    )
    ax.add_patch(border)

    # Note
    ax.text(0.5, 0.04,
            'Note: median_income is the strongest predictor of house prices in California.',
            transform=ax.transAxes, fontsize=7.5, color=TEXT_MUTED,
            va='center', ha='center', fontstyle='italic', fontfamily='sans-serif')

    save_figure(fig, 'fig_7_10_feature_importance.png')


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  Generating Application Screenshot Mockups")
    print("  House Price Prediction - C4 Project")
    print("=" * 60)
    print()

    generators = [
        ("Fig 7.1  - Login Page",              gen_login),
        ("Fig 7.2  - Register Page",           gen_register),
        ("Fig 7.3  - Home / Dashboard",        gen_home),
        ("Fig 7.4  - Prediction Form",         gen_predict),
        ("Fig 7.5  - Prediction Result",       gen_result),
        ("Fig 7.6  - Prediction History",      gen_history),
        ("Fig 7.7  - EDA Visualize Page",      gen_visualize),
        ("Fig 7.8  - Model Dashboard",         gen_dashboard),
        ("Fig 7.9  - About Page",              gen_about),
        ("Fig 7.10 - Feature Importance",      gen_feature_importance),
    ]

    for i, (label, func) in enumerate(generators, 1):
        print(f"[{i:2d}/10] {label}")
        func()

    print()
    print("=" * 60)
    print(f"  All 10 screenshots saved to:")
    print(f"  {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
