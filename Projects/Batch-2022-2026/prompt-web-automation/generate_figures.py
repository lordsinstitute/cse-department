"""
generate_figures.py
===================
Generates 7 dark-themed matplotlib diagrams for the
"Prompt-Driven AI Web Automation" project report.

Project: Claude AI + Playwright browser automation, Flask-SocketIO, port 5050
Modules: Web Data Extraction Agent  |  AI Form Filler Bot

Run:
    python generate_figures.py

Output:
    figures/system_architecture.png
    figures/use_case_diagram.png
    figures/class_diagram.png
    figures/sequence_diagram.png
    figures/activity_diagram.png
    figures/er_diagram.png
    figures/agile_model.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import matplotlib.patheffects as pe
import numpy as np

# ── Dark-theme palette ─────────────────────────────────────────────────────
BG       = "#1a1a2e"
ACCENT   = "#06b6d4"   # cyan — matches the app's UI theme
SECONDARY = "#0ea5e9"
TEXT     = "white"
GRID     = "#333355"
MUTED    = "#8892b0"
DARK_BOX = "#16213e"
MID_BOX  = "#0f3460"
HIGHLIGHT = "#e94560"
SUCCESS  = "#10b981"
WARNING  = "#f59e0b"
PURPLE   = "#a78bfa"
PINK     = "#ec4899"
ORANGE   = "#f97316"

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def _setup_fig(title, figsize=(14, 10)):
    """Create a figure with the dark theme and a centered title."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(title, color=TEXT, fontsize=20, fontweight="bold", pad=20)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    return fig, ax


def _rounded_box(ax, xy, width, height, text, color=ACCENT,
                 text_color=TEXT, fontsize=11, radius=0.3, lw=2,
                 text_lines=None, alpha=1.0):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch(
        xy, width, height,
        boxstyle=f"round,pad={radius}",
        facecolor=color, edgecolor="white", linewidth=lw, alpha=alpha,
        zorder=3,
    )
    ax.add_patch(box)
    cx = xy[0] + width / 2
    cy = xy[1] + height / 2
    if text_lines:
        n = len(text_lines)
        line_h = 0.22
        start_y = cy + (n - 1) * line_h / 2
        for i, line in enumerate(text_lines):
            fs = fontsize if i > 0 else fontsize + 1
            fw = "bold" if i == 0 else "normal"
            ax.text(cx, start_y - i * line_h, line,
                    ha="center", va="center", color=text_color,
                    fontsize=fs, fontweight=fw, zorder=4)
    else:
        ax.text(cx, cy, text, ha="center", va="center",
                color=text_color, fontsize=fontsize, fontweight="bold",
                zorder=4)
    return box


def _arrow(ax, x1, y1, x2, y2, color=ACCENT, lw=1.8, style="->",
           connectionstyle="arc3,rad=0"):
    """Draw a fancy arrow between two points."""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, color=color, lw=lw,
        connectionstyle=connectionstyle, zorder=5,
        mutation_scale=15,
    )
    ax.add_patch(arrow)
    return arrow


def _label_arrow(ax, x1, y1, x2, y2, label="", color=ACCENT, lw=1.8,
                 label_offset=(0, 0.15), fontsize=8, style="->",
                 connectionstyle="arc3,rad=0"):
    """Arrow with a label at the midpoint."""
    _arrow(ax, x1, y1, x2, y2, color=color, lw=lw, style=style,
           connectionstyle=connectionstyle)
    mx = (x1 + x2) / 2 + label_offset[0]
    my = (y1 + y2) / 2 + label_offset[1]
    if label:
        ax.text(mx, my, label, ha="center", va="center",
                color=MUTED, fontsize=fontsize, fontstyle="italic", zorder=6)


