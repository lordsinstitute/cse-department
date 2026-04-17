#!/usr/bin/env python3
"""
Generate architecture and analysis figures for the B3 Resume Builder project report.
Saves all figures to ../figures/ directory.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Color palette
DARK_BG = '#1a1a2e'
CARD_BG = '#1f1f3a'
ACCENT = '#ffc107'
BLUE = '#3498db'
NAVY = '#2c3e50'
TEAL = '#0f766e'
GREEN = '#27ae60'
RED = '#e74c3c'
PURPLE = '#8e44ad'
ORANGE = '#e67e22'
LIGHT_BLUE = '#5dade2'


def save_fig(fig, name):
    path = os.path.join(FIGURES_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {name}.png")


def fig_system_architecture():
    """Two-panel architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('System Architecture — Two-Panel Layout', fontsize=16, fontweight='bold', pad=15)

    # Browser container
    browser = FancyBboxPatch((0.3, 0.3), 9.4, 7.2, boxstyle="round,pad=0.1",
                              facecolor='#f0f0f0', edgecolor=NAVY, linewidth=2)
    ax.add_patch(browser)
    ax.text(5, 7.7, 'Browser (index.html)', ha='center', fontsize=13, fontweight='bold', color=NAVY)

    # Navbar
    navbar = FancyBboxPatch((0.5, 6.8), 9, 0.6, boxstyle="round,pad=0.05",
                             facecolor=DARK_BG, edgecolor='#333')
    ax.add_patch(navbar)
    ax.text(5, 7.1, 'Navbar: ResumeForge  |  ATS  |  Undo/Redo  |  Save  |  JSON  |  PDF',
            ha='center', fontsize=9, color=ACCENT, fontweight='bold')

    # Editor Panel
    editor = FancyBboxPatch((0.5, 0.5), 3.5, 6, boxstyle="round,pad=0.1",
                             facecolor=CARD_BG, edgecolor='#444', linewidth=1.5)
    ax.add_patch(editor)
    ax.text(2.25, 6.2, 'Editor Panel', ha='center', fontsize=12, fontweight='bold', color=ACCENT)

    sections = ['Personal Info (10 fields)', 'Work Experience', 'Education',
                'Skills + Proficiency', 'Projects', 'Certifications', 'Awards', 'ATS Checker']
    for i, s in enumerate(sections):
        y = 5.6 - i * 0.65
        box = FancyBboxPatch((0.7, y - 0.2), 3.1, 0.5, boxstyle="round,pad=0.05",
                              facecolor='#2a2a4a', edgecolor='#555')
        ax.add_patch(box)
        ax.text(2.25, y + 0.05, s, ha='center', fontsize=8, color='#e0e0e0')

    # Preview Panel
    preview = FancyBboxPatch((4.3, 0.5), 5.2, 6, boxstyle="round,pad=0.1",
                              facecolor='white', edgecolor='#ccc', linewidth=1.5)
    ax.add_patch(preview)
    ax.text(6.9, 6.2, 'Live Preview Panel', ha='center', fontsize=12, fontweight='bold', color=NAVY)

    # Template tabs
    templates = ['Professional', 'Modern', 'Minimal', 'Creative', 'Executive']
    for i, t in enumerate(templates):
        x = 4.6 + i * 1.0
        colors = [NAVY, BLUE, '#666', TEAL, DARK_BG]
        box = FancyBboxPatch((x, 5.5), 0.9, 0.4, boxstyle="round,pad=0.03",
                              facecolor=colors[i], edgecolor='#999')
        ax.add_patch(box)
        ax.text(x + 0.45, 5.7, t, ha='center', fontsize=6, color='white', fontweight='bold')

    # Resume preview area
    resume = FancyBboxPatch((5.0, 0.8), 3.8, 4.5, boxstyle="round,pad=0.05",
                             facecolor='#fafafa', edgecolor='#ddd', linewidth=1)
    ax.add_patch(resume)
    ax.text(6.9, 4.8, 'A4 Resume Page (210mm x 297mm)', ha='center', fontsize=9, color='#666')

    resume_lines = ['John Doe', 'Software Developer', '---', 'Experience...', 'Education...', 'Skills...']
    for i, line in enumerate(resume_lines):
        ax.text(6.9, 4.3 - i * 0.55, line, ha='center', fontsize=8, color='#888', style='italic')

    # Arrow from editor to preview
    ax.annotate('', xy=(4.3, 3.5), xytext=(4.0, 3.5),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))
    ax.text(4.15, 3.8, 'Real-time\nUpdate', ha='center', fontsize=7, color=ACCENT, fontweight='bold')

    save_fig(fig, 'system_architecture')


