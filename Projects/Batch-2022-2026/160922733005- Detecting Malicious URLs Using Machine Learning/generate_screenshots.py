#!/usr/bin/env python3
"""
generate_screenshots.py
Generates 14 Ch7 screenshot mockup PNG images for the C12
"URLShield - Detecting Malicious URLs Using Machine Learning" project report.

Usage:
    python generate_screenshots.py

All images are saved into a figures/ subdirectory at 150 DPI.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── Theme colours ────────────────────────────────────────────────────────────
DARK_BG    = "#0f0f1a"
DARK_CARD  = "#1a1a2e"
ACCENT     = "#ffc107"
TEXT_WHITE  = "#ffffff"
TEXT_MUTED  = "#a0aec0"
GREEN      = "#2ecc71"
RED        = "#e74c3c"
FIELD_BG   = "#374151"
NAVBAR_BG  = "#16213e"
BORDER     = "#2d2d44"

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 150

# ── Helper utilities ─────────────────────────────────────────────────────────

def _new_fig(w=12, h=7):
    """Return (fig, ax) with dark background and no ticks."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def draw_box(ax, x, y, w, h, color=DARK_CARD, radius=0.015, linewidth=0,
             edgecolor=None, alpha=1.0):
    """Draw a rounded rectangle (FancyBboxPatch) and return it."""
    ec = edgecolor if edgecolor else color
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor=ec,
        linewidth=linewidth, alpha=alpha,
        transform=ax.transAxes, clip_on=False,
    )
    ax.add_patch(box)
    return box


def draw_navbar(ax, auth=True, active=None):
    """Draw the top navbar bar."""
    draw_box(ax, 0, 0.92, 1, 0.08, color=NAVBAR_BG, radius=0.005)
    ax.text(0.03, 0.96, "URLShield", fontsize=14, fontweight="bold",
            color=ACCENT, transform=ax.transAxes, va="center")
    ax.text(0.03, 0.935, "Port 5004", fontsize=6, color=TEXT_MUTED,
            transform=ax.transAxes, va="center")

    if auth:
        links = ["Home", "Predict", "History", "Visualize", "Dashboard", "About", "Logout"]
    else:
        links = ["Home", "About", "Login", "Register"]

    x_start = 0.55 if auth else 0.70
    spacing = 0.065
    for i, lnk in enumerate(links):
        c = ACCENT if lnk == active else TEXT_WHITE
        fw = "bold" if lnk == active else "normal"
        ax.text(x_start + i * spacing, 0.96, lnk, fontsize=7,
                color=c, fontweight=fw,
                transform=ax.transAxes, va="center", ha="center")


def draw_field(ax, x, y, w, h, label="", placeholder="", label_offset=0.025):
    """Draw a labelled dark input field."""
    if label:
        ax.text(x, y + h + label_offset, label, fontsize=8, color=TEXT_WHITE,
                transform=ax.transAxes, va="bottom")
    draw_box(ax, x, y, w, h, color=FIELD_BG, radius=0.008,
             linewidth=0.6, edgecolor=BORDER)
    if placeholder:
        ax.text(x + 0.01, y + h / 2, placeholder, fontsize=7,
                color=TEXT_MUTED, transform=ax.transAxes, va="center")


def draw_button(ax, x, y, w, h, text, color=ACCENT, text_color="#000000",
                fontsize=9, radius=0.008):
    """Draw a coloured button with centred text."""
    draw_box(ax, x, y, w, h, color=color, radius=radius)
    ax.text(x + w / 2, y + h / 2, text, fontsize=fontsize,
            color=text_color, fontweight="bold",
            transform=ax.transAxes, ha="center", va="center")


def draw_badge(ax, x, y, text, color, fontsize=7, w=0.07, h=0.022):
    """Small rounded badge."""
    draw_box(ax, x - w / 2, y - h / 2, w, h, color=color, radius=0.006)
    ax.text(x, y, text, fontsize=fontsize, color=TEXT_WHITE,
            fontweight="bold", transform=ax.transAxes, ha="center", va="center")


def draw_stat_card(ax, x, y, w, h, number, label, color):
    """Stat card with large number and label."""
    draw_box(ax, x, y, w, h, color=DARK_CARD, radius=0.012,
             linewidth=1.2, edgecolor=color)
    ax.text(x + w / 2, y + h * 0.62, str(number), fontsize=22,
            color=color, fontweight="bold",
            transform=ax.transAxes, ha="center", va="center")
    ax.text(x + w / 2, y + h * 0.25, label, fontsize=8,
            color=TEXT_MUTED, transform=ax.transAxes, ha="center", va="center")


def _save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor(),
                bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {name}")