# ═══════════════════════════════════════════════════════════════════════════
# 1. SYSTEM ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════
def fig_system_architecture():
    fig, ax = _setup_fig("System Architecture — Multi-Layer Design", figsize=(16, 10))

    layers = [
        ("Presentation Layer",    "#0d9488", 8.2,
         ["Flask Templates (Jinja2)", "SocketIO Real-Time UI", "Bootstrap 5 Dark Theme"]),
        ("Application Layer",     "#0369a1", 6.4,
         ["Flask Routes (web/)", "Flask-Login Auth", "PDF Upload & Parse"]),
        ("Agent Layer",           "#7c3aed", 4.6,
         ["BaseAgent", "ScraperAgent", "FormFillerAgent"]),
        ("Browser Layer",         "#b45309", 2.8,
         ["Playwright (Chromium)", "BrowserManager", "PageState / BrowserActions"]),
        ("LLM Layer",             "#be123c", 1.0,
         ["Claude AI (Anthropic API)", "7 tool_use Tools", "Structured JSON Responses"]),
    ]

    for label, color, y, items in layers:
        # full-width layer band
        _rounded_box(ax, (0.3, y), 9.4, 1.3, "", color=color, alpha=0.25, radius=0.2)
        ax.text(0.6, y + 1.05, label, color=color, fontsize=14,
                fontweight="bold", va="center", zorder=4)
        # individual component boxes
        n = len(items)
        box_w = 2.6
        gap = (9.4 - n * box_w) / (n + 1)
        for i, item in enumerate(items):
            bx = 0.3 + gap + i * (box_w + gap)
            _rounded_box(ax, (bx, y + 0.1), box_w, 0.6, item,
                         color=color, fontsize=9, radius=0.15, alpha=0.85)

    # downward arrows between layers
    for i in range(len(layers) - 1):
        y_top = layers[i][2]
        y_bot = layers[i + 1][2] + 1.3
        _arrow(ax, 5, y_top, 5, y_bot, color=MUTED, lw=2.5, style="-|>")

    # side labels
    ax.text(10.0, 5.0, "Port 5050\nFlask-SocketIO",
            ha="center", va="center", color=MUTED, fontsize=10,
            fontstyle="italic", bbox=dict(boxstyle="round,pad=0.4",
            facecolor=DARK_BOX, edgecolor=GRID))

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "system_architecture.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[1/7] system_architecture.png")