def fig_data_flow():
    """Data flow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('Data Flow Diagram', fontsize=16, fontweight='bold', pad=15)

    boxes = [
        (0.3, 2, 'User Input\n(Form Fields)', BLUE),
        (2.3, 2, 'JavaScript\nState (resumeData)', NAVY),
        (4.3, 2, 'localStorage\n(Browser Storage)', GREEN),
        (6.3, 2, 'Live Preview\n(DOM Rendering)', PURPLE),
        (8.3, 2, 'Export\n(PDF / JSON)', RED),
    ]

    for x, y, text, color in boxes:
        box = FancyBboxPatch((x, y), 1.7, 1.2, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x + 0.85, y + 0.6, text, ha='center', va='center', fontsize=9,
                color='white', fontweight='bold')

    # Arrows
    for i in range(4):
        x1 = boxes[i][0] + 1.7
        x2 = boxes[i + 1][0]
        ax.annotate('', xy=(x2, 2.6), xytext=(x1, 2.6),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # Labels above arrows
    labels = ['onChange\nevent', 'saveToLocal()', 'updatePreview()', 'html2pdf.js\nexportJSON()']
    for i, label in enumerate(labels):
        x = (boxes[i][0] + 1.7 + boxes[i + 1][0]) / 2
        ax.text(x, 3.5, label, ha='center', fontsize=8, color='#555', style='italic')

    # Undo/Redo box
    undo = FancyBboxPatch((2.3, 0.3), 1.7, 0.8, boxstyle="round,pad=0.1",
                           facecolor=ORANGE, edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(undo)
    ax.text(3.15, 0.7, 'Undo/Redo\nStack (50 states)', ha='center', va='center',
            fontsize=8, color='white', fontweight='bold')
    ax.annotate('', xy=(3.15, 2.0), xytext=(3.15, 1.1),
                arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=1.5))

    save_fig(fig, 'data_flow')


def fig_ats_scoring():
    """ATS scoring breakdown bar chart."""
    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ['Personal Info', 'Experience', 'Education', 'Skills', 'Extras']
    max_scores = [30, 20, 15, 20, 15]
    details = ['Name, Email,\nPhone, Summary', '2+ Entries,\nDescriptions', 'At Least\n1 Entry',
               '5+ Skills\n= 20pts', 'Projects,\nCerts, Awards']
    colors = [BLUE, GREEN, PURPLE, ORANGE, TEAL]

    bars = ax.barh(categories, max_scores, color=colors, edgecolor='white', height=0.6)

    for bar, score, detail in zip(bars, max_scores, details):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{score} pts', va='center', fontsize=11, fontweight='bold')
        ax.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                detail, va='center', ha='center', fontsize=8, color='white')

    ax.set_xlabel('Maximum Points', fontsize=12)
    ax.set_title('ATS Compatibility Score Breakdown (Total: 100 Points)', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 38)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'ats_scoring')


def fig_template_comparison():
    """5 templates comparison chart."""
    fig, ax = plt.subplots(figsize=(9, 5))

    templates = ['Professional', 'Modern', 'Minimal', 'Creative', 'Executive']
    features = ['Centered\nHeader', 'Gradient\nBanner', 'Serif\nFonts', 'Two-Column\nLayout',
                'Skill\nBars', 'Section\nBorders', 'Color\nAccents']

    # Feature matrix (1 = has feature)
    matrix = np.array([
        [1, 0, 0, 0, 1, 1, 1],  # Professional
        [0, 1, 0, 0, 1, 1, 1],  # Modern
        [1, 0, 1, 0, 1, 0, 0],  # Minimal
        [0, 0, 0, 1, 1, 0, 1],  # Creative
        [1, 0, 1, 0, 1, 1, 1],  # Executive
    ])

    colors_map = [NAVY, BLUE, '#888', TEAL, DARK_BG]

    x = np.arange(len(features))
    width = 0.15

    for i, (template, color) in enumerate(zip(templates, colors_map)):
        offset = (i - 2) * width
        bars = ax.bar(x + offset, matrix[i], width, label=template, color=color, edgecolor='white')

    ax.set_xticks(x)
    ax.set_xticklabels(features, fontsize=9)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['No', 'Yes'])
    ax.set_title('Resume Template Feature Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'template_comparison')


def fig_technology_stack():
    """Technology stack layers diagram."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Technology Stack', fontsize=16, fontweight='bold', pad=15)

    layers = [
        (0.5, 5.5, 7, 1.0, 'Presentation Layer', 'HTML5 + CSS3 + Bootstrap 5 + Google Fonts', BLUE),
        (0.5, 4.2, 7, 1.0, 'Application Logic', 'JavaScript ES6 (app.js — 1,543 lines)', NAVY),
        (0.5, 2.9, 7, 1.0, 'Data Persistence', 'localStorage API + JSON Export/Import', GREEN),
        (0.5, 1.6, 7, 1.0, 'Export Layer', 'html2pdf.js (PDF) + Blob API (JSON)', PURPLE),
        (0.5, 0.3, 7, 1.0, 'AI Integration', 'Claude API (Anthropic) — Optional', ORANGE),
    ]

    for x, y, w, h, title, detail, color in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(4, y + 0.65, title, ha='center', va='center', fontsize=12,
                color='white', fontweight='bold')
        ax.text(4, y + 0.3, detail, ha='center', va='center', fontsize=9, color='#ddd')

    save_fig(fig, 'technology_stack')