# ═════════════════════════════════════════════════════════════════════════════
# 1. Login page
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_1_login():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=False, active="Login")

    # Centred card
    cw, ch = 0.35, 0.55
    cx, cy = 0.5 - cw / 2, 0.15
    draw_box(ax, cx, cy, cw, ch, color=DARK_CARD, radius=0.015,
             linewidth=0.8, edgecolor=BORDER)

    ax.text(0.5, cy + ch - 0.06, "Welcome Back", fontsize=16,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center")
    ax.text(0.5, cy + ch - 0.11, "Sign in to your URLShield account",
            fontsize=8, color=TEXT_MUTED,
            transform=ax.transAxes, ha="center", va="center")

    fw = cw - 0.08
    fx = cx + 0.04
    draw_field(ax, fx, cy + 0.30, fw, 0.05, label="Username",
               placeholder="Enter username")
    draw_field(ax, fx, cy + 0.16, fw, 0.05, label="Password",
               placeholder="Enter password")

    draw_button(ax, fx, cy + 0.06, fw, 0.05, "Login")

    ax.text(0.5, cy + 0.02, "Don't have an account?  Register",
            fontsize=7, color=ACCENT,
            transform=ax.transAxes, ha="center", va="center")

    _save(fig, "fig_7_1_login.png")


# ═════════════════════════════════════════════════════════════════════════════
# 2. Register page
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_2_register():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=False, active="Register")

    cw, ch = 0.35, 0.62
    cx, cy = 0.5 - cw / 2, 0.12
    draw_box(ax, cx, cy, cw, ch, color=DARK_CARD, radius=0.015,
             linewidth=0.8, edgecolor=BORDER)

    ax.text(0.5, cy + ch - 0.06, "Create Account", fontsize=16,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center")

    fw = cw - 0.08
    fx = cx + 0.04
    draw_field(ax, fx, cy + 0.40, fw, 0.05, label="Full Name",
               placeholder="Enter your name")
    draw_field(ax, fx, cy + 0.27, fw, 0.05, label="Username",
               placeholder="Choose a username")
    draw_field(ax, fx, cy + 0.14, fw, 0.05, label="Password",
               placeholder="Create a password")

    draw_button(ax, fx, cy + 0.05, fw, 0.05, "Register")

    ax.text(0.5, cy + 0.015, "Already have an account?  Login",
            fontsize=7, color=ACCENT,
            transform=ax.transAxes, ha="center", va="center")

    _save(fig, "fig_7_2_register.png")


# ═════════════════════════════════════════════════════════════════════════════
# 3. Home Dashboard
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_3_home():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Home")

    ax.text(0.04, 0.88, "Dashboard Overview", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    # 3 stat cards
    card_w, card_h = 0.28, 0.14
    gap = 0.035
    sx = 0.04
    sy = 0.70
    draw_stat_card(ax, sx, sy, card_w, card_h, 15, "Your Scans", ACCENT)
    draw_stat_card(ax, sx + card_w + gap, sy, card_w, card_h, 5, "Malicious", RED)
    draw_stat_card(ax, sx + 2 * (card_w + gap), sy, card_w, card_h, 10, "Safe", GREEN)

    # Recent Scans table
    ax.text(0.04, 0.64, "Recent Scans", fontsize=11,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    tw = 0.92
    tx = 0.04
    draw_box(ax, tx, 0.05, tw, 0.56, color=DARK_CARD, radius=0.01,
             linewidth=0.6, edgecolor=BORDER)

    headers = ["#", "URL", "Result", "Confidence", "Date"]
    hx = [0.06, 0.14, 0.58, 0.72, 0.86]
    hy = 0.575
    for i, h in enumerate(headers):
        ax.text(hx[i], hy, h, fontsize=8, fontweight="bold",
                color=ACCENT, transform=ax.transAxes, va="center")
    # separator line
    ax.plot([tx + 0.005, tx + tw - 0.005], [hy - 0.018, hy - 0.018],
            color=BORDER, linewidth=0.5, transform=ax.transAxes)

    rows = [
        ("1", "https://google.com/search?q=ml",       "Legitimate", "96.1%", "2025-03-01"),
        ("2", "http://192.168.1.1/verify-account",     "Malicious",  "88.5%", "2025-03-01"),
        ("3", "https://github.com/user/repo",          "Legitimate", "97.3%", "2025-02-28"),
        ("4", "http://free-prize.xyz/claim-now",       "Malicious",  "91.7%", "2025-02-28"),
        ("5", "https://stackoverflow.com/questions",   "Legitimate", "94.8%", "2025-02-27"),
    ]

    for ri, row in enumerate(rows):
        ry = 0.52 - ri * 0.085
        for ci, val in enumerate(row):
            if ci == 2:  # Result badge
                bc = GREEN if val == "Legitimate" else RED
                draw_badge(ax, hx[ci] + 0.03, ry, val, bc, fontsize=6,
                           w=0.08, h=0.025)
            else:
                txt = val
                if ci == 1 and len(val) > 35:
                    txt = val[:35] + "..."
                ax.text(hx[ci], ry, txt, fontsize=7, color=TEXT_WHITE,
                        transform=ax.transAxes, va="center")

    _save(fig, "fig_7_3_home.png")


# ═════════════════════════════════════════════════════════════════════════════
# 4. Predict (URL Detection) page
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_4_predict():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Predict")

    ax.text(0.04, 0.88, "URL Malicious Detection", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)
    ax.text(0.04, 0.845, "Enter a URL to check if it is malicious or legitimate",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)

    # Left panel - input
    lw, lh = 0.44, 0.70
    lx, ly = 0.04, 0.08
    draw_box(ax, lx, ly, lw, lh, color=DARK_CARD, radius=0.012,
             linewidth=0.6, edgecolor=BORDER)
    ax.text(lx + 0.03, ly + lh - 0.05, "Enter URL", fontsize=10,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    draw_field(ax, lx + 0.03, ly + lh - 0.19, lw - 0.06, 0.06,
               label="URL to Check", placeholder="https://example.com")

    draw_button(ax, lx + 0.03, ly + lh - 0.30, lw - 0.06, 0.055,
                "Check URL", color=ACCENT, text_color="#000000")

    # Right panel - placeholder
    rw, rh = 0.44, 0.70
    rx, ry = 0.52, 0.08
    draw_box(ax, rx, ry, rw, rh, color=DARK_CARD, radius=0.012,
             linewidth=0.6, edgecolor=BORDER)
    ax.text(rx + rw / 2, ry + rh / 2 + 0.03, "Results will appear here",
            fontsize=10, color=TEXT_MUTED,
            transform=ax.transAxes, ha="center", va="center")
    ax.text(rx + rw / 2, ry + rh / 2 - 0.03,
            "Submit a URL to see the analysis",
            fontsize=8, color=TEXT_MUTED,
            transform=ax.transAxes, ha="center", va="center", alpha=0.6)

    _save(fig, "fig_7_4_predict.png")


# ═════════════════════════════════════════════════════════════════════════════
# 5. Result – Legitimate
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_5_result_legit():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Predict")

    ax.text(0.04, 0.88, "URL Analysis Result", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    # Green result card
    cw, ch = 0.60, 0.62
    cx, cy = 0.20, 0.10
    draw_box(ax, cx, cy, cw, ch, color=DARK_CARD, radius=0.015,
             linewidth=2, edgecolor=GREEN)

    # Top green banner
    draw_box(ax, cx, cy + ch - 0.12, cw, 0.12, color=GREEN, radius=0.012)
    ax.text(cx + cw / 2, cy + ch - 0.06, "\u2713  Legitimate URL",
            fontsize=16, fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center")

    # Confidence
    ax.text(cx + cw / 2, cy + ch - 0.19, "Confidence: 94.2%",
            fontsize=13, fontweight="bold", color=GREEN,
            transform=ax.transAxes, ha="center", va="center")

    # URL
    ax.text(cx + 0.04, cy + ch - 0.28, "Scanned URL:",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)
    draw_box(ax, cx + 0.04, cy + ch - 0.36, cw - 0.08, 0.05,
             color=FIELD_BG, radius=0.006)
    ax.text(cx + 0.06, cy + ch - 0.335, "https://www.google.com/search?q=machine+learning",
            fontsize=7, color=TEXT_WHITE, transform=ax.transAxes, va="center")

    # Key features
    ax.text(cx + 0.04, cy + ch - 0.42, "Key Features:",
            fontsize=9, fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes)
    features = [
        "\u2713  Uses HTTPS protocol",
        "\u2713  Known domain (google.com)",
        "\u2713  Normal URL length (49 chars)",
        "\u2713  No suspicious words detected",
        "\u2713  No IP address in URL",
    ]
    for i, f in enumerate(features):
        ax.text(cx + 0.06, cy + ch - 0.48 - i * 0.04, f,
                fontsize=7, color=GREEN, transform=ax.transAxes)

    _save(fig, "fig_7_5_result_legit.png")


# ═════════════════════════════════════════════════════════════════════════════
# 6. Result – Malicious
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_6_result_malicious():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Predict")

    ax.text(0.04, 0.88, "URL Analysis Result", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    cw, ch = 0.60, 0.62
    cx, cy = 0.20, 0.10
    draw_box(ax, cx, cy, cw, ch, color=DARK_CARD, radius=0.015,
             linewidth=2, edgecolor=RED)

    # Top red banner
    draw_box(ax, cx, cy + ch - 0.12, cw, 0.12, color=RED, radius=0.012)
    ax.text(cx + cw / 2, cy + ch - 0.06,
            "\u26A0  WARNING: Malicious URL Detected!",
            fontsize=14, fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center")

    ax.text(cx + cw / 2, cy + ch - 0.19, "Confidence: 88.5%",
            fontsize=13, fontweight="bold", color=RED,
            transform=ax.transAxes, ha="center", va="center")

    ax.text(cx + 0.04, cy + ch - 0.28, "Scanned URL:",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)
    draw_box(ax, cx + 0.04, cy + ch - 0.36, cw - 0.08, 0.05,
             color=FIELD_BG, radius=0.006)
    ax.text(cx + 0.06, cy + ch - 0.335,
            "http://192.168.1.1/verify-account",
            fontsize=7, color=RED, transform=ax.transAxes, va="center")

    ax.text(cx + 0.04, cy + ch - 0.42, "Suspicious Features:",
            fontsize=9, fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes)
    features = [
        "\u2717  Uses HTTP (not HTTPS)",
        "\u2717  IP address used instead of domain",
        "\u2717  Contains suspicious word: 'verify'",
        "\u2717  No recognizable TLD",
        "\u2717  Suspicious path structure",
    ]
    for i, f in enumerate(features):
        ax.text(cx + 0.06, cy + ch - 0.48 - i * 0.04, f,
                fontsize=7, color=RED, transform=ax.transAxes)

    _save(fig, "fig_7_6_result_malicious.png")


# ═════════════════════════════════════════════════════════════════════════════
# 7. History page
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_7_history():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="History")

    ax.text(0.04, 0.88, "Scan History", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)
    ax.text(0.04, 0.845, "Your previous URL scans",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)

    tw = 0.92
    tx = 0.04
    draw_box(ax, tx, 0.05, tw, 0.76, color=DARK_CARD, radius=0.01,
             linewidth=0.6, edgecolor=BORDER)

    headers = ["#", "URL", "Result", "Confidence", "Date"]
    hx_pos = [0.06, 0.12, 0.56, 0.70, 0.84]
    hy = 0.76
    for i, h in enumerate(headers):
        ax.text(hx_pos[i], hy, h, fontsize=8, fontweight="bold",
                color=ACCENT, transform=ax.transAxes, va="center")
    ax.plot([tx + 0.005, tx + tw - 0.005], [hy - 0.02, hy - 0.02],
            color=BORDER, linewidth=0.5, transform=ax.transAxes)

    rows = [
        ("1", "https://google.com/search?q=ml",          "Legitimate", "96.1%", "2025-03-01"),
        ("2", "http://192.168.1.1/verify-account",        "Malicious",  "88.5%", "2025-03-01"),
        ("3", "https://github.com/user/repo",             "Legitimate", "97.3%", "2025-02-28"),
        ("4", "http://free-prize.xyz/claim-now",          "Malicious",  "91.7%", "2025-02-28"),
        ("5", "https://stackoverflow.com/questions/ml",   "Legitimate", "94.8%", "2025-02-27"),
        ("6", "http://login-secure.xyz/bank/verify",      "Malicious",  "93.2%", "2025-02-26"),
    ]

    for ri, row in enumerate(rows):
        ry = 0.68 - ri * 0.095
        for ci, val in enumerate(row):
            if ci == 2:
                bc = GREEN if val == "Legitimate" else RED
                draw_badge(ax, hx_pos[ci] + 0.04, ry, val, bc, fontsize=6,
                           w=0.08, h=0.025)
            else:
                txt = val
                if ci == 1 and len(val) > 38:
                    txt = val[:38] + "..."
                ax.text(hx_pos[ci], ry, txt, fontsize=7, color=TEXT_WHITE,
                        transform=ax.transAxes, va="center")

    _save(fig, "fig_7_7_history.png")


# ═════════════════════════════════════════════════════════════════════════════
# 8. Visualize (EDA gallery)
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_8_visualize():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Visualize")

    ax.text(0.04, 0.88, "Exploratory Data Analysis", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)
    ax.text(0.04, 0.845, "Visual insights from the URL dataset",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)

    labels = [
        "Label Distribution", "URL Length Distribution",
        "HTTPS Distribution", "Suspicious Words Count",
        "Correlation Heatmap", "Feature Importance",
    ]
    cols, rows_n = 3, 2
    cw, ch = 0.27, 0.32
    gx, gy = 0.04, 0.08
    hgap = 0.035
    vgap = 0.06

    for idx, lbl in enumerate(labels):
        r = idx // cols
        c = idx % cols
        bx = gx + c * (cw + hgap)
        by = gy + (rows_n - 1 - r) * (ch + vgap)

        draw_box(ax, bx, by, cw, ch, color=DARK_CARD, radius=0.01,
                 linewidth=0.6, edgecolor=BORDER)

        # Placeholder chart icon (simple bar sketches)
        bar_colors = [ACCENT, GREEN, RED, "#8b5cf6"]
        nbar = 4
        bar_w = cw * 0.12
        bar_gap = cw * 0.05
        bar_start_x = bx + cw / 2 - (nbar * bar_w + (nbar - 1) * bar_gap) / 2
        for bi in range(nbar):
            bh = ch * (0.15 + 0.25 * np.random.random())
            draw_box(ax, bar_start_x + bi * (bar_w + bar_gap),
                     by + ch * 0.20, bar_w, bh,
                     color=bar_colors[bi % len(bar_colors)],
                     radius=0.004, alpha=0.5)

        ax.text(bx + cw / 2, by + 0.03, lbl, fontsize=7,
                fontweight="bold", color=TEXT_WHITE,
                transform=ax.transAxes, ha="center", va="center")

    _save(fig, "fig_7_8_visualize.png")


# ═════════════════════════════════════════════════════════════════════════════
# 9. Dashboard
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_9_dashboard():
    fig, ax = _new_fig(12, 8)
    draw_navbar(ax, auth=True, active="Dashboard")

    ax.text(0.04, 0.88, "Model Performance Dashboard", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    # Stat cards
    card_w, card_h = 0.20, 0.10
    gap = 0.035
    sx = 0.14
    sy = 0.77
    draw_stat_card(ax, sx, sy, card_w, card_h, "8,000", "Train Size", ACCENT)
    draw_stat_card(ax, sx + card_w + gap, sy, card_w, card_h, "2,000",
                   "Test Size", GREEN)
    draw_stat_card(ax, sx + 2 * (card_w + gap), sy, card_w, card_h, "28",
                   "Features", "#8b5cf6")

    # Model comparison table
    draw_box(ax, 0.04, 0.36, 0.92, 0.38, color=DARK_CARD, radius=0.01,
             linewidth=0.6, edgecolor=BORDER)
    ax.text(0.06, 0.71, "Model Comparison", fontsize=10,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)

    cols_hdr = ["#", "Model", "Accuracy", "Precision", "Recall", "F1 Score"]
    cx_pos = [0.06, 0.10, 0.45, 0.57, 0.69, 0.81]
    chy = 0.67
    for i, ch_text in enumerate(cols_hdr):
        ax.text(cx_pos[i], chy, ch_text, fontsize=7, fontweight="bold",
                color=ACCENT, transform=ax.transAxes, va="center")
    ax.plot([0.05, 0.95], [chy - 0.015, chy - 0.015],
            color=BORDER, linewidth=0.5, transform=ax.transAxes)

    models = [
        ("1", "Random Forest",       "96.2%", "95.8%", "96.5%", "96.1%"),
        ("2", "XGBoost",             "95.8%", "95.4%", "96.1%", "95.7%"),
        ("3", "Gradient Boosting",   "95.1%", "94.7%", "95.4%", "95.0%"),
        ("4", "Decision Tree",       "93.5%", "93.1%", "93.8%", "93.4%"),
        ("5", "SVM",                 "92.8%", "92.3%", "93.2%", "92.7%"),
        ("6", "KNN",                 "91.4%", "91.0%", "91.7%", "91.3%"),
        ("7", "Logistic Regression", "90.6%", "90.2%", "90.9%", "90.5%"),
        ("8", "Naive Bayes",         "87.3%", "86.9%", "87.6%", "87.2%"),
    ]
    for ri, row in enumerate(models):
        ry = 0.63 - ri * 0.034
        for ci, val in enumerate(row):
            c = TEXT_WHITE if ci <= 1 else GREEN
            ax.text(cx_pos[ci], ry, val, fontsize=6.5, color=c,
                    transform=ax.transAxes, va="center")

    # Bottom chart placeholders
    ph_w, ph_h = 0.43, 0.25
    py = 0.05
    for px, title in [(0.04, "Accuracy Comparison"),
                      (0.52, "F1 Score Comparison")]:
        draw_box(ax, px, py, ph_w, ph_h, color=DARK_CARD, radius=0.01,
                 linewidth=0.6, edgecolor=BORDER)
        ax.text(px + ph_w / 2, py + ph_h - 0.03, title,
                fontsize=8, fontweight="bold", color=TEXT_WHITE,
                transform=ax.transAxes, ha="center", va="center")
        # Mini bar chart
        nbar = 8
        bar_w = ph_w * 0.08
        bar_gap = ph_w * 0.035
        bar_sx = px + ph_w / 2 - (nbar * bar_w + (nbar - 1) * bar_gap) / 2
        for bi in range(nbar):
            bh = ph_h * (0.25 + 0.45 * (1 - bi * 0.08))
            draw_box(ax, bar_sx + bi * (bar_w + bar_gap),
                     py + 0.03, bar_w, bh,
                     color=ACCENT, radius=0.003, alpha=0.7 - bi * 0.04)

    _save(fig, "fig_7_9_dashboard.png")


# ═════════════════════════════════════════════════════════════════════════════
# 10. Feature Importance bar chart
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_10_feature_importance():
    features = [
        ("url_length",         0.15),
        ("n_suspicious_words", 0.12),
        ("n_dots",             0.10),
        ("special_ratio",      0.09),
        ("has_https",          0.08),
        ("domain_length",      0.07),
        ("n_digits",           0.06),
        ("path_length",        0.05),
        ("url_depth",          0.05),
        ("has_ip",             0.04),
    ]
    names = [f[0] for f in features][::-1]
    vals = [f[1] for f in features][::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    bars = ax.barh(range(len(names)), vals, color=ACCENT, height=0.6,
                   edgecolor=ACCENT, linewidth=0.5)

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9, color=TEXT_WHITE)
    ax.set_xlabel("Importance", fontsize=10, color=TEXT_WHITE)
    ax.set_title("Top 10 Feature Importances – Random Forest",
                 fontsize=13, fontweight="bold", color=TEXT_WHITE, pad=15)

    ax.tick_params(axis="x", colors=TEXT_MUTED, labelsize=8)
    ax.tick_params(axis="y", colors=TEXT_WHITE, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.xaxis.grid(True, color=BORDER, alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)

    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height() / 2,
                f"{v:.2f}", va="center", fontsize=8, color=ACCENT)

    fig.tight_layout()
    _save(fig, "fig_7_10_feature_importance.png")


# ═════════════════════════════════════════════════════════════════════════════
# 11. Confusion Matrix
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_11_confusion():
    cm = np.array([[929, 85],
                   [68,  918]])
    labels = ["Legitimate", "Malicious"]

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.set_title("Confusion Matrix – Random Forest",
                 fontsize=13, fontweight="bold", color=TEXT_WHITE, pad=15)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=10, color=TEXT_WHITE)
    ax.set_yticklabels(labels, fontsize=10, color=TEXT_WHITE)
    ax.set_xlabel("Predicted Label", fontsize=10, color=TEXT_WHITE, labelpad=10)
    ax.set_ylabel("True Label", fontsize=10, color=TEXT_WHITE, labelpad=10)

    ax.tick_params(axis="both", colors=TEXT_MUTED)

    # Text annotations
    thresh = cm.max() / 2.0
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center", fontsize=18, fontweight="bold",
                    color="white" if cm[i, j] > thresh else DARK_BG)

    for spine in ax.spines.values():
        spine.set_color(BORDER)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color=TEXT_MUTED)
    cbar.outline.set_edgecolor(BORDER)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_MUTED)

    fig.tight_layout()
    _save(fig, "fig_7_11_confusion.png")


# ═════════════════════════════════════════════════════════════════════════════
# 12. About page
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_12_about():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="About")

    # Title section
    ax.text(0.5, 0.85, "URLShield", fontsize=22,
            fontweight="bold", color=ACCENT,
            transform=ax.transAxes, ha="center")
    ax.text(0.5, 0.80,
            "Detecting Malicious URLs Using Machine Learning",
            fontsize=10, color=TEXT_MUTED,
            transform=ax.transAxes, ha="center")

    # Description card
    draw_box(ax, 0.08, 0.60, 0.84, 0.14, color=DARK_CARD, radius=0.01,
             linewidth=0.6, edgecolor=BORDER)
    desc = (
        "URLShield is an intelligent web application that uses machine learning\n"
        "to classify URLs as legitimate or malicious. It extracts 28 features from\n"
        "each URL and applies ensemble learning for high-accuracy detection."
    )
    ax.text(0.5, 0.67, desc, fontsize=8, color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center",
            linespacing=1.6)

    # How it works - 4 steps
    ax.text(0.5, 0.55, "How It Works", fontsize=12,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center")

    steps = ["Enter URL", "Extract 28\nFeatures", "ML\nClassification", "Get Result"]
    step_colors = [ACCENT, "#8b5cf6", "#3b82f6", GREEN]
    sw, sh = 0.16, 0.12
    total_w = 4 * sw + 3 * 0.06
    sx_start = 0.5 - total_w / 2
    sy = 0.37

    for i, (step, sc) in enumerate(zip(steps, step_colors)):
        sx = sx_start + i * (sw + 0.06)
        draw_box(ax, sx, sy, sw, sh, color=DARK_CARD, radius=0.01,
                 linewidth=1.2, edgecolor=sc)
        ax.text(sx + sw / 2, sy + sh * 0.65, f"Step {i + 1}",
                fontsize=6, color=sc, fontweight="bold",
                transform=ax.transAxes, ha="center", va="center")
        ax.text(sx + sw / 2, sy + sh * 0.30, step,
                fontsize=7, color=TEXT_WHITE,
                transform=ax.transAxes, ha="center", va="center",
                linespacing=1.3)

        # Arrow between steps
        if i < 3:
            arrow_x = sx + sw + 0.01
            ax.annotate("", xy=(arrow_x + 0.04, sy + sh / 2),
                        xytext=(arrow_x, sy + sh / 2),
                        xycoords="axes fraction",
                        arrowprops=dict(arrowstyle="->", color=TEXT_MUTED,
                                        lw=1.5),
                        transform=ax.transAxes)

    # Tech stack
    ax.text(0.5, 0.30, "Tech Stack", fontsize=12,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center")

    techs = [
        ("Python 3.10", ACCENT),
        ("Flask", GREEN),
        ("scikit-learn", "#3b82f6"),
        ("XGBoost", "#8b5cf6"),
        ("SQLite", RED),
        ("Chart.js", "#06b6d4"),
        ("Bootstrap 5", "#8b5cf6"),
    ]
    tw_total = len(techs) * 0.11 + (len(techs) - 1) * 0.015
    tx_start = 0.5 - tw_total / 2
    for i, (tech, tc) in enumerate(techs):
        tx = tx_start + i * (0.11 + 0.015)
        draw_box(ax, tx, 0.18, 0.11, 0.06, color=DARK_CARD, radius=0.008,
                 linewidth=1, edgecolor=tc)
        ax.text(tx + 0.055, 0.21, tech, fontsize=6, color=tc,
                fontweight="bold", transform=ax.transAxes,
                ha="center", va="center")

    ax.text(0.5, 0.10,
            "Developed as a Major Project  |  IV-C  |  2024-2025",
            fontsize=7, color=TEXT_MUTED,
            transform=ax.transAxes, ha="center")

    _save(fig, "fig_7_12_about.png")


# ═════════════════════════════════════════════════════════════════════════════
# 13. Admin view
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_13_admin():
    fig, ax = _new_fig()
    draw_navbar(ax, auth=True, active="Dashboard")

    ax.text(0.04, 0.88, "Admin Dashboard", fontsize=14,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)
    ax.text(0.04, 0.845, "Platform overview (admin only)",
            fontsize=8, color=TEXT_MUTED, transform=ax.transAxes)

    # Platform statistics heading
    ax.text(0.5, 0.78, "Platform Statistics", fontsize=13,
            fontweight="bold", color=ACCENT,
            transform=ax.transAxes, ha="center")

    # 3 large stat cards
    card_w, card_h = 0.26, 0.30
    gap = 0.04
    total_w = 3 * card_w + 2 * gap
    sx_start = 0.5 - total_w / 2
    sy = 0.38

    stats = [
        ("25", "Total Users", "#3b82f6"),
        ("342", "Total Scans", ACCENT),
        ("128", "Malicious Detected", RED),
    ]
    for i, (num, lbl, clr) in enumerate(stats):
        sx = sx_start + i * (card_w + gap)
        draw_box(ax, sx, sy, card_w, card_h, color=DARK_CARD, radius=0.015,
                 linewidth=1.5, edgecolor=clr)
        ax.text(sx + card_w / 2, sy + card_h * 0.65, num,
                fontsize=32, fontweight="bold", color=clr,
                transform=ax.transAxes, ha="center", va="center")
        ax.text(sx + card_w / 2, sy + card_h * 0.30, lbl,
                fontsize=9, color=TEXT_MUTED,
                transform=ax.transAxes, ha="center", va="center")

    # Extra info under malicious card
    mal_sx = sx_start + 2 * (card_w + gap)
    ax.text(mal_sx + card_w / 2, sy + card_h * 0.14, "37.4% of all scans",
            fontsize=7, color=RED, alpha=0.8,
            transform=ax.transAxes, ha="center", va="center")

    # Quick summary table below
    draw_box(ax, 0.15, 0.08, 0.70, 0.24, color=DARK_CARD, radius=0.01,
             linewidth=0.6, edgecolor=BORDER)
    ax.text(0.5, 0.28, "Quick Summary", fontsize=10,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center")

    summary = [
        ("Active Users (last 7d):", "18"),
        ("Scans Today:", "12"),
        ("Avg Confidence:", "93.4%"),
        ("Top Model:", "Random Forest (96.2%)"),
    ]
    for i, (k, v) in enumerate(summary):
        ry = 0.23 - i * 0.035
        ax.text(0.25, ry, k, fontsize=7, color=TEXT_MUTED,
                transform=ax.transAxes, va="center")
        ax.text(0.65, ry, v, fontsize=7, color=TEXT_WHITE,
                fontweight="bold", transform=ax.transAxes, va="center")

    _save(fig, "fig_7_13_admin.png")


# ═════════════════════════════════════════════════════════════════════════════
# 14. Mobile responsive view
# ═════════════════════════════════════════════════════════════════════════════

def fig_7_14_mobile():
    fig, ax = plt.subplots(figsize=(4, 8))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Phone frame border
    draw_box(ax, 0.02, 0.02, 0.96, 0.96, color=DARK_BG, radius=0.03,
             linewidth=2, edgecolor=TEXT_MUTED)

    # Status bar
    ax.text(0.5, 0.96, "9:41", fontsize=7, color=TEXT_WHITE,
            fontweight="bold", transform=ax.transAxes, ha="center")

    # Mini navbar
    draw_box(ax, 0.04, 0.90, 0.92, 0.05, color=NAVBAR_BG, radius=0.008)
    ax.text(0.12, 0.925, "URLShield", fontsize=9, fontweight="bold",
            color=ACCENT, transform=ax.transAxes, va="center")
    ax.text(0.85, 0.925, "\u2630", fontsize=11, color=TEXT_WHITE,
            transform=ax.transAxes, va="center", ha="center")

    # Title
    ax.text(0.5, 0.86, "Check URL", fontsize=12,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center")

    # URL input card
    draw_box(ax, 0.06, 0.70, 0.88, 0.13, color=DARK_CARD, radius=0.012,
             linewidth=0.6, edgecolor=BORDER)
    ax.text(0.12, 0.81, "URL to Check", fontsize=7, color=TEXT_WHITE,
            transform=ax.transAxes)
    draw_box(ax, 0.10, 0.74, 0.80, 0.05, color=FIELD_BG, radius=0.006)
    ax.text(0.14, 0.765, "https://example.com", fontsize=6,
            color=TEXT_MUTED, transform=ax.transAxes, va="center")

    # Check button
    draw_button(ax, 0.15, 0.63, 0.70, 0.05, "Check URL",
                fontsize=8, radius=0.008)

    # Result card (stacked below)
    draw_box(ax, 0.06, 0.12, 0.88, 0.46, color=DARK_CARD, radius=0.012,
             linewidth=1.5, edgecolor=GREEN)

    # Green banner
    draw_box(ax, 0.06, 0.50, 0.88, 0.08, color=GREEN, radius=0.010)
    ax.text(0.5, 0.54, "\u2713  Legitimate URL", fontsize=11,
            fontweight="bold", color=TEXT_WHITE,
            transform=ax.transAxes, ha="center", va="center")

    ax.text(0.5, 0.46, "Confidence: 94.2%", fontsize=10,
            fontweight="bold", color=GREEN,
            transform=ax.transAxes, ha="center", va="center")

    # URL
    ax.text(0.12, 0.41, "Scanned URL:", fontsize=6,
            color=TEXT_MUTED, transform=ax.transAxes)
    draw_box(ax, 0.10, 0.36, 0.80, 0.04, color=FIELD_BG, radius=0.005)
    ax.text(0.14, 0.38, "https://www.google.com/search",
            fontsize=5.5, color=TEXT_WHITE,
            transform=ax.transAxes, va="center")

    # Features
    ax.text(0.12, 0.33, "Key Features:", fontsize=7,
            fontweight="bold", color=TEXT_WHITE, transform=ax.transAxes)
    feats = [
        "\u2713  Uses HTTPS",
        "\u2713  Known domain",
        "\u2713  Normal URL length",
        "\u2713  No suspicious words",
    ]
    for i, f in enumerate(feats):
        ax.text(0.14, 0.29 - i * 0.035, f, fontsize=6,
                color=GREEN, transform=ax.transAxes)

    # Home indicator at bottom
    draw_box(ax, 0.35, 0.035, 0.30, 0.008, color=TEXT_MUTED, radius=0.004)

    _save(fig, "fig_7_14_mobile.png")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Saving screenshots to: {OUT_DIR}\n")

    generators = [
        ("Fig 7.1  Login Page",             fig_7_1_login),
        ("Fig 7.2  Register Page",           fig_7_2_register),
        ("Fig 7.3  Home Dashboard",          fig_7_3_home),
        ("Fig 7.4  Predict Page",            fig_7_4_predict),
        ("Fig 7.5  Result – Legitimate",     fig_7_5_result_legit),
        ("Fig 7.6  Result – Malicious",      fig_7_6_result_malicious),
        ("Fig 7.7  History Page",            fig_7_7_history),
        ("Fig 7.8  Visualize (EDA)",         fig_7_8_visualize),
        ("Fig 7.9  Model Dashboard",         fig_7_9_dashboard),
        ("Fig 7.10 Feature Importance",      fig_7_10_feature_importance),
        ("Fig 7.11 Confusion Matrix",        fig_7_11_confusion),
        ("Fig 7.12 About Page",              fig_7_12_about),
        ("Fig 7.13 Admin View",              fig_7_13_admin),
        ("Fig 7.14 Mobile Responsive",       fig_7_14_mobile),
    ]

    for label, fn in generators:
        print(f"Generating {label} ...")
        fn()

    print(f"\nDone. {len(generators)} screenshots saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()