# ═══════════════════════════════════════════════════════════════════════════
# 2. USE-CASE DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
def fig_use_case_diagram():
    fig, ax = _setup_fig("Use-Case Diagram", figsize=(16, 10))

    # ── Actor (stick figure) ───────────────────────────────────────────
    actor_x, actor_y = 1.5, 5.0
    head_r = 0.25
    ax.add_patch(plt.Circle((actor_x, actor_y + 1.0), head_r,
                            fill=False, edgecolor=ACCENT, lw=2, zorder=4))
    ax.plot([actor_x, actor_x], [actor_y + 0.75, actor_y + 0.1],
            color=ACCENT, lw=2, zorder=4)                          # body
    ax.plot([actor_x - 0.35, actor_x, actor_x + 0.35],
            [actor_y + 0.55, actor_y + 0.65, actor_y + 0.55],
            color=ACCENT, lw=2, zorder=4)                          # arms
    ax.plot([actor_x - 0.25, actor_x, actor_x + 0.25],
            [actor_y - 0.35, actor_y + 0.1, actor_y - 0.35],
            color=ACCENT, lw=2, zorder=4)                          # legs
    ax.text(actor_x, actor_y - 0.6, "User", ha="center",
            color=TEXT, fontsize=12, fontweight="bold")

    # ── System boundary ────────────────────────────────────────────────
    _rounded_box(ax, (3.2, 0.4), 6.5, 9.2, "", color=DARK_BOX,
                 alpha=0.4, radius=0.3, lw=1.5)
    ax.text(6.45, 9.3, "Prompt-Driven AI Web Automation System",
            ha="center", color=ACCENT, fontsize=13, fontweight="bold")

    # ── Module 1: Web Data Extraction ──────────────────────────────────
    m1_cases = [
        "Register / Login",
        "Enter Extraction Prompt",
        "Upload Target URL",
        "View Real-Time Progress",
        "Preview Extracted Data",
        "Export to Excel / JSON",
    ]
    ax.text(5.0, 8.7, "Module 1: Web Data Extraction Agent",
            ha="center", color=SUCCESS, fontsize=11, fontweight="bold")
    for i, uc in enumerate(m1_cases):
        ey = 8.1 - i * 0.75
        ellipse = mpatches.Ellipse((5.0, ey), 2.8, 0.55,
                                    facecolor=MID_BOX, edgecolor=SUCCESS,
                                    lw=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(5.0, ey, uc, ha="center", va="center",
                color=TEXT, fontsize=9, zorder=4)
        _arrow(ax, actor_x + 0.4, actor_y + 0.5, 5.0 - 1.4, ey,
               color=GRID, lw=1, style="->")

    # ── Module 2: AI Form Filler Bot ───────────────────────────────────
    m2_cases = [
        "Upload PDF Resume",
        "Provide Form URL",
        "Watch AI Fill Form",
        "Review & Confirm Submission",
    ]
    ax.text(8.2, 8.7, "Module 2: AI Form Filler Bot",
            ha="center", color=WARNING, fontsize=11, fontweight="bold")
    for i, uc in enumerate(m2_cases):
        ey = 8.1 - i * 0.75
        ellipse = mpatches.Ellipse((8.2, ey), 2.6, 0.55,
                                    facecolor=MID_BOX, edgecolor=WARNING,
                                    lw=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(8.2, ey, uc, ha="center", va="center",
                color=TEXT, fontsize=9, zorder=4)
        _arrow(ax, actor_x + 0.4, actor_y + 0.3, 8.2 - 1.3, ey,
               color=GRID, lw=1, style="->")

    # ── External actors ────────────────────────────────────────────────
    # Claude AI
    ax.text(8.5, 1.0, "Claude AI\n(Anthropic)", ha="center",
            color=PURPLE, fontsize=10, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BOX,
                      edgecolor=PURPLE, lw=1.5))
    _arrow(ax, 7.5, 1.5, 8.0, 1.3, color=PURPLE, lw=1.2)

    # Target Website
    ax.text(5.0, 0.8, "Target\nWebsite", ha="center",
            color=ORANGE, fontsize=10, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BOX,
                      edgecolor=ORANGE, lw=1.5))

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "use_case_diagram.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[2/7] use_case_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
# 3. CLASS DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
def fig_class_diagram():
    fig, ax = _setup_fig("Class Diagram", figsize=(16, 10))

    def _class_box(ax, x, y, name, attrs, methods, color=ACCENT, w=2.8):
        """UML-style class box: name | attributes | methods."""
        line_h = 0.28
        n_attr = len(attrs)
        n_meth = len(methods)
        total_h = (1 + n_attr + n_meth) * line_h + 0.3
        # background
        _rounded_box(ax, (x, y - total_h), w, total_h, "",
                     color=DARK_BOX, alpha=0.85, radius=0.12, lw=1.5)
        # class name
        ax.text(x + w / 2, y - line_h * 0.6, name, ha="center", va="center",
                color=color, fontsize=10, fontweight="bold", zorder=4)
        # separator line
        sep_y = y - line_h * 1.1
        ax.plot([x + 0.1, x + w - 0.1], [sep_y, sep_y],
                color=GRID, lw=1, zorder=4)
        # attributes
        for i, a in enumerate(attrs):
            ax.text(x + 0.15, sep_y - (i + 0.7) * line_h, a,
                    color=MUTED, fontsize=8, va="center", zorder=4,
                    fontfamily="monospace")
        sep2_y = sep_y - (n_attr + 0.2) * line_h
        ax.plot([x + 0.1, x + w - 0.1], [sep2_y, sep2_y],
                color=GRID, lw=1, zorder=4)
        # methods
        for i, m in enumerate(methods):
            ax.text(x + 0.15, sep2_y - (i + 0.7) * line_h, m,
                    color=SUCCESS, fontsize=8, va="center", zorder=4,
                    fontfamily="monospace")
        return (x, y - total_h, w, total_h)

    # ── BaseAgent ──────────────────────────────────────────────────────
    _class_box(ax, 3.6, 9.8, "BaseAgent (ABC)",
               ["- llm: ClaudeClient", "- browser: BrowserManager",
                "- max_steps: int"],
               ["+ run(prompt)", "+ step()", "+ get_tools()"],
               color=ACCENT, w=3.0)

    # ── ScraperAgent ───────────────────────────────────────────────────
    _class_box(ax, 0.5, 6.2, "ScraperAgent",
               ["- extraction_prompt: str", "- results: list"],
               ["+ run(url, prompt)", "+ parse_result()", "+ export()"],
               color=SUCCESS, w=2.8)

    # ── FormFillerAgent ────────────────────────────────────────────────
    _class_box(ax, 6.8, 6.2, "FormFillerAgent",
               ["- pdf_data: dict", "- form_url: str"],
               ["+ run(url, pdf)", "+ fill_fields()", "+ submit()"],
               color=WARNING, w=2.8)

    # ── BrowserManager ─────────────────────────────────────────────────
    _class_box(ax, 0.2, 3.4, "BrowserManager",
               ["- browser: Browser", "- page: Page"],
               ["+ launch()", "+ close()", "+ get_state()"],
               color=SECONDARY, w=2.6)

    # ── PageState ──────────────────────────────────────────────────────
    _class_box(ax, 3.2, 3.4, "PageState",
               ["- url: str", "- title: str", "- elements: list"],
               ["+ snapshot()", "+ to_prompt()"],
               color=PURPLE, w=2.4)

    # ── BrowserActions ─────────────────────────────────────────────────
    _class_box(ax, 5.9, 3.4, "BrowserActions",
               ["- page: Page"],
               ["+ click()", "+ fill()", "+ select()",
                "+ navigate()", "+ scroll()"],
               color=PINK, w=2.5)

    # ── ClaudeClient ───────────────────────────────────────────────────
    _class_box(ax, 8.8, 3.4, "ClaudeClient",
               ["- api_key: str", "- model: str"],
               ["+ chat(messages, tools)", "+ parse_tool_use()"],
               color=HIGHLIGHT, w=2.6)

    # ── PDFParser ──────────────────────────────────────────────────────
    _class_box(ax, 1.0, 0.9, "PDFParser",
               ["- file_path: str"],
               ["+ extract_text()", "+ to_dict()"],
               color=ORANGE, w=2.4)

    # ── ExcelExporter ──────────────────────────────────────────────────
    _class_box(ax, 7.0, 0.9, "ExcelExporter",
               ["- data: list[dict]"],
               ["+ to_excel(path)", "+ to_json(path)"],
               color="#14b8a6", w=2.6)

    # ── Inheritance arrows (BaseAgent → children) ──────────────────────
    # ScraperAgent
    _arrow(ax, 1.9, 6.2, 4.5, 7.5, color=MUTED, lw=1.8, style="-|>")
    ax.text(2.7, 7.0, "extends", color=MUTED, fontsize=8, fontstyle="italic",
            rotation=30)
    # FormFillerAgent
    _arrow(ax, 8.2, 6.2, 5.7, 7.5, color=MUTED, lw=1.8, style="-|>")
    ax.text(7.3, 7.0, "extends", color=MUTED, fontsize=8, fontstyle="italic",
            rotation=-30)

    # ── Composition arrows ─────────────────────────────────────────────
    _arrow(ax, 1.5, 3.4, 2.5, 5.0, color=GRID, lw=1.2, style="->")
    _arrow(ax, 4.4, 3.4, 3.5, 5.0, color=GRID, lw=1.2, style="->")
    _arrow(ax, 7.1, 3.4, 7.5, 5.0, color=GRID, lw=1.2, style="->")
    _arrow(ax, 10.1, 3.4, 8.5, 5.0, color=GRID, lw=1.2, style="->")

    # ── Legend ─────────────────────────────────────────────────────────
    ax.text(11.5, 9.5, "Relationships", color=TEXT, fontsize=10,
            fontweight="bold")
    _arrow(ax, 11.5, 9.1, 12.3, 9.1, color=MUTED, lw=1.8, style="-|>")
    ax.text(12.5, 9.1, "Inheritance", color=MUTED, fontsize=9, va="center")
    _arrow(ax, 11.5, 8.7, 12.3, 8.7, color=GRID, lw=1.2, style="->")
    ax.text(12.5, 8.7, "Composition", color=MUTED, fontsize=9, va="center")

    ax.set_xlim(-0.2, 14)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "class_diagram.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[3/7] class_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