def fig_user_flow():
    """User journey flowchart."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('User Journey Flowchart', fontsize=16, fontweight='bold', pad=15)

    steps = [
        (0.5, 2, 'Open\nindex.html', '#95a5a6'),
        (2.3, 2, 'Login /\nRegister', BLUE),
        (4.1, 2, 'Fill Resume\nSections', NAVY),
        (5.9, 2, 'Live\nPreview', PURPLE),
        (7.7, 2, 'Check ATS\nScore', ORANGE),
        (9.5, 2, 'Export\nPDF/JSON', GREEN),
    ]

    for x, y, text, color in steps:
        box = FancyBboxPatch((x, y), 1.5, 1.2, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x + 0.75, y + 0.6, text, ha='center', va='center', fontsize=10,
                color='white', fontweight='bold')

    for i in range(5):
        x1 = steps[i][0] + 1.5
        x2 = steps[i + 1][0]
        ax.annotate('', xy=(x2, 2.6), xytext=(x1, 2.6),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # Side actions
    side = [
        (4.1, 0.5, 'Save to\nlocalStorage', GREEN, 4.85, 2.0),
        (5.9, 4.0, 'Switch\nTemplate', TEAL, 6.65, 3.2),
        (7.7, 0.5, 'Grammar\nCheck', RED, 8.45, 2.0),
    ]

    for x, y, text, color, arrow_x, arrow_y in side:
        box = FancyBboxPatch((x, y), 1.5, 0.8, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='white', alpha=0.7)
        ax.add_patch(box)
        ax.text(x + 0.75, y + 0.4, text, ha='center', va='center', fontsize=8,
                color='white', fontweight='bold')
        ax.annotate('', xy=(arrow_x, arrow_y), xytext=(x + 0.75, y + 0.8 if y < 2 else y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5, ls='--'))

    save_fig(fig, 'user_flow')


def fig_feature_categories():
    """Feature categories pie chart."""
    fig, ax = plt.subplots(figsize=(8, 6))

    categories = ['Resume Editing\n(7 sections)', 'Templates\n(5 designs)', 'Data Management\n(Save/Export)',
                  'ATS Scoring', 'AI Suggestions', 'Undo/Redo\n& Grammar', 'Authentication']
    sizes = [30, 20, 15, 12, 10, 8, 5]
    colors = [BLUE, NAVY, GREEN, ORANGE, PURPLE, TEAL, RED]
    explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=categories,
                                       autopct='%1.0f%%', colors=colors,
                                       textprops={'fontsize': 9},
                                       pctdistance=0.75, startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title('Feature Distribution by Category', fontsize=14, fontweight='bold')

    save_fig(fig, 'feature_categories')


if __name__ == '__main__':
    print("Generating figures for B3 Resume Builder report...")
    fig_system_architecture()
    fig_data_flow()
    fig_ats_scoring()
    fig_template_comparison()
    fig_technology_stack()
    fig_user_flow()
    fig_feature_categories()
    print(f"\nAll figures saved to: {FIGURES_DIR}/")
