#!/usr/bin/env python3
"""
Generate 10 app screenshot mockups for the B12 AI Medical Chatbot project.
Uses matplotlib to create realistic chat interface and landing page mockups.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patheffects as pe
import numpy as np
import os

OUT_DIR = "/Users/shoukathali/lord-major-projects/IV-B Projects/IV-B Projects/B12/figures"
os.makedirs(OUT_DIR, exist_ok=True)

BLUE_DARK    = "#00527a"
BLUE_LIGHT   = "#00b8d4"
CHAT_BG_TOP  = "#f5f7fa"
CHAT_BG_BOT  = "#c3cfe2"
BOT_BUBBLE   = "#ececec"
USER_BUBBLE  = "#579ffb"
HEADER_BG    = "#eeeeee"
HEADER_TEXT   = "#666666"
SEND_GREEN   = (0/255, 196/255, 65/255)
WHITE        = "#ffffff"
BLACK        = "#333333"
DARK_TEXT     = "#222222"
LIGHT_TEXT    = "#888888"
TIMESTAMP_CLR = "#aaaaaa"
DPI = 200

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def draw_gradient(ax, color_top, color_bottom):
    c_top = np.array(hex_to_rgb(color_top))
    c_bot = np.array(hex_to_rgb(color_bottom))
    gradient = np.linspace(c_top, c_bot, 256).reshape(256, 1, 3)
    ax.imshow(gradient, aspect='auto', extent=ax.get_xlim() + ax.get_ylim(), origin='upper', zorder=0)

def draw_bubble(ax, x, y, width, height, color, radius=0.15):
    fancy = FancyBboxPatch((x, y), width, height, boxstyle=f"round,pad=0,rounding_size={radius}", facecolor=color, edgecolor='none', zorder=2)
    ax.add_patch(fancy)
    return fancy

def draw_bot_avatar(ax, cx, cy, r=0.22):
    ax.add_patch(Circle((cx, cy), r, facecolor='#4fc3f7', edgecolor='#0288d1', linewidth=1.2, zorder=3))
    eye_r = r * 0.15
    ax.add_patch(Circle((cx - r*0.3, cy + r*0.15), eye_r, fc='white', ec='none', zorder=4))
    ax.add_patch(Circle((cx + r*0.3, cy + r*0.15), eye_r, fc='white', ec='none', zorder=4))
    ax.plot([cx, cx], [cy + r, cy + r + r*0.45], color='#0288d1', lw=1.2, zorder=4)
    ax.add_patch(Circle((cx, cy + r + r*0.45), r*0.12, fc='#0288d1', ec='none', zorder=4))
    mouth_x = np.linspace(cx - r*0.3, cx + r*0.3, 20)
    mouth_y = cy - r*0.2 - 0.03 * np.sin(np.linspace(0, np.pi, 20))
    ax.plot(mouth_x, mouth_y, color='white', lw=1, zorder=4)

def draw_user_avatar(ax, cx, cy, r=0.22):
    ax.add_patch(Circle((cx, cy), r, facecolor='#90a4ae', edgecolor='#607d8b', linewidth=1.2, zorder=3))
    ax.add_patch(Circle((cx, cy + r*0.2), r*0.35, fc='#cfd8dc', ec='none', zorder=4))
    body = mpatches.Arc((cx, cy - r*0.6), r*0.9, r*0.7, angle=0, theta1=0, theta2=180, color='#cfd8dc', lw=1.5, zorder=4)
    ax.add_patch(body)

def create_chat_figure(fig_width=5.0, fig_height_inches=9.0):
    fig, ax = plt.subplots(figsize=(fig_width, fig_height_inches))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 18 * (fig_height_inches / 9.0))
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax

def draw_chat_bg(ax):
    draw_gradient(ax, CHAT_BG_TOP, CHAT_BG_BOT)

def draw_chat_header(ax, title="Medical-chatbot", y_top=None):
    if y_top is None:
        y_top = ax.get_ylim()[1]
    header_h = 1.1
    header = FancyBboxPatch((0, y_top - header_h), 10, header_h, boxstyle="square,pad=0", facecolor=HEADER_BG, edgecolor='#cccccc', linewidth=0.5, zorder=5)
    ax.add_patch(header)
    ax.text(0.5, y_top - header_h/2, '<', fontsize=14, color=HEADER_TEXT, ha='center', va='center', zorder=6, fontweight='bold')
    draw_bot_avatar(ax, 1.5, y_top - header_h/2, r=0.3)
    ax.text(2.3, y_top - header_h/2 + 0.05, title, fontsize=9, color=HEADER_TEXT, ha='left', va='center', zorder=6, fontweight='bold', fontfamily='sans-serif')
    ax.add_patch(Circle((2.3, y_top - header_h/2 - 0.28), 0.06, fc='#4caf50', ec='none', zorder=6))
    ax.text(2.55, y_top - header_h/2 - 0.28, 'Online', fontsize=5, color='#4caf50', ha='left', va='center', zorder=6)
    return y_top - header_h

def draw_input_bar(ax, y_bottom=0, text="Type a message..."):
    bar_h = 1.0
    bar = FancyBboxPatch((0, y_bottom), 10, bar_h, boxstyle="square,pad=0", facecolor='#fafafa', edgecolor='#dddddd', linewidth=0.5, zorder=5)
    ax.add_patch(bar)
    field = FancyBboxPatch((0.4, y_bottom + 0.2), 7.6, 0.6, boxstyle="round,pad=0,rounding_size=0.25", facecolor=WHITE, edgecolor='#cccccc', linewidth=0.5, zorder=6)
    ax.add_patch(field)
    ax.text(0.8, y_bottom + 0.5, text, fontsize=6.5, color='#aaa', ha='left', va='center', zorder=7, fontstyle='italic', fontfamily='sans-serif')
    send_btn = Circle((9.1, y_bottom + 0.5), 0.3, facecolor=SEND_GREEN, edgecolor='none', zorder=6)
    ax.add_patch(send_btn)
    ax.text(9.1, y_bottom + 0.52, '>', fontsize=10, color='white', ha='center', va='center', zorder=7, fontweight='bold')
    return y_bottom + bar_h

def _wrap_text(text, max_chars=42):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if current and len(current) + 1 + len(w) > max_chars:
            lines.append(current)
            current = w
        else:
            current = current + " " + w if current else w
    if current:
        lines.append(current)
    return lines if lines else [""]

def draw_bot_message(ax, y, text, max_width=6.0, fontsize=6.5, show_avatar=True, timestamp="10:30 AM"):
    lines = _wrap_text(text, max_chars=int(max_width * 6.5))
    line_h = 0.35
    padding = 0.25
    bubble_h = len(lines) * line_h + 2 * padding
    bubble_w = min(max_width, max(len(l) for l in lines) * 0.125 + 2 * padding + 0.3)
    bubble_w = max(bubble_w, 1.8)
    bx = 1.2 if show_avatar else 0.5
    by = y - bubble_h
    draw_bubble(ax, bx, by, bubble_w, bubble_h, BOT_BUBBLE)
    for i, line in enumerate(lines):
        ax.text(bx + padding, by + bubble_h - padding - i * line_h - 0.05, line, fontsize=fontsize, color=DARK_TEXT, ha='left', va='top', zorder=3, fontfamily='sans-serif')
    ax.text(bx + bubble_w + 0.15, by + 0.05, timestamp, fontsize=4, color=TIMESTAMP_CLR, ha='left', va='bottom', zorder=3)
    if show_avatar:
        draw_bot_avatar(ax, 0.6, by + bubble_h / 2, r=0.22)
    return by - 0.25

def draw_user_message(ax, y, text, max_width=5.5, fontsize=6.5, show_avatar=True, timestamp="10:31 AM"):
    lines = _wrap_text(text, max_chars=int(max_width * 6.0))
    line_h = 0.35
    padding = 0.25
    bubble_h = len(lines) * line_h + 2 * padding
    bubble_w = min(max_width, max(len(l) for l in lines) * 0.125 + 2 * padding + 0.3)
    bubble_w = max(bubble_w, 1.5)
    bx = 8.8 - bubble_w if show_avatar else 9.5 - bubble_w
    by = y - bubble_h
    draw_bubble(ax, bx, by, bubble_w, bubble_h, USER_BUBBLE)
    for i, line in enumerate(lines):
        ax.text(bx + padding, by + bubble_h - padding - i * line_h - 0.05, line, fontsize=fontsize, color=WHITE, ha='left', va='top', zorder=3, fontfamily='sans-serif')
    ax.text(bx - 0.15, by + 0.05, timestamp, fontsize=4, color=TIMESTAMP_CLR, ha='right', va='bottom', zorder=3)
    if show_avatar:
        draw_user_avatar(ax, 9.4, by + bubble_h / 2, r=0.22)
    return by - 0.25

def fig_7_1_landing():
    fig, ax = plt.subplots(figsize=(5.0, 9.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 18); ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    draw_gradient(ax, BLUE_DARK, BLUE_LIGHT)
    ax.text(5, 15.5, "MEDICAL", fontsize=28, color=WHITE, ha='center', va='center', fontweight='bold', zorder=2, fontfamily='sans-serif', path_effects=[pe.withStroke(linewidth=1, foreground='#003d5c')])
    ax.text(5, 14.5, "CHATBOT", fontsize=28, color=WHITE, ha='center', va='center', fontweight='bold', zorder=2, fontfamily='sans-serif', path_effects=[pe.withStroke(linewidth=1, foreground='#003d5c')])
    ax.text(5, 13.3, "Personal care for your healthy living", fontsize=10, color='#b2ebf2', ha='center', va='center', zorder=2, fontfamily='sans-serif', fontstyle='italic')
    desc = "An intelligent medical chatbot that uses AI\nto help diagnose diseases based on your\nsymptoms and provide medical guidance."
    ax.text(5, 12.0, desc, fontsize=7, color='#e0f7fa', ha='center', va='center', zorder=2, fontfamily='sans-serif', linespacing=1.6)
    doc_cx, doc_cy = 7.0, 7.5
    ax.add_patch(FancyBboxPatch((doc_cx - 1.2, doc_cy - 3.0), 2.4, 4.0, boxstyle="round,pad=0,rounding_size=0.3", facecolor='#e0f7fa', edgecolor='none', alpha=0.25, zorder=2))
    ax.add_patch(Circle((doc_cx, doc_cy + 1.8), 0.8, fc='#e0f7fa', ec='none', alpha=0.3, zorder=2))
    theta = np.linspace(0, np.pi, 30)
    ax.plot(doc_cx + 0.6 * np.cos(theta), doc_cy + 0.3 + 0.6 * np.sin(theta), color='#80deea', lw=2, alpha=0.5, zorder=2)
    cross_cx, cross_cy = 3.0, 7.5; cross_arm = 0.35; cross_len = 1.2
    ax.add_patch(FancyBboxPatch((cross_cx - cross_arm, cross_cy - cross_len), cross_arm*2, cross_len*2, boxstyle="round,pad=0,rounding_size=0.1", fc='#e0f7fa', ec='none', alpha=0.2, zorder=2))
    ax.add_patch(FancyBboxPatch((cross_cx - cross_len, cross_cy - cross_arm), cross_len*2, cross_arm*2, boxstyle="round,pad=0,rounding_size=0.1", fc='#e0f7fa', ec='none', alpha=0.2, zorder=2))
    for (dcx, dcy, dr, da) in [(1.5,15,0.4,0.1),(8.5,16,0.3,0.08),(1,5,0.5,0.07),(9,4,0.35,0.09),(2,10,0.2,0.12),(8,11,0.25,0.1)]:
        ax.add_patch(Circle((dcx, dcy), dr, fc='white', ec='none', alpha=da, zorder=1))
    btn_w, btn_h = 3.2, 0.9
    ax.add_patch(FancyBboxPatch((5 - btn_w/2, 3.5), btn_w, btn_h, boxstyle="round,pad=0,rounding_size=0.35", facecolor='#ffffff', edgecolor='none', zorder=3))
    ax.text(5, 3.95, "Chat Now", fontsize=12, color=BLUE_DARK, ha='center', va='center', fontweight='bold', zorder=4, fontfamily='sans-serif')
    pulse_x = np.linspace(2, 8, 200)
    pulse_y = 2.5 + 0.3 * np.exp(-((pulse_x - 4.5)**2)/0.1) * np.sin(30*(pulse_x - 4.5))
    ax.plot(pulse_x, pulse_y, color='#80deea', lw=1.5, alpha=0.4, zorder=2)
    ax.text(5, 1.2, "Powered by AI  |  NLP  |  Machine Learning", fontsize=6, color='#b2ebf2', ha='center', va='center', zorder=2, fontfamily='sans-serif', alpha=0.7)
    path = os.path.join(OUT_DIR, "fig_7_1_landing.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_2_greeting():
    fig, ax = create_chat_figure(5.0, 9.0); draw_chat_bg(ax)
    y = draw_chat_header(ax, y_top=ax.get_ylim()[1]); draw_input_bar(ax)
    greeting = "Hello, my name is Medical-chatbot, and I will be happy to help diagnose your disease. To start, we need to ask some basic questions, tap OK to continue!"
    y = draw_bot_message(ax, y - 0.5, greeting, timestamp="10:00 AM")
    path = os.path.join(OUT_DIR, "fig_7_2_greeting.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_3_demographics():
    fig, ax = create_chat_figure(5.0, 9.0); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "What is your name?", timestamp="10:01 AM")
    y = draw_user_message(ax, y, "Ahmed", timestamp="10:01 AM")
    y = draw_bot_message(ax, y, "How old are you?", timestamp="10:01 AM")
    y = draw_user_message(ax, y, "25", timestamp="10:02 AM")
    y = draw_bot_message(ax, y, "Can you specify your gender?", timestamp="10:02 AM")
    y = draw_user_message(ax, y, "Male", timestamp="10:02 AM")
    y = draw_bot_message(ax, y, "Well, Hello again Mr Ahmed, I hope you are feeling well today. Let's start the diagnosis process.", timestamp="10:02 AM")
    path = os.path.join(OUT_DIR, "fig_7_3_demographics.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_4_symptom_input():
    fig, ax = create_chat_figure(5.5, 9.5); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "Can you precise your main symptom Mr Ahmed?", timestamp="10:03 AM")
    y = draw_user_message(ax, y, "I have a bad headache", timestamp="10:03 AM")
    y = draw_bot_message(ax, y, "You are experiencing headache, correct?", timestamp="10:03 AM")
    nlp_y = y - 0.1
    nlp_box = FancyBboxPatch((1.2, nlp_y - 0.7), 5.5, 0.6, boxstyle="round,pad=0,rounding_size=0.15", facecolor='#fff9c4', edgecolor='#f9a825', linewidth=0.5, alpha=0.85, zorder=4)
    ax.add_patch(nlp_box)
    ax.text(1.5, nlp_y - 0.4, 'NLP Processing: "bad headache" -> headache', fontsize=5.5, color='#e65100', ha='left', va='center', zorder=5, fontfamily='sans-serif')
    y = nlp_y - 0.9
    y = draw_user_message(ax, y, "yes", timestamp="10:04 AM")
    y = draw_bot_message(ax, y, "Great, let me check for related symptoms...", timestamp="10:04 AM")
    path = os.path.join(OUT_DIR, "fig_7_4_symptom_input.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_5_followup():
    fig, ax = create_chat_figure(5.5, 9.5); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "Are you experiencing high_fever?", timestamp="10:05 AM")
    y = draw_user_message(ax, y, "yes", timestamp="10:05 AM")
    y = draw_bot_message(ax, y, "Are you experiencing vomiting?", timestamp="10:05 AM")
    y = draw_user_message(ax, y, "yes", timestamp="10:06 AM")
    y = draw_bot_message(ax, y, "Are you experiencing chills?", timestamp="10:06 AM")
    y = draw_user_message(ax, y, "no", timestamp="10:06 AM")
    y = draw_bot_message(ax, y, "Are you experiencing sweating?", timestamp="10:07 AM")
    y = draw_user_message(ax, y, "yes", timestamp="10:07 AM")
    y = draw_bot_message(ax, y, "Are you experiencing muscle_pain?", timestamp="10:07 AM")
    y = draw_user_message(ax, y, "yes", timestamp="10:08 AM")
    path = os.path.join(OUT_DIR, "fig_7_5_followup.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_6_prediction():
    fig, ax = create_chat_figure(5.5, 9.5); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "Analyzing your symptoms...", timestamp="10:09 AM")
    bar_y = y - 0.05
    ax.add_patch(FancyBboxPatch((1.2, bar_y - 0.35), 5.0, 0.3, boxstyle="round,pad=0,rounding_size=0.12", facecolor='#e0e0e0', edgecolor='none', zorder=3))
    ax.add_patch(FancyBboxPatch((1.2, bar_y - 0.35), 5.0, 0.3, boxstyle="round,pad=0,rounding_size=0.12", facecolor='#4caf50', edgecolor='none', zorder=4))
    ax.text(3.7, bar_y - 0.2, "100% Complete", fontsize=5, color='white', ha='center', va='center', zorder=5, fontweight='bold')
    y = bar_y - 0.6
    result_h = 1.6
    ax.add_patch(FancyBboxPatch((0.8, y - result_h), 8.4, result_h, boxstyle="round,pad=0,rounding_size=0.2", facecolor='#e8f5e9', edgecolor='#4caf50', linewidth=1.5, zorder=3))
    ax.text(5, y - 0.35, "Disease Prediction Result", fontsize=8, color='#2e7d32', ha='center', va='center', fontweight='bold', zorder=4, fontfamily='sans-serif')
    ax.text(5, y - 0.75, "Based on your symptoms, you may have:", fontsize=6.5, color='#555', ha='center', va='center', zorder=4)
    ax.text(5, y - 1.15, "MALARIA", fontsize=14, color='#d32f2f', ha='center', va='center', fontweight='bold', zorder=4, fontfamily='sans-serif')
    y = y - result_h - 0.3
    y = draw_bot_message(ax, y, "Based on your symptoms, you may have Malaria. Tap D to get a description of the disease and precautions to take.", timestamp="10:09 AM")
    path = os.path.join(OUT_DIR, "fig_7_6_prediction.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_7_description():
    fig, ax = create_chat_figure(5.5, 9.5); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_user_message(ax, y - 0.4, "D", timestamp="10:10 AM")
    y = draw_bot_message(ax, y, "Disease: Malaria", timestamp="10:10 AM", fontsize=7)
    y = draw_bot_message(ax, y, "Description: Malaria is a life-threatening disease caused by parasites that are transmitted to people through the bites of infected female Anopheles mosquitoes. It is preventable and curable. The symptoms usually appear 10-15 days after the infective mosquito bite.", timestamp="10:10 AM", show_avatar=True)
    y = draw_bot_message(ax, y, "Medication: Chloroquine, Artemisinin-based combination therapies (ACTs), Quinine sulfate. Please consult a healthcare professional for proper medication and dosage.", timestamp="10:10 AM", show_avatar=True)
    path = os.path.join(OUT_DIR, "fig_7_7_description.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_8_severity():
    fig, ax = create_chat_figure(5.0, 9.0); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "How many days have you been experiencing these symptoms?", timestamp="10:12 AM")
    y = draw_user_message(ax, y, "5", timestamp="10:12 AM")
    sev_h = 1.1
    ax.add_patch(FancyBboxPatch((0.8, y - sev_h - 0.1), 8.4, sev_h, boxstyle="round,pad=0,rounding_size=0.2", facecolor='#fff3e0', edgecolor='#ff9800', linewidth=1.2, zorder=3))
    ax.text(5, y - 0.4, "Severity Assessment", fontsize=8, color='#e65100', ha='center', va='center', fontweight='bold', zorder=4, fontfamily='sans-serif')
    ax.text(5, y - 0.8, "Severity Level: MODERATE-HIGH", fontsize=7, color='#bf360c', ha='center', va='center', fontweight='bold', zorder=4)
    y = y - sev_h - 0.4
    y = draw_bot_message(ax, y, "Your condition is concerning. You should take consultation from a doctor, preferably an Infectious Disease Specialist.", timestamp="10:12 AM")
    y = draw_bot_message(ax, y, "Recommended specialist: Infectious Disease Specialist. Please visit your nearest hospital as soon as possible.", timestamp="10:12 AM")
    path = os.path.join(OUT_DIR, "fig_7_8_severity.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_9_precautions():
    fig, ax = create_chat_figure(5.0, 9.0); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "Here are some precautions you should follow:", timestamp="10:14 AM")
    precautions = ["1. Consult nearest hospital", "2. Avoid oily food", "3. Avoid non veg food", "4. Keep mosquito nets around your bed"]
    card_h = 3.2; card_x = 1.2
    ax.add_patch(FancyBboxPatch((card_x, y - card_h), 7.0, card_h, boxstyle="round,pad=0,rounding_size=0.2", facecolor=BOT_BUBBLE, edgecolor='#d0d0d0', linewidth=0.8, zorder=2))
    ax.text(card_x + 0.4, y - 0.35, "Precautions for Malaria", fontsize=7, color='#1565c0', ha='left', va='center', fontweight='bold', zorder=3, fontfamily='sans-serif')
    ax.plot([card_x + 0.3, card_x + 6.7], [y - 0.6, y - 0.6], color='#ccc', lw=0.5, zorder=3)
    for i, p in enumerate(precautions):
        py = y - 0.9 - i * 0.55
        ax.add_patch(Circle((card_x + 0.55, py), 0.12, fc='#4caf50', ec='none', zorder=3))
        ax.text(card_x + 0.55, py, str(i+1), fontsize=5, color='white', ha='center', va='center', zorder=4, fontweight='bold')
        ax.text(card_x + 0.85, py, p[3:], fontsize=6.5, color=DARK_TEXT, ha='left', va='center', zorder=3, fontfamily='sans-serif')
    draw_bot_avatar(ax, 0.6, y - card_h/2, r=0.22)
    y = y - card_h - 0.3
    ax.text(card_x + 7.15, y + 0.35, "10:14 AM", fontsize=4, color=TIMESTAMP_CLR, ha='left', va='bottom', zorder=3)
    y = draw_bot_message(ax, y, "Remember to take your prescribed medication regularly and stay hydrated. Get plenty of rest.", timestamp="10:14 AM", show_avatar=True)
    path = os.path.join(OUT_DIR, "fig_7_9_precautions.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

def fig_7_10_restart():
    fig, ax = create_chat_figure(3.0, 9.0); draw_chat_bg(ax)
    y = draw_chat_header(ax); draw_input_bar(ax)
    y = draw_bot_message(ax, y - 0.4, "Do you need another medical consultation (yes or no)?", max_width=7.5, timestamp="10:16 AM")
    y = draw_user_message(ax, y, "no", timestamp="10:16 AM")
    farewell_h = 1.4
    ax.add_patch(FancyBboxPatch((0.8, y - farewell_h), 8.4, farewell_h, boxstyle="round,pad=0,rounding_size=0.2", facecolor='#e3f2fd', edgecolor='#42a5f5', linewidth=1.2, zorder=3))
    ax.text(5, y - 0.45, "THANKS Mr Ahmed, take care!", fontsize=8, color='#1565c0', ha='center', va='center', fontweight='bold', zorder=4, fontfamily='sans-serif')
    ax.text(5, y - 0.9, "Stay healthy and don't hesitate to come back!", fontsize=6, color='#555', ha='center', va='center', zorder=4, fontfamily='sans-serif')
    draw_bot_avatar(ax, 0.4, y - farewell_h/2, r=0.2)
    path = os.path.join(OUT_DIR, "fig_7_10_restart.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0); plt.close(fig)
    print(f"  Saved {path}")

if __name__ == "__main__":
    print("Generating B12 AI Medical Chatbot screenshot mockups...\n")
    generators = [
        ("Fig 7.1  - Landing Page",              fig_7_1_landing),
        ("Fig 7.2  - Initial Greeting",           fig_7_2_greeting),
        ("Fig 7.3  - Demographics Collection",    fig_7_3_demographics),
        ("Fig 7.4  - Symptom Input",              fig_7_4_symptom_input),
        ("Fig 7.5  - Follow-up Questions",        fig_7_5_followup),
        ("Fig 7.6  - Disease Prediction",         fig_7_6_prediction),
        ("Fig 7.7  - Disease Description",        fig_7_7_description),
        ("Fig 7.8  - Severity Assessment",        fig_7_8_severity),
        ("Fig 7.9  - Precaution Recommendations", fig_7_9_precautions),
        ("Fig 7.10 - Restart / New Consultation", fig_7_10_restart),
    ]
    for label, func in generators:
        print(f"[*] {label}")
        func()
    print(f"\nAll 10 screenshots saved to:\n  {OUT_DIR}/")
    print("Done.")