# 4. SEQUENCE DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
def fig_sequence_diagram():
    fig, ax = _setup_fig("Sequence Diagram — Automation Workflow", figsize=(16, 10))

    # ── Lifelines ──────────────────────────────────────────────────────
    actors = [
        ("User",       1.5,  ACCENT),
        ("Flask\nApp", 3.5,  SECONDARY),
        ("Agent",      5.5,  SUCCESS),
        ("Claude\nAI", 7.5,  PURPLE),
        ("Playwright", 9.5,  WARNING),
        ("Website",    11.5, ORANGE),
    ]
    top_y = 9.0
    bot_y = 0.5
    for name, x, color in actors:
        _rounded_box(ax, (x - 0.6, top_y), 1.2, 0.7, name,
                     color=color, fontsize=9, radius=0.12)
        ax.plot([x, x], [top_y, bot_y], color=GRID, lw=1,
                linestyle="--", zorder=1)

    # ── Messages ───────────────────────────────────────────────────────
    messages = [
        (1.5, 3.5, 8.3, "1. Submit prompt + URL",           ACCENT),
        (3.5, 5.5, 7.8, "2. Create agent, start task",      SECONDARY),
        (5.5, 7.5, 7.3, "3. Send page state + tools",       SUCCESS),
        (7.5, 5.5, 6.8, "4. Return tool_use (click/fill)",  PURPLE),
        (5.5, 9.5, 6.3, "5. Execute browser action",        SUCCESS),
        (9.5, 11.5, 5.8, "6. Interact with DOM",            WARNING),
        (11.5, 9.5, 5.3, "7. Return page HTML",             ORANGE),
        (9.5, 5.5, 4.8, "8. Updated PageState",             WARNING),
        (5.5, 7.5, 4.3, "9. Next step (loop 3-8)",          SUCCESS),
        (7.5, 5.5, 3.8, "10. tool_use: done / extract_data", PURPLE),
        (5.5, 3.5, 3.3, "11. Return results",               SUCCESS),
        (3.5, 3.5, 2.8, "12. SocketIO emit → UI update",    SECONDARY),
        (3.5, 1.5, 2.3, "13. Display results / export",     SECONDARY),
    ]
    for x1, x2, y, label, color in messages:
        _arrow(ax, x1, y, x2, y, color=color, lw=1.5, style="-|>")
        mid_x = (x1 + x2) / 2
        offset = 0.15
        ax.text(mid_x, y + offset, label, ha="center", va="bottom",
                color=color, fontsize=8, fontweight="bold", zorder=6)

    # ── Loop box (steps 3-8) ───────────────────────────────────────────
    _rounded_box(ax, (4.8, 3.6), 7.2, 4.4, "", color=GRID,
                 alpha=0.15, radius=0.15, lw=1)
    ax.text(5.0, 7.85, "loop", color=MUTED, fontsize=9,
            fontweight="bold", fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=BG,
                      edgecolor=GRID, lw=1))
    ax.text(5.8, 7.85, "[until done tool is called]",
            color=MUTED, fontsize=8, fontstyle="italic")

    ax.set_xlim(0, 13)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sequence_diagram.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[4/7] sequence_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
