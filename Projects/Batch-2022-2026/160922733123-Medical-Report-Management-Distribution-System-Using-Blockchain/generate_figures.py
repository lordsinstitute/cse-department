"""
Generate all figures for the B6 Medical Report Management and Distribution
System Using Blockchain project report.

Produces 7 dark-theme matplotlib figures saved to ../figures/.
Run:  python generate_figures.py
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ── colour palette ──────────────────────────────────────────────────────────
DARK_BG   = "#1a1a2e"
ACCENT    = "#00b4d8"
LIGHT_TEXT = "#e0e0e0"
CARD_BG   = "#16213e"
SECONDARY = "#0f3460"
HIGHLIGHT = "#e94560"
SUCCESS   = "#2ecc71"
WARNING   = "#f39c12"

# ── output directory ────────────────────────────────────────────────────────
FIGURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"
)
os.makedirs(FIGURES_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
#  Helper utilities
# ═══════════════════════════════════════════════════════════════════════════

def _new_figure(width=12, height=7):
    """Return (fig, ax) with dark background and axis turned off."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, label, color=CARD_BG, edge=ACCENT,
         fontsize=10, text_color=LIGHT_TEXT, lw=1.5, style="round,pad=0.1"):
    """Draw a rounded rectangle with centred label."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=style,
        facecolor=color, edgecolor=edge, linewidth=lw,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2, label,
        ha="center", va="center", fontsize=fontsize,
        color=text_color, fontweight="bold", wrap=True,
    )
    return box


def _arrow(ax, x1, y1, x2, y2, color=ACCENT, style="->", lw=1.5,
           connectionstyle="arc3,rad=0.0"):
    """Draw an arrow between two points."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=style, color=color, lw=lw,
            connectionstyle=connectionstyle,
        ),
    )


def _arrow_label(ax, x1, y1, x2, y2, label="", color=ACCENT, lw=1.5,
                 connectionstyle="arc3,rad=0.0", fontsize=8):
    """Arrow with a text label at midpoint."""
    _arrow(ax, x1, y1, x2, y2, color=color, lw=lw,
           connectionstyle=connectionstyle)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if label:
        ax.text(mx, my + 0.03, label, ha="center", va="bottom",
                fontsize=fontsize, color=LIGHT_TEXT, style="italic")


def _save(fig, name):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  Saved  {path}")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 1.1 — System Architecture (3-tier)
# ═══════════════════════════════════════════════════════════════════════════