# 5. ACTIVITY DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
def fig_activity_diagram():
    fig, ax = _setup_fig("Activity Diagram — Automation Loop", figsize=(14, 10))

    # ── Helper: rounded activity box ───────────────────────────────────
    def _act(x, y, text, color=ACCENT, w=2.4, h=0.55):
        _rounded_box(ax, (x - w / 2, y - h / 2), w, h, text,
                     color=color, fontsize=9, radius=0.15)

    # ── Helper: diamond decision ───────────────────────────────────────
    def _diamond(x, y, text, color=WARNING, size=0.45):
        pts = np.array([
            [x, y + size], [x + size, y], [x, y - size], [x - size, y]
        ])
        diamond = plt.Polygon(pts, facecolor=DARK_BOX, edgecolor=color,
                              lw=2, zorder=3)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha="center", va="center", color=color,
                fontsize=8, fontweight="bold", zorder=4)

    # ── Start (filled circle) ─────────────────────────────────────────
    ax.add_patch(plt.Circle((5, 9.5), 0.18, facecolor=ACCENT,
                            edgecolor=TEXT, lw=2, zorder=4))
    ax.text(5, 9.5, "S", ha="center", va="center", color=BG,
            fontsize=10, fontweight="bold", zorder=5)

    # ── Activities ─────────────────────────────────────────────────────
    _act(5, 8.8, "User submits prompt", ACCENT)
    _act(5, 8.0, "Upload URL / PDF", SECONDARY)

    _diamond(5, 7.2, "Module?", WARNING, 0.4)
    ax.text(3.2, 7.35, "Extraction", color=SUCCESS, fontsize=9,
            fontweight="bold")
    ax.text(6.6, 7.35, "Form Fill", color=PINK, fontsize=9,
            fontweight="bold")

    # Left branch — Extraction
    _act(2.5, 6.3, "Create ScraperAgent", SUCCESS)
    _act(2.5, 5.5, "Navigate to URL", SUCCESS)

    # Right branch — Form Fill
    _act(7.5, 6.3, "Parse PDF (pymupdf4llm)", PINK)
    _act(7.5, 5.5, "Create FormFillerAgent", PINK)

    # Merge into common loop
    _act(5, 4.7, "Send state to Claude AI", PURPLE, w=2.8)

    _diamond(5, 3.9, "Tool?", WARNING, 0.4)

    # Tool actions
    _act(2.2, 3.2, "click / fill / select\nnavigate / scroll", ORANGE, w=2.6, h=0.65)
    _act(7.8, 3.2, "extract_data / done", HIGHLIGHT, w=2.4)

    # Loop back
    _act(2.2, 2.3, "Execute via Playwright", SECONDARY, w=2.6)
    _act(2.2, 1.5, "Update PageState", SECONDARY, w=2.6)

    # Result path
    _act(7.8, 2.3, "Collect Results", SUCCESS, w=2.4)
    _act(7.8, 1.5, "Export Excel / JSON", SUCCESS, w=2.4)

    # End
    ax.add_patch(plt.Circle((7.8, 0.7), 0.18, facecolor=BG,
                            edgecolor=ACCENT, lw=3, zorder=4))
    ax.add_patch(plt.Circle((7.8, 0.7), 0.12, facecolor=ACCENT,
                            edgecolor=ACCENT, lw=1, zorder=5))

    # ── Arrows ─────────────────────────────────────────────────────────
    _arrow(ax, 5, 9.32, 5, 9.08, color=MUTED)
    _arrow(ax, 5, 8.52, 5, 8.28, color=MUTED)
    _arrow(ax, 5, 7.72, 5, 7.6, color=MUTED)

    # decision → branches
    _arrow(ax, 4.6, 7.2, 3.7, 6.58, color=SUCCESS, lw=1.5)
    _arrow(ax, 5.4, 7.2, 6.3, 6.58, color=PINK, lw=1.5)

    # left branch down
    _arrow(ax, 2.5, 6.02, 2.5, 5.78, color=MUTED)
    _arrow(ax, 2.5, 5.22, 4.0, 4.98, color=MUTED)

    # right branch down
    _arrow(ax, 7.5, 6.02, 7.5, 5.78, color=MUTED)
    _arrow(ax, 7.5, 5.22, 6.0, 4.98, color=MUTED)

    # main loop
    _arrow(ax, 5, 4.42, 5, 4.3, color=MUTED)

    # tool decision → branches
    _arrow(ax, 4.6, 3.9, 3.5, 3.52, color=ORANGE, lw=1.5)
    ax.text(3.7, 3.75, "action", color=ORANGE, fontsize=8, fontstyle="italic")
    _arrow(ax, 5.4, 3.9, 6.6, 3.5, color=HIGHLIGHT, lw=1.5)
    ax.text(6.1, 3.75, "done", color=HIGHLIGHT, fontsize=8, fontstyle="italic")

    # left loop
    _arrow(ax, 2.2, 2.87, 2.2, 2.58, color=MUTED)
    _arrow(ax, 2.2, 2.02, 2.2, 1.78, color=MUTED)
    # loop back up
    ax.annotate("", xy=(5, 4.98), xytext=(1.0, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5,
                                connectionstyle="arc3,rad=-0.3"), zorder=5)
    ax.text(0.5, 3.3, "loop", color=ACCENT, fontsize=9, fontweight="bold",
            rotation=90)

    # right path down to end
    _arrow(ax, 7.8, 2.87, 7.8, 2.58, color=MUTED)
    _arrow(ax, 7.8, 2.02, 7.8, 1.78, color=MUTED)
    _arrow(ax, 7.8, 1.22, 7.8, 0.88, color=MUTED)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "activity_diagram.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[5/7] activity_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
# 6. ER DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
def fig_er_diagram():
    fig, ax = _setup_fig("ER Diagram — Database Schema", figsize=(14, 10))

    # ── Users table ────────────────────────────────────────────────────
    cols_users = [
        ("id",              "INTEGER   PK", ACCENT),
        ("username",        "TEXT UNIQUE",   TEXT),
        ("email",           "TEXT UNIQUE",   TEXT),
        ("password_hash",   "TEXT",          TEXT),
        ("created_at",      "DATETIME",      MUTED),
    ]
    table_x, table_y, col_w, row_h = 1.5, 7.5, 3.5, 0.5

    # Table header
    _rounded_box(ax, (table_x, table_y), col_w, 0.6, "users",
                 color=ACCENT, fontsize=13, radius=0.12)

    for i, (name, dtype, color) in enumerate(cols_users):
        ry = table_y - (i + 1) * row_h
        _rounded_box(ax, (table_x, ry), col_w, row_h, "",
                     color=DARK_BOX, alpha=0.8, radius=0.05, lw=1)
        # key icon for PK
        prefix = "PK " if "PK" in dtype else "    "
        ax.text(table_x + 0.15, ry + row_h / 2,
                f"{prefix}{name}", va="center", color=color,
                fontsize=10, fontfamily="monospace", zorder=4)
        ax.text(table_x + col_w - 0.15, ry + row_h / 2,
                dtype.replace(" PK", ""), va="center", ha="right",
                color=MUTED, fontsize=9, fontfamily="monospace", zorder=4)

    # ── Execution History (conceptual / in-memory) ─────────────────────
    cols_hist = [
        ("execution_id",  "UUID",      ACCENT),
        ("user_id",       "INTEGER FK", WARNING),
        ("module",        "TEXT",       TEXT),
        ("prompt",        "TEXT",       TEXT),
        ("target_url",    "TEXT",       TEXT),
        ("status",        "TEXT",       TEXT),
        ("result_data",   "JSON",       TEXT),
        ("started_at",    "DATETIME",   MUTED),
        ("completed_at",  "DATETIME",   MUTED),
    ]
    t2_x, t2_y, t2_w = 6.0, 7.5, 3.8
    _rounded_box(ax, (t2_x, t2_y), t2_w, 0.6, "execution_history",
                 color=WARNING, fontsize=12, radius=0.12)
    ax.text(t2_x + t2_w + 0.15, t2_y + 0.3, "(in-memory)",
            color=MUTED, fontsize=9, fontstyle="italic")

    for i, (name, dtype, color) in enumerate(cols_hist):
        ry = t2_y - (i + 1) * row_h
        _rounded_box(ax, (t2_x, ry), t2_w, row_h, "",
                     color=DARK_BOX, alpha=0.8, radius=0.05, lw=1)
        prefix = "FK " if "FK" in dtype else ("PK " if i == 0 else "    ")
        ax.text(t2_x + 0.15, ry + row_h / 2,
                f"{prefix}{name}", va="center", color=color,
                fontsize=10, fontfamily="monospace", zorder=4)
        ax.text(t2_x + t2_w - 0.15, ry + row_h / 2,
                dtype.replace(" FK", "").replace(" PK", ""),
                va="center", ha="right", color=MUTED, fontsize=9,
                fontfamily="monospace", zorder=4)

    # ── Relationship line (1:N) ────────────────────────────────────────
    rel_y = 6.5
    ax.plot([table_x + col_w, t2_x], [rel_y, rel_y],
            color=ACCENT, lw=2, zorder=3)
    ax.text(table_x + col_w + 0.15, rel_y + 0.15, "1",
            color=ACCENT, fontsize=12, fontweight="bold")
    ax.text(t2_x - 0.35, rel_y + 0.15, "N",
            color=WARNING, fontsize=12, fontweight="bold")
    ax.text((table_x + col_w + t2_x) / 2, rel_y + 0.2,
            "has many", color=MUTED, fontsize=9, ha="center",
            fontstyle="italic")

    # ── SQLite badge ───────────────────────────────────────────────────
    ax.text(5, 1.5, "SQLite  (auth.db)",
            ha="center", color=ACCENT, fontsize=14, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=DARK_BOX,
                      edgecolor=ACCENT, lw=2))
    ax.text(5, 0.9,
            "Users table stored in SQLite  |  Execution history tracked in-memory via SocketIO sessions",
            ha="center", color=MUTED, fontsize=10, fontstyle="italic")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "er_diagram.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[6/7] er_diagram.png")