def fig_1_1_system_architecture():
    fig, ax = _new_figure(14, 8)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.98, "System Architecture — 3-Tier Design",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    # ── Tier labels ─────────────────────────────────────────────────────
    tier_labels = ["Client Tier", "Application Tier", "Data Tier"]
    tier_xs = [0.08, 0.38, 0.72]
    for lbl, tx in zip(tier_labels, tier_xs):
        ax.text(tx + 0.10, 0.90, lbl, ha="center", va="center",
                fontsize=13, color=WARNING, fontweight="bold")

    # ── Client tier ─────────────────────────────────────────────────────
    _box(ax, 0.02, 0.60, 0.18, 0.12, "Web Browser\n(HTML / CSS / JS)",
         color=SECONDARY, edge=ACCENT, fontsize=10)
    _box(ax, 0.02, 0.40, 0.18, 0.12, "Bootstrap 5\nDark Theme UI",
         color=SECONDARY, edge=ACCENT, fontsize=10)
    _box(ax, 0.02, 0.20, 0.18, 0.12, "Jinja2\nTemplates",
         color=SECONDARY, edge=ACCENT, fontsize=10)

    # ── Application tier ────────────────────────────────────────────────
    _box(ax, 0.30, 0.68, 0.20, 0.10, "Flask App\n(Routes / Views)",
         color=CARD_BG, edge=ACCENT, fontsize=10)
    _box(ax, 0.30, 0.52, 0.20, 0.10, "Auth Module\n(Login / RBAC)",
         color=CARD_BG, edge=ACCENT, fontsize=10)
    _box(ax, 0.30, 0.36, 0.20, 0.10, "Blockchain.py\n(SHA-256 Hashing)",
         color=CARD_BG, edge=HIGHLIGHT, fontsize=10)
    _box(ax, 0.30, 0.20, 0.20, 0.10, "File Handler\n(Upload / Storage)",
         color=CARD_BG, edge=ACCENT, fontsize=10)

    # ── Data tier ───────────────────────────────────────────────────────
    _box(ax, 0.62, 0.64, 0.20, 0.12, "SQLite DB\n(5 Tables)",
         color=SECONDARY, edge=SUCCESS, fontsize=10)
    _box(ax, 0.62, 0.44, 0.20, 0.12, "Blockchain\nLedger",
         color=SECONDARY, edge=HIGHLIGHT, fontsize=10)
    _box(ax, 0.62, 0.24, 0.20, 0.12, "File Storage\n(Encrypted Reports)",
         color=SECONDARY, edge=WARNING, fontsize=10)

    # ── Tier boundary lines ─────────────────────────────────────────────
    for bx in [0.26, 0.58]:
        ax.plot([bx, bx], [0.10, 0.88], ls="--", lw=1, color=LIGHT_TEXT,
                alpha=0.3)

    # ── Arrows client -> app ────────────────────────────────────────────
    _arrow(ax, 0.20, 0.66, 0.30, 0.73, color=ACCENT)
    _arrow(ax, 0.20, 0.46, 0.30, 0.57, color=ACCENT)
    _arrow(ax, 0.20, 0.26, 0.30, 0.25, color=ACCENT)

    # ── Arrows app -> data ──────────────────────────────────────────────
    _arrow(ax, 0.50, 0.73, 0.62, 0.70, color=SUCCESS)
    _arrow(ax, 0.50, 0.41, 0.62, 0.50, color=HIGHLIGHT)
    _arrow(ax, 0.50, 0.25, 0.62, 0.30, color=WARNING)

    # ── Legend ──────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(facecolor=SECONDARY, edgecolor=ACCENT, label="Client / Data"),
        mpatches.Patch(facecolor=CARD_BG, edgecolor=ACCENT, label="Application"),
        mpatches.Patch(facecolor=CARD_BG, edgecolor=HIGHLIGHT, label="Blockchain"),
    ]
    ax.legend(handles=legend_items, loc="lower center", ncol=3,
              fontsize=9, facecolor=DARK_BG, edgecolor=ACCENT,
              labelcolor=LIGHT_TEXT, framealpha=0.9)

    _save(fig, "fig_1_1_system_architecture.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3.1 — Use-Case Diagram
# ═══════════════════════════════════════════════════════════════════════════

def fig_3_1_use_case_diagram():
    fig, ax = _new_figure(14, 9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.98, "Use-Case Diagram",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    # ── System boundary ─────────────────────────────────────────────────
    boundary = FancyBboxPatch(
        (0.25, 0.05), 0.50, 0.85,
        boxstyle="round,pad=0.02",
        facecolor="none", edgecolor=ACCENT, linewidth=2, linestyle="--",
    )
    ax.add_patch(boundary)
    ax.text(0.50, 0.88, "Medical Report Management System",
            ha="center", va="center", fontsize=12, color=ACCENT,
            fontweight="bold")

    # ── Actors (stick figures as labelled ovals) ────────────────────────
    actors = {
        "Admin":   (0.08, 0.70),
        "Doctor":  (0.08, 0.40),
        "Patient": (0.92, 0.50),
    }
    for name, (ax_, ay) in actors.items():
        circle = plt.Circle((ax_, ay), 0.04, facecolor=SECONDARY,
                            edgecolor=HIGHLIGHT, lw=2)
        ax.add_patch(circle)
        ax.text(ax_, ay, name[0], ha="center", va="center",
                fontsize=14, color=LIGHT_TEXT, fontweight="bold")
        ax.text(ax_, ay - 0.07, name, ha="center", va="center",
                fontsize=10, color=LIGHT_TEXT, fontweight="bold")

    # ── Use cases (ellipses as rounded boxes) ───────────────────────────
    use_cases = [
        # (label, x, y)
        ("Audit System\nLogs",          0.38, 0.76),
        ("Verify Blockchain\nIntegrity", 0.58, 0.76),
        ("Manage Users",                 0.48, 0.64),
        ("Upload Medical\nReport",       0.38, 0.50),
        ("View Patient\nReports",        0.58, 0.50),
        ("View Own\nReports",            0.58, 0.36),
        ("Share / Revoke\nAccess",       0.48, 0.22),
        ("Login /\nAuthenticate",        0.48, 0.10),
    ]

    uc_positions = {}
    for label, ux, uy in use_cases:
        ellipse = mpatches.Ellipse(
            (ux, uy), 0.18, 0.09,
            facecolor=CARD_BG, edgecolor=ACCENT, lw=1.5,
        )
        ax.add_patch(ellipse)
        ax.text(ux, uy, label, ha="center", va="center",
                fontsize=8, color=LIGHT_TEXT, fontweight="bold")
        uc_positions[label.replace("\n", " ")] = (ux, uy)

    # ── Association lines ───────────────────────────────────────────────
    # Admin
    _arrow(ax, 0.12, 0.70, 0.29, 0.76, color=HIGHLIGHT, lw=1.2)
    _arrow(ax, 0.12, 0.70, 0.49, 0.76, color=HIGHLIGHT, lw=1.2)
    _arrow(ax, 0.12, 0.70, 0.39, 0.64, color=HIGHLIGHT, lw=1.2)
    _arrow(ax, 0.12, 0.70, 0.39, 0.10, color=HIGHLIGHT, lw=1.2,
           connectionstyle="arc3,rad=-0.3")

    # Doctor
    _arrow(ax, 0.12, 0.40, 0.29, 0.50, color=SUCCESS, lw=1.2)
    _arrow(ax, 0.12, 0.40, 0.49, 0.50, color=SUCCESS, lw=1.2)
    _arrow(ax, 0.12, 0.40, 0.39, 0.10, color=SUCCESS, lw=1.2,
           connectionstyle="arc3,rad=-0.2")

    # Patient
    _arrow(ax, 0.88, 0.50, 0.67, 0.36, color=WARNING, lw=1.2)
    _arrow(ax, 0.88, 0.50, 0.57, 0.22, color=WARNING, lw=1.2)
    _arrow(ax, 0.88, 0.50, 0.57, 0.10, color=WARNING, lw=1.2,
           connectionstyle="arc3,rad=0.25")

    # ── Legend ──────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(facecolor=SECONDARY, edgecolor=HIGHLIGHT, label="Admin"),
        mpatches.Patch(facecolor=SECONDARY, edgecolor=SUCCESS, label="Doctor"),
        mpatches.Patch(facecolor=SECONDARY, edgecolor=WARNING, label="Patient"),
    ]
    ax.legend(handles=legend_items, loc="lower left", fontsize=9,
              facecolor=DARK_BG, edgecolor=ACCENT, labelcolor=LIGHT_TEXT)

    _save(fig, "fig_3_1_use_case_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3.2 — ER Diagram
# ═══════════════════════════════════════════════════════════════════════════

def fig_3_2_er_diagram():
    fig, ax = _new_figure(14, 9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.99, "Entity-Relationship Diagram",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    # ── Table definitions ───────────────────────────────────────────────
    tables = {
        "users": {
            "pos": (0.03, 0.55), "w": 0.18, "h": 0.35,
            "cols": ["PK  id", "username", "email", "password_hash",
                     "role (A/D/P)", "created_at"],
        },
        "medical_reports": {
            "pos": (0.28, 0.55), "w": 0.20, "h": 0.35,
            "cols": ["PK  id", "FK  doctor_id", "FK  patient_id",
                     "title", "file_path", "file_hash (SHA-256)",
                     "created_at"],
        },
        "access_grants": {
            "pos": (0.55, 0.55), "w": 0.20, "h": 0.35,
            "cols": ["PK  id", "FK  report_id", "FK  granted_by",
                     "FK  granted_to", "status", "created_at"],
        },
        "blockchain": {
            "pos": (0.28, 0.07), "w": 0.20, "h": 0.35,
            "cols": ["PK  id", "index", "timestamp",
                     "data (JSON)", "prev_hash", "hash",
                     "nonce"],
        },
        "audit_log": {
            "pos": (0.55, 0.07), "w": 0.20, "h": 0.35,
            "cols": ["PK  id", "FK  user_id", "action",
                     "details", "ip_address", "timestamp"],
        },
    }

    for tname, info in tables.items():
        x, y = info["pos"]
        w, h = info["w"], info["h"]

        # header
        _box(ax, x, y + h - 0.07, w, 0.07, tname,
             color=SECONDARY, edge=ACCENT, fontsize=11)

        # body
        body = FancyBboxPatch(
            (x, y), w, h - 0.07,
            boxstyle="round,pad=0.02",
            facecolor=CARD_BG, edgecolor=ACCENT, linewidth=1,
        )
        ax.add_patch(body)

        for i, col in enumerate(info["cols"]):
            cy = y + h - 0.12 - i * 0.038
            col_color = WARNING if col.startswith("PK") else (
                HIGHLIGHT if col.startswith("FK") else LIGHT_TEXT
            )
            ax.text(x + 0.01, cy, col, fontsize=7.5, color=col_color,
                    va="center", fontfamily="monospace")

    # ── Relationships ───────────────────────────────────────────────────
    # users 1:M medical_reports  (doctor_id / patient_id)
    _arrow_label(ax, 0.21, 0.78, 0.28, 0.78, "1 : M",
                 color=SUCCESS, fontsize=8)
    _arrow_label(ax, 0.21, 0.72, 0.28, 0.72, "1 : M",
                 color=SUCCESS, fontsize=8)

    # users 1:M access_grants (granted_by / granted_to)
    _arrow_label(ax, 0.21, 0.65, 0.55, 0.78, "1 : M",
                 color=HIGHLIGHT, fontsize=8,
                 connectionstyle="arc3,rad=-0.15")

    # medical_reports 1:M access_grants (report_id)
    _arrow_label(ax, 0.48, 0.70, 0.55, 0.70, "1 : M",
                 color=WARNING, fontsize=8)

    # users 1:M audit_log
    _arrow_label(ax, 0.12, 0.55, 0.55, 0.38, "1 : M",
                 color=ACCENT, fontsize=8,
                 connectionstyle="arc3,rad=0.25")

    # ── Legend ──────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(color=WARNING, label="Primary Key (PK)"),
        mpatches.Patch(color=HIGHLIGHT, label="Foreign Key (FK)"),
        mpatches.Patch(color=LIGHT_TEXT, label="Attribute"),
    ]
    ax.legend(handles=legend_items, loc="lower left", fontsize=9,
              facecolor=DARK_BG, edgecolor=ACCENT, labelcolor=LIGHT_TEXT)

    _save(fig, "fig_3_2_er_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3.3 — Data Flow Diagram (Level 0)
# ═══════════════════════════════════════════════════════════════════════════

def fig_3_3_data_flow_diagram():
    fig, ax = _new_figure(14, 8)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.98, "Level-0 Data Flow Diagram",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    # ── External entities ───────────────────────────────────────────────
    entities = [
        ("Doctor",  0.05, 0.70),
        ("Patient", 0.05, 0.40),
        ("Admin",   0.05, 0.15),
    ]
    for name, ex, ey in entities:
        _box(ax, ex, ey, 0.14, 0.10, name,
             color=SECONDARY, edge=HIGHLIGHT, fontsize=11)

    # ── Central process ─────────────────────────────────────────────────
    center_x, center_y = 0.42, 0.42
    circle = plt.Circle((center_x + 0.09, center_y + 0.06), 0.12,
                        facecolor=CARD_BG, edgecolor=ACCENT, lw=2.5)
    ax.add_patch(circle)
    ax.text(center_x + 0.09, center_y + 0.06,
            "Medical Report\nManagement\nSystem",
            ha="center", va="center", fontsize=10, color=LIGHT_TEXT,
            fontweight="bold")

    # ── Data stores ─────────────────────────────────────────────────────
    stores = [
        ("D1  SQLite Database",  0.72, 0.72),
        ("D2  Blockchain Ledger", 0.72, 0.48),
        ("D3  File Storage",     0.72, 0.24),
    ]
    for label, sx, sy in stores:
        # Open-ended rectangle style
        ax.plot([sx, sx + 0.25], [sy + 0.07, sy + 0.07],
                color=ACCENT, lw=2)
        ax.plot([sx, sx], [sy, sy + 0.07], color=ACCENT, lw=2)
        ax.plot([sx, sx + 0.25], [sy, sy], color=ACCENT, lw=2)
        rect = FancyBboxPatch(
            (sx, sy), 0.25, 0.07,
            boxstyle="square,pad=0",
            facecolor=CARD_BG, edgecolor="none",
        )
        ax.add_patch(rect)
        ax.text(sx + 0.125, sy + 0.035, label, ha="center", va="center",
                fontsize=9, color=LIGHT_TEXT, fontweight="bold")

    # ── Flows: entities -> process ──────────────────────────────────────
    flows_in = [
        (0.19, 0.75, 0.40, 0.52, "Upload\nReport",    SUCCESS),
        (0.19, 0.45, 0.40, 0.47, "View / Share\nRequest", WARNING),
        (0.19, 0.20, 0.40, 0.40, "Audit / Verify\nRequest", HIGHLIGHT),
    ]
    for x1, y1, x2, y2, lbl, clr in flows_in:
        _arrow_label(ax, x1, y1, x2, y2, lbl, color=clr, fontsize=8)

    # ── Flows: process -> data stores ───────────────────────────────────
    flows_out = [
        (0.60, 0.52, 0.72, 0.76, "Read / Write\nRecords", SUCCESS),
        (0.60, 0.48, 0.72, 0.52, "Add Block /\nVerify Chain", HIGHLIGHT),
        (0.60, 0.42, 0.72, 0.28, "Store / Retrieve\nFiles", WARNING),
    ]
    for x1, y1, x2, y2, lbl, clr in flows_out:
        _arrow_label(ax, x1, y1, x2, y2, lbl, color=clr, fontsize=8)

    # ── Flows: process -> entities (responses) ──────────────────────────
    _arrow_label(ax, 0.40, 0.55, 0.19, 0.77, "Report\nStatus",
                 color=SUCCESS, fontsize=7,
                 connectionstyle="arc3,rad=-0.15")
    _arrow_label(ax, 0.40, 0.44, 0.19, 0.47, "Report\nData",
                 color=WARNING, fontsize=7,
                 connectionstyle="arc3,rad=-0.1")
    _arrow_label(ax, 0.40, 0.38, 0.19, 0.22, "Audit\nResults",
                 color=HIGHLIGHT, fontsize=7,
                 connectionstyle="arc3,rad=-0.15")

    _save(fig, "fig_3_3_data_flow_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3.4 — Blockchain Flow
# ═══════════════════════════════════════════════════════════════════════════

def fig_3_4_blockchain_flow():
    fig, ax = _new_figure(16, 7)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.97, "Blockchain — Block Linking Visualization",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    blocks = [
        {
            "title": "Genesis Block",
            "index": 0,
            "data": "System Init",
            "prev": "0" * 8 + "...",
            "hash": "a3f7c1d9...",
        },
        {
            "title": "Block 1",
            "index": 1,
            "data": "Report Upload\n(SHA-256 hash)",
            "prev": "a3f7c1d9...",
            "hash": "5b8e02fa...",
        },
        {
            "title": "Block 2",
            "index": 2,
            "data": "Access Grant\n(Patient share)",
            "prev": "5b8e02fa...",
            "hash": "d41c93e7...",
        },
        {
            "title": "Block 3",
            "index": 3,
            "data": "Report View\n(Audit entry)",
            "prev": "d41c93e7...",
            "hash": "f209ab31...",
        },
    ]

    bw, bh = 0.19, 0.60
    gap = 0.06
    start_x = 0.04
    base_y = 0.12

    for i, blk in enumerate(blocks):
        bx = start_x + i * (bw + gap)

        # Block outer
        outer = FancyBboxPatch(
            (bx, base_y), bw, bh,
            boxstyle="round,pad=0.02",
            facecolor=CARD_BG, edgecolor=ACCENT, linewidth=2,
        )
        ax.add_patch(outer)

        # Title header
        _box(ax, bx + 0.01, base_y + bh - 0.09, bw - 0.02, 0.07,
             blk["title"], color=SECONDARY, edge=ACCENT, fontsize=10)

        # Fields
        fields = [
            f"Index: {blk['index']}",
            f"Data:\n  {blk['data']}",
            f"Prev Hash:\n  {blk['prev']}",
            f"Hash:\n  {blk['hash']}",
        ]
        field_ys = [0.50, 0.39, 0.24, 0.13]
        field_colors = [LIGHT_TEXT, SUCCESS, WARNING, HIGHLIGHT]
        for fy, field, fc in zip(field_ys, fields, field_colors):
            ax.text(bx + 0.015, base_y + fy, field,
                    fontsize=7.5, color=fc, va="center",
                    fontfamily="monospace")

        # Chain arrow
        if i > 0:
            ax.annotate(
                "", xy=(bx, base_y + bh / 2),
                xytext=(bx - gap, base_y + bh / 2),
                arrowprops=dict(
                    arrowstyle="-|>", color=HIGHLIGHT, lw=2.5,
                    mutation_scale=18,
                ),
            )
            # Hash link label
            ax.text(bx - gap / 2, base_y + bh / 2 + 0.04, "hash\nlink",
                    ha="center", va="bottom", fontsize=7, color=HIGHLIGHT,
                    fontweight="bold")

    # ── Explanation note ────────────────────────────────────────────────
    ax.text(0.5, 0.04,
            "Each block's 'Prev Hash' equals the preceding block's 'Hash', "
            "forming an immutable chain secured by SHA-256.",
            ha="center", va="center", fontsize=9, color=LIGHT_TEXT,
            style="italic",
            bbox=dict(facecolor=SECONDARY, edgecolor=ACCENT, boxstyle="round,pad=0.4"))

    _save(fig, "fig_3_4_blockchain_flow.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3.5 — Activity Diagram (Report Upload & Sharing)
# ═══════════════════════════════════════════════════════════════════════════

def fig_3_5_activity_diagram():
    fig, ax = _new_figure(14, 9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    ax.text(0.5, 0.99, "Activity Diagram — Report Upload & Sharing",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    # ── Start node ──────────────────────────────────────────────────────
    start = plt.Circle((0.50, 0.92), 0.015, facecolor=LIGHT_TEXT,
                       edgecolor=LIGHT_TEXT, lw=2)
    ax.add_patch(start)

    # ── Activity boxes ──────────────────────────────────────────────────
    activities = [
        ("Doctor Logs In",               0.38, 0.83, SUCCESS),
        ("Doctor Uploads\nMedical Report", 0.38, 0.72, SUCCESS),
        ("System Computes\nSHA-256 Hash",  0.38, 0.61, ACCENT),
        ("New Block Added\nto Blockchain", 0.38, 0.50, HIGHLIGHT),
        ("Report Stored\nin Database",     0.38, 0.39, ACCENT),
        ("Patient Logs In\n& Views Report", 0.38, 0.28, WARNING),
        ("Patient Shares\nAccess",          0.38, 0.17, WARNING),
        ("Access Grant Block\nAdded to Chain", 0.38, 0.06, HIGHLIGHT),
    ]

    box_w, box_h = 0.24, 0.07
    for label, bx, by, edge_c in activities:
        _box(ax, bx, by, box_w, box_h, label,
             color=CARD_BG, edge=edge_c, fontsize=9)

    # ── Arrows between activities ───────────────────────────────────────
    ys = [a[2] for a in activities]
    # Start -> first activity
    _arrow(ax, 0.50, 0.905, 0.50, 0.83 + box_h, color=LIGHT_TEXT, lw=1.5)

    for i in range(len(ys) - 1):
        _arrow(ax, 0.50, ys[i], 0.50, ys[i + 1] + box_h,
               color=LIGHT_TEXT, lw=1.5)

    # ── End node ────────────────────────────────────────────────────────
    end_outer = plt.Circle((0.50, 0.01), 0.018, facecolor="none",
                           edgecolor=LIGHT_TEXT, lw=2)
    end_inner = plt.Circle((0.50, 0.01), 0.010, facecolor=LIGHT_TEXT,
                           edgecolor=LIGHT_TEXT, lw=1)
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)
    _arrow(ax, 0.50, 0.06, 0.50, 0.028, color=LIGHT_TEXT, lw=1.5)

    # ── Swim-lane labels ────────────────────────────────────────────────
    ax.text(0.75, 0.78, "Doctor\nActions", ha="center", va="center",
            fontsize=11, color=SUCCESS, fontweight="bold",
            bbox=dict(facecolor=DARK_BG, edgecolor=SUCCESS,
                      boxstyle="round,pad=0.3"))
    ax.text(0.75, 0.56, "System\nProcessing", ha="center", va="center",
            fontsize=11, color=ACCENT, fontweight="bold",
            bbox=dict(facecolor=DARK_BG, edgecolor=ACCENT,
                      boxstyle="round,pad=0.3"))
    ax.text(0.75, 0.23, "Patient\nActions", ha="center", va="center",
            fontsize=11, color=WARNING, fontweight="bold",
            bbox=dict(facecolor=DARK_BG, edgecolor=WARNING,
                      boxstyle="round,pad=0.3"))

    # ── Annotations with side arrows ────────────────────────────────────
    _arrow(ax, 0.70, 0.78, 0.62, 0.755, color=SUCCESS, lw=1,
           connectionstyle="arc3,rad=0.15")
    _arrow(ax, 0.70, 0.56, 0.62, 0.545, color=ACCENT, lw=1,
           connectionstyle="arc3,rad=0.15")
    _arrow(ax, 0.70, 0.23, 0.62, 0.315, color=WARNING, lw=1,
           connectionstyle="arc3,rad=-0.15")

    _save(fig, "fig_3_5_activity_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 4.1 — Agile Methodology (Sprint Timeline)
# ═══════════════════════════════════════════════════════════════════════════

def fig_4_1_agile_methodology():
    fig, ax = _new_figure(14, 7)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.10, 1.05)

    ax.text(0.5, 0.98, "Agile Methodology — Sprint Plan",
            ha="center", va="top", fontsize=16, color=ACCENT,
            fontweight="bold")

    sprints = [
        {
            "name": "Sprint 1",
            "title": "Database &\nAuthentication",
            "tasks": ["SQLite schema (5 tables)",
                      "User registration / login",
                      "Role-based access (RBAC)",
                      "Password hashing (bcrypt)"],
            "color": SUCCESS,
        },
        {
            "name": "Sprint 2",
            "title": "Blockchain &\nFile Upload",
            "tasks": ["Blockchain class impl.",
                      "SHA-256 file hashing",
                      "Genesis block creation",
                      "Report upload endpoint"],
            "color": HIGHLIGHT,
        },
        {
            "name": "Sprint 3",
            "title": "Access Control\n& Sharing",
            "tasks": ["Access grant / revoke",
                      "Doctor-patient linking",
                      "Block for every grant",
                      "Permission validation"],
            "color": WARNING,
        },
        {
            "name": "Sprint 4",
            "title": "Dashboard\n& Audit",
            "tasks": ["Admin dashboard",
                      "Blockchain integrity check",
                      "Audit log viewer",
                      "Role-based dashboards"],
            "color": ACCENT,
        },
        {
            "name": "Sprint 5",
            "title": "Testing &\nDeployment",
            "tasks": ["Unit & integration tests",
                      "UI/UX polish (Bootstrap 5)",
                      "Docker containerisation",
                      "Final documentation"],
            "color": "#c678dd",
        },
    ]

    n = len(sprints)
    card_w = 0.16
    total_w = n * card_w + (n - 1) * 0.025
    start_x = (1.0 - total_w) / 2

    # ── Timeline line ───────────────────────────────────────────────────
    tl_y = 0.82
    ax.plot([start_x - 0.02, start_x + total_w + 0.02], [tl_y, tl_y],
            color=ACCENT, lw=2.5, zorder=1)

    for i, sp in enumerate(sprints):
        sx = start_x + i * (card_w + 0.025)

        # Timeline dot
        dot = plt.Circle((sx + card_w / 2, tl_y), 0.012,
                         facecolor=sp["color"], edgecolor=LIGHT_TEXT,
                         lw=1.5, zorder=3)
        ax.add_patch(dot)

        # Sprint label above timeline
        ax.text(sx + card_w / 2, tl_y + 0.04, sp["name"],
                ha="center", va="bottom", fontsize=10,
                color=sp["color"], fontweight="bold")

        # Card
        card_h = 0.55
        card_y = tl_y - 0.06 - card_h
        card = FancyBboxPatch(
            (sx, card_y), card_w, card_h,
            boxstyle="round,pad=0.02",
            facecolor=CARD_BG, edgecolor=sp["color"], linewidth=2,
        )
        ax.add_patch(card)

        # Connector from timeline to card
        ax.plot([sx + card_w / 2, sx + card_w / 2],
                [tl_y - 0.012, card_y + card_h],
                color=sp["color"], lw=1.5, ls="--")

        # Card title
        ax.text(sx + card_w / 2, card_y + card_h - 0.04, sp["title"],
                ha="center", va="center", fontsize=9,
                color=sp["color"], fontweight="bold")

        # Separator line
        sep_y = card_y + card_h - 0.10
        ax.plot([sx + 0.01, sx + card_w - 0.01], [sep_y, sep_y],
                color=sp["color"], lw=0.8, alpha=0.5)

        # Tasks
        for j, task in enumerate(sp["tasks"]):
            ty = sep_y - 0.05 - j * 0.09
            ax.text(sx + 0.015, ty, f"  {task}",
                    fontsize=7, color=LIGHT_TEXT, va="center")
            # bullet
            bullet = plt.Circle((sx + 0.025, ty), 0.004,
                                facecolor=sp["color"], edgecolor="none")
            ax.add_patch(bullet)

    # ── Arrow at end of timeline ────────────────────────────────────────
    ax.annotate(
        "", xy=(start_x + total_w + 0.04, tl_y),
        xytext=(start_x + total_w + 0.02, tl_y),
        arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=2.5),
    )

    _save(fig, "fig_4_1_agile_methodology.png")


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("Generating figures for B6 — Medical Report Blockchain Project")
    print(f"Output directory: {FIGURES_DIR}\n")

    fig_1_1_system_architecture()
    fig_3_1_use_case_diagram()
    fig_3_2_er_diagram()
    fig_3_3_data_flow_diagram()
    fig_3_4_blockchain_flow()
    fig_3_5_activity_diagram()
    fig_4_1_agile_methodology()

    print(f"\nAll 7 figures saved to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