# ═══════════════════════════════════════════════════════════════════════════
# 7. AGILE MODEL (SDLC)
# ═══════════════════════════════════════════════════════════════════════════
def fig_agile_model():
    fig, ax = _setup_fig("Agile SDLC Model — Iterative Sprints", figsize=(16, 10))

    # ── Central circle ─────────────────────────────────────────────────
    center_x, center_y = 5.5, 5.0
    ax.add_patch(plt.Circle((center_x, center_y), 0.9,
                            facecolor=DARK_BOX, edgecolor=ACCENT,
                            lw=2.5, zorder=3))
    ax.text(center_x, center_y + 0.15, "Agile", ha="center", va="center",
            color=ACCENT, fontsize=16, fontweight="bold", zorder=4)
    ax.text(center_x, center_y - 0.2, "Iterative", ha="center", va="center",
            color=MUTED, fontsize=11, zorder=4)

    # ── Phases arranged in a circle ────────────────────────────────────
    phases = [
        ("1. Requirements\nGathering",   SUCCESS,   90),
        ("2. Design &\nArchitecture",    SECONDARY, 30),
        ("3. Development\n(Sprint)",     ACCENT,    -30),
        ("4. Testing &\nQA",            WARNING,   -90),
        ("5. Review &\nFeedback",        PURPLE,    -150),
        ("6. Deployment\n& Release",     HIGHLIGHT, 150),
    ]
    radius = 3.2
    box_w, box_h = 2.2, 0.9

    for label, color, angle_deg in phases:
        angle = np.radians(angle_deg)
        px = center_x + radius * np.cos(angle)
        py = center_y + radius * np.sin(angle)
        _rounded_box(ax, (px - box_w / 2, py - box_h / 2), box_w, box_h,
                     label, color=color, fontsize=10, radius=0.15, alpha=0.9)
        # arrow from center outward
        inner_r = 1.0
        ix = center_x + inner_r * np.cos(angle)
        iy = center_y + inner_r * np.sin(angle)
        outer_r = radius - box_w / 2 - 0.15
        ox = center_x + outer_r * np.cos(angle)
        oy = center_y + outer_r * np.sin(angle)
        _arrow(ax, ix, iy, ox, oy, color=color, lw=1.8, style="-|>")

    # ── Curved arrows between phases (clockwise cycle) ─────────────────
    for i in range(len(phases)):
        a1 = np.radians(phases[i][2])
        a2 = np.radians(phases[(i + 1) % len(phases)][2])
        r_arc = radius + 0.6
        x1 = center_x + r_arc * np.cos(a1)
        y1 = center_y + r_arc * np.sin(a1)
        x2 = center_x + r_arc * np.cos(a2)
        y2 = center_y + r_arc * np.sin(a2)
        _arrow(ax, x1, y1, x2, y2, color=GRID, lw=1.2, style="-|>",
               connectionstyle="arc3,rad=-0.35")

    # ── Sprint details ─────────────────────────────────────────────────
    sprint_info = [
        "Sprint 1: Core Agent Framework + Claude Integration",
        "Sprint 2: Web Data Extraction Module",
        "Sprint 3: AI Form Filler Module + PDF Parsing",
        "Sprint 4: SocketIO Real-Time UI + Export Features",
        "Sprint 5: Auth, Testing & Deployment (Port 5050)",
    ]
    ax.text(11.5, 8.5, "Sprint Breakdown", color=TEXT, fontsize=12,
            fontweight="bold")
    for i, s in enumerate(sprint_info):
        ax.text(11.5, 7.8 - i * 0.55, s, color=MUTED, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=DARK_BOX,
                          edgecolor=GRID, lw=0.8))

    # ── Continuous loop label ──────────────────────────────────────────
    ax.text(center_x, center_y - 4.2,
            "Continuous Integration  |  Continuous Feedback  |  Continuous Delivery",
            ha="center", color=ACCENT, fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BOX,
                      edgecolor=ACCENT, lw=1.5))

    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(0, 10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "agile_model.png"),
                dpi=200, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("[7/7] agile_model.png")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Saving figures to: {FIGURES_DIR}\n")
    fig_system_architecture()
    fig_use_case_diagram()
    fig_class_diagram()
    fig_sequence_diagram()
    fig_activity_diagram()
    fig_er_diagram()
    fig_agile_model()
    print(f"\nAll 7 figures generated in {FIGURES_DIR}/")
