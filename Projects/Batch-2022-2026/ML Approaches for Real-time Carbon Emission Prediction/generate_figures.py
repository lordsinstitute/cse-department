#!/usr/bin/env python3
"""Generate UML and architecture diagrams for C6 Carbon Emission Prediction report."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(SAVE_DIR, exist_ok=True)

# Theme
BG = '#1a1a2e'
CARD = '#16213e'
ACCENT = '#10b981'
ACCENT2 = '#059669'
TEXT = '#eeeeee'
GRID = '#2a2a4a'
COLORS = ['#10b981', '#0f3460', '#e94560', '#00b4d8', '#e9c46a', '#2a9d8f',
          '#f4845f', '#7209b7', '#4cc9f0', '#fb8500']


def save_fig(fig, name):
    path = os.path.join(SAVE_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {name}")


def draw_box(ax, x, y, w, h, label, color=ACCENT, fontsize=9):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.15", facecolor=color,
                         edgecolor=TEXT, linewidth=1.2, alpha=0.85)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=fontsize,
            color='white', fontweight='bold', wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, color=TEXT):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))


# ── 1. System Architecture ──────────────────────────────────────────────
def system_architecture():
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('System Architecture', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    # Presentation tier
    ax.add_patch(FancyBboxPatch((0.5, 5.8), 11, 1.8, boxstyle="round,pad=0.2",
                                facecolor='#0f3460', edgecolor=ACCENT, linewidth=1.5, alpha=0.4))
    ax.text(6, 7.2, 'PRESENTATION TIER', ha='center', fontsize=11, color=ACCENT, fontweight='bold')
    for i, (lbl, clr) in enumerate([('Bootstrap 5\nDark Theme', '#0f3460'),
                                     ('Chart.js\nDashboard', '#533483'),
                                     ('Jinja2\nTemplates', '#0f3460'),
                                     ('Responsive\nUI Forms', '#533483')]):
        draw_box(ax, 2 + i * 2.5, 6.3, 1.8, 0.7, lbl, clr, 8)

    # Application tier
    ax.add_patch(FancyBboxPatch((0.5, 3.0), 11, 2.4, boxstyle="round,pad=0.2",
                                facecolor='#16213e', edgecolor=ACCENT, linewidth=1.5, alpha=0.4))
    ax.text(6, 5.0, 'APPLICATION TIER (Flask)', ha='center', fontsize=11, color=ACCENT, fontweight='bold')
    for i, (lbl, clr) in enumerate([('Auth\nModule', ACCENT2),
                                     ('Prediction\nEngine', '#e94560'),
                                     ('History\nManager', '#0f3460'),
                                     ('Dashboard\nAnalytics', '#533483')]):
        draw_box(ax, 2 + i * 2.5, 4.2, 1.8, 0.7, lbl, clr, 8)

    draw_box(ax, 3.5, 3.4, 2.5, 0.6, 'ML Pipeline\n(6 Regression Models)', '#e94560', 8)
    draw_box(ax, 8.5, 3.4, 2.5, 0.6, 'Preprocessing\n(LabelEncoder + Scaler)', ACCENT2, 8)

    # Data tier
    ax.add_patch(FancyBboxPatch((0.5, 0.4), 11, 2.2, boxstyle="round,pad=0.2",
                                facecolor='#1a1a2e', edgecolor=ACCENT, linewidth=1.5, alpha=0.4))
    ax.text(6, 2.2, 'DATA TIER', ha='center', fontsize=11, color=ACCENT, fontweight='bold')
    for i, (lbl, clr) in enumerate([('SQLite DB\n(users, predictions)', '#0f3460'),
                                     ('best_model.pkl\n(Random Forest)', '#e94560'),
                                     ('encoders.pkl\nscaler.pkl', ACCENT2),
                                     ('final_co2.csv\n(7,000 records)', '#533483')]):
        draw_box(ax, 2 + i * 2.5, 1.3, 1.8, 0.7, lbl, clr, 8)

    # Arrows between tiers
    for x in [2, 4.5, 7, 9.5]:
        draw_arrow(ax, x, 5.8, x, 5.5)
        draw_arrow(ax, x, 3.0, x, 2.7)

    save_fig(fig, 'system_architecture.png')


# ── 2. Use Case Diagram ─────────────────────────────────────────────────
def use_case_diagram():
    fig, ax = plt.subplots(figsize=(11, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Use Case Diagram', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    # System boundary
    ax.add_patch(FancyBboxPatch((3, 0.3), 5.5, 7.2, boxstyle="round,pad=0.3",
                                facecolor=CARD, edgecolor=ACCENT, linewidth=2, alpha=0.5))
    ax.text(5.75, 7.2, 'Carbon Emission Prediction System', ha='center',
            fontsize=12, color=ACCENT, fontweight='bold')

    # Actors
    for ay, lbl in [(5.5, 'Regular\nUser'), (2.5, 'Admin')]:
        ax.plot(1.5, ay + 0.3, 'o', color=ACCENT, markersize=12)
        ax.plot([1.5, 1.5], [ay + 0.15, ay - 0.1], color=ACCENT, lw=2)
        ax.plot([1.2, 1.8], [ay + 0.05, ay + 0.05], color=ACCENT, lw=2)
        ax.plot([1.5, 1.2], [ay - 0.1, ay - 0.35], color=ACCENT, lw=2)
        ax.plot([1.5, 1.8], [ay - 0.1, ay - 0.35], color=ACCENT, lw=2)
        ax.text(1.5, ay - 0.55, lbl, ha='center', va='top', fontsize=9, color=TEXT)

    # Use cases
    cases = [
        (5.75, 6.5, 'Register Account'),
        (5.75, 5.7, 'Login / Logout'),
        (5.75, 4.9, 'Predict CO₂ Emissions'),
        (5.75, 4.1, 'View Prediction History'),
        (5.75, 3.3, 'View Dashboard'),
        (5.75, 2.5, 'View About Page'),
        (5.75, 1.7, 'Manage All Users'),
        (5.75, 0.9, 'View All Predictions'),
    ]
    for cx, cy, label in cases:
        ellipse = mpatches.Ellipse((cx, cy), 3.5, 0.6, facecolor='#0f3460',
                                    edgecolor=ACCENT, linewidth=1.2, alpha=0.8)
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=9, color=TEXT, fontweight='bold')

    # User connections
    for cy in [6.5, 5.7, 4.9, 4.1, 3.3, 2.5]:
        draw_arrow(ax, 2.0, 5.5, 4.0, cy)
    # Admin connections
    for cy in [5.7, 3.3, 1.7, 0.9]:
        draw_arrow(ax, 2.0, 2.5, 4.0, cy)

    save_fig(fig, 'use_case_diagram.png')


# ── 3. Class Diagram ────────────────────────────────────────────────────
def class_diagram():
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Class Diagram', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    def draw_class(x, y, w, h, name, attrs, methods, color=ACCENT2):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                    facecolor=CARD, edgecolor=color, linewidth=1.5))
        # Title
        ax.add_patch(plt.Rectangle((x + 0.05, y + h - 0.45), w - 0.1, 0.4,
                                   facecolor=color, alpha=0.3))
        ax.text(x + w/2, y + h - 0.25, name, ha='center', va='center',
                fontsize=10, color=TEXT, fontweight='bold')
        # Attributes
        ay = y + h - 0.65
        for a in attrs:
            ax.text(x + 0.15, ay, a, fontsize=7, color='#aaaaaa', family='monospace')
            ay -= 0.22
        # Divider
        ax.plot([x + 0.1, x + w - 0.1], [ay + 0.05, ay + 0.05], color=color, lw=0.5, alpha=0.5)
        ay -= 0.1
        for m in methods:
            ax.text(x + 0.15, ay, m, fontsize=7, color=ACCENT, family='monospace')
            ay -= 0.22

    # FlaskApp
    draw_class(0.3, 5.5, 3.5, 3.2, 'FlaskApp',
               ['- app: Flask', '- secret_key: str', '- db_path: str'],
               ['+ init_db()', '+ login_required(f)', '+ index()', '+ login()',
                '+ register()', '+ predict()', '+ history()', '+ dashboard()'],
               ACCENT)

    # MLPipeline
    draw_class(4.5, 5.5, 3.2, 3.2, 'MLPipeline',
               ['- model: RandomForest', '- encoders: dict', '- scaler: StandardScaler',
                '- models_info: dict'],
               ['+ load_model()', '+ preprocess(data)', '+ predict(features)',
                '+ get_co2_rating(co2)', '+ get_metrics()'],
               '#e94560')

    # User model
    draw_class(0.3, 2.0, 3.5, 2.8, 'User',
               ['+ id: int PK', '+ username: str UNIQUE', '+ password: str (hash)',
                '+ name: str', '+ role: str'],
               ['+ register()', '+ authenticate()', '+ is_admin()'],
               '#0f3460')

    # Prediction model
    draw_class(4.5, 2.0, 3.2, 2.8, 'Prediction',
               ['+ id: int PK', '+ user_id: int FK', '+ input_data: json',
                '+ predicted_co2: float', '+ co2_rating: int', '+ pred_date: str'],
               ['+ save()', '+ get_by_user()', '+ get_all()'],
               '#533483')

    # DataProcessor
    draw_class(8.5, 5.5, 3.2, 3.2, 'DataProcessor',
               ['- label_encoders: dict', '- standard_scaler: obj',
                '- features: list[9]', '- target: CO2_Emissions'],
               ['+ encode_categorical()', '+ scale_numeric()',
                '+ transform(input)', '+ inverse_transform()'],
               '#e9c46a')

    # TrainingEngine
    draw_class(8.5, 2.0, 3.2, 2.8, 'TrainingEngine',
               ['- models: dict[6]', '- X_train, X_test', '- y_train, y_test',
                '- best_model: str'],
               ['+ train_all()', '+ evaluate()', '+ save_best()',
                '+ export_metrics()'],
               '#00b4d8')

    # Relationships
    draw_arrow(ax, 3.8, 7.0, 4.5, 7.0)
    draw_arrow(ax, 7.7, 7.0, 8.5, 7.0)
    draw_arrow(ax, 2.0, 5.5, 2.0, 4.8)
    draw_arrow(ax, 6.0, 5.5, 6.0, 4.8)
    draw_arrow(ax, 7.7, 3.5, 8.5, 3.5)
    ax.text(4.15, 7.15, 'uses', fontsize=7, color='#888888', style='italic')
    ax.text(8.05, 7.15, 'uses', fontsize=7, color='#888888', style='italic')
    ax.text(2.15, 5.1, '1..*', fontsize=7, color='#888888')

    save_fig(fig, 'class_diagram.png')


# ── 4. Sequence Diagram ─────────────────────────────────────────────────
def sequence_diagram():
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Sequence Diagram — CO₂ Prediction Flow', color=TEXT,
                 fontsize=16, fontweight='bold', pad=15)

    actors = [('User', 1.5), ('Browser', 3.5), ('Flask App', 5.5),
              ('ML Pipeline', 7.5), ('SQLite DB', 9.5)]
    for name, x in actors:
        draw_box(ax, x, 8.3, 1.5, 0.5, name, ACCENT2 if name != 'User' else ACCENT, 9)
        ax.plot([x, x], [8.05, 0.5], color='#444466', lw=1, linestyle='--')

    messages = [
        (1.5, 3.5, 7.5, 'Fill prediction form', True),
        (3.5, 5.5, 7.0, 'POST /predict (9 features)', True),
        (5.5, 7.5, 6.5, 'preprocess(input_data)', True),
        (7.5, 5.5, 6.0, 'encoded + scaled features', False),
        (5.5, 7.5, 5.5, 'model.predict(features)', True),
        (7.5, 5.5, 5.0, 'CO₂ = 185.3 g/km', False),
        (5.5, 5.5, 4.5, 'get_co2_rating(185.3) → 7', True),
        (5.5, 9.5, 4.0, 'INSERT prediction', True),
        (9.5, 5.5, 3.5, 'OK (saved)', False),
        (5.5, 3.5, 3.0, 'render result.html', False),
        (3.5, 1.5, 2.5, 'Display result + rating', False),
    ]

    for src, dst, y, msg, is_req in messages:
        style = '->' if is_req else '->'
        color = ACCENT if is_req else '#e94560'
        ls = '-' if is_req else '--'
        ax.annotate('', xy=(dst, y), xytext=(src, y),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.2, linestyle=ls))
        mid = (src + dst) / 2
        ax.text(mid, y + 0.15, msg, ha='center', fontsize=7, color=TEXT,
                style='italic' if not is_req else 'normal')

    save_fig(fig, 'sequence_diagram.png')


# ── 5. Activity Diagram ─────────────────────────────────────────────────
def activity_diagram():
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Activity Diagram', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    # Start
    ax.plot(5, 11.5, 'o', color=ACCENT, markersize=15, markeredgecolor=TEXT, markeredgewidth=2)

    activities = [
        (5, 10.8, 'Open Application'),
        (5, 9.8, 'Login / Register'),
        (5, 8.8, 'View Home Dashboard'),
        (5, 7.8, 'Navigate to Predict'),
        (5, 6.8, 'Enter Vehicle Features (9 inputs)'),
        (5, 5.8, 'Submit Prediction'),
        (5, 4.8, 'Preprocess → Encode + Scale'),
        (5, 3.8, 'Random Forest Predict'),
        (5, 2.8, 'Calculate CO₂ Rating (1-10)'),
        (5, 1.8, 'Display Result + Save to DB'),
    ]

    for x, y, label in activities:
        draw_box(ax, x, y, 4.0, 0.6, label, ACCENT2, 9)

    # Decision diamond after login
    diamond_x, diamond_y = 5, 9.3
    diamond = plt.Polygon([[diamond_x, diamond_y + 0.25], [diamond_x + 0.4, diamond_y],
                           [diamond_x, diamond_y - 0.25], [diamond_x - 0.4, diamond_y]],
                          facecolor='#e9c46a', edgecolor=TEXT, linewidth=1.2)
    ax.add_patch(diamond)
    ax.text(diamond_x, diamond_y, '?', ha='center', va='center', fontsize=10,
            color='black', fontweight='bold')
    ax.text(diamond_x + 0.5, diamond_y + 0.1, 'Valid?', fontsize=8, color='#e9c46a')

    # Arrows
    for i in range(len(activities) - 1):
        y1 = activities[i][1] - 0.3
        y2 = activities[i + 1][1] + 0.3
        if i == 1:  # skip for decision diamond
            draw_arrow(ax, 5, y1, 5, diamond_y + 0.25)
            draw_arrow(ax, 5, diamond_y - 0.25, 5, y2)
        else:
            draw_arrow(ax, 5, y1, 5, y2)

    draw_arrow(ax, 5, 11.5, 5, 11.1)

    # End
    ax.plot(5, 1.2, 'o', color='#e94560', markersize=15, markeredgecolor=TEXT, markeredgewidth=2)
    ax.plot(5, 1.2, 'o', color='#e94560', markersize=10)
    draw_arrow(ax, 5, 1.5, 5, 1.3)

    # Side options
    draw_box(ax, 8.5, 7.8, 2.5, 0.5, 'View History', '#0f3460', 8)
    draw_box(ax, 8.5, 6.8, 2.5, 0.5, 'View Dashboard', '#533483', 8)
    draw_box(ax, 8.5, 5.8, 2.5, 0.5, 'View About', '#0f3460', 8)
    for y in [7.8, 6.8, 5.8]:
        ax.annotate('', xy=(7.25, y), xytext=(7.0, y),
                    arrowprops=dict(arrowstyle='->', color='#666688', lw=1))

    save_fig(fig, 'activity_diagram.png')


# ── 6. ER Diagram ───────────────────────────────────────────────────────
def er_diagram():
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Entity-Relationship Diagram', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    def draw_entity(x, y, w, h, name, attrs, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                    facecolor=CARD, edgecolor=color, linewidth=2))
        ax.add_patch(plt.Rectangle((x + 0.05, y + h - 0.5), w - 0.1, 0.45,
                                   facecolor=color, alpha=0.3))
        ax.text(x + w/2, y + h - 0.28, name, ha='center', va='center',
                fontsize=12, color=TEXT, fontweight='bold')
        ay = y + h - 0.75
        for attr in attrs:
            prefix = 'PK ' if 'PK' in attr else 'FK ' if 'FK' in attr else '   '
            clean = attr.replace(' PK', '').replace(' FK', '')
            ax.text(x + 0.2, ay, prefix, fontsize=8, color='#e9c46a' if 'PK' in attr
                    else '#e94560' if 'FK' in attr else '#888888', family='monospace',
                    fontweight='bold')
            ax.text(x + 0.6, ay, clean, fontsize=8, color=TEXT, family='monospace')
            ay -= 0.3

    # Users entity
    draw_entity(0.5, 2.5, 4, 3.5, 'USERS', [
        'id INTEGER PK',
        'username TEXT UNIQUE',
        'password TEXT (hash)',
        'name TEXT',
        'role TEXT',
    ], ACCENT)

    # Predictions entity
    draw_entity(6.5, 1.5, 4, 4.5, 'PREDICTIONS', [
        'id INTEGER PK',
        'user_id INTEGER FK',
        'input_data TEXT (JSON)',
        'predicted_co2 REAL',
        'co2_rating INTEGER',
        'pred_date TEXT',
    ], '#e94560')

    # Relationship
    ax.annotate('', xy=(6.5, 4.2), xytext=(4.5, 4.2),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2.5))
    diamond = plt.Polygon([[5.5, 4.5], [5.85, 4.2], [5.5, 3.9], [5.15, 4.2]],
                          facecolor='#e9c46a', edgecolor=TEXT, linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(5.5, 4.2, 'has', ha='center', va='center', fontsize=8, color='black', fontweight='bold')
    ax.text(4.6, 4.45, '1', fontsize=11, color=ACCENT, fontweight='bold')
    ax.text(6.3, 4.45, 'N', fontsize=11, color='#e94560', fontweight='bold')

    save_fig(fig, 'er_diagram.png')


# ── 7. Agile Model ──────────────────────────────────────────────────────
def agile_model():
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Agile Development Model', color=TEXT, fontsize=16, fontweight='bold', pad=15)

    sprints = [
        ('Sprint 1\n(Weeks 1-2)', 'Project Setup\nFlask App\nDB Schema', ACCENT),
        ('Sprint 2\n(Weeks 3-4)', 'Dataset Gen\nML Training\n6 Models', '#e94560'),
        ('Sprint 3\n(Weeks 5-6)', 'Prediction UI\nForm Validation\nResult Display', '#0f3460'),
        ('Sprint 4\n(Weeks 7-8)', 'History Page\nDashboard\nChart.js', '#533483'),
        ('Sprint 5\n(Weeks 9-10)', 'Testing\nDocker\nDeployment', '#e9c46a'),
    ]

    for i, (title, tasks, color) in enumerate(sprints):
        x = 1.2 + i * 2.1
        # Sprint box
        ax.add_patch(FancyBboxPatch((x - 0.8, 1.5), 1.6, 3.0,
                                    boxstyle="round,pad=0.15", facecolor=CARD,
                                    edgecolor=color, linewidth=2, alpha=0.8))
        ax.text(x, 4.1, title, ha='center', va='center', fontsize=9,
                color=color, fontweight='bold')
        ax.text(x, 2.7, tasks, ha='center', va='center', fontsize=7.5,
                color=TEXT, linespacing=1.6)

        if i < len(sprints) - 1:
            draw_arrow(ax, x + 0.85, 3.0, x + 1.25, 3.0)

    # Cycle arrow at top
    ax.annotate('Continuous Integration & Feedback', xy=(6, 5.2), fontsize=10,
                color=ACCENT, ha='center', fontweight='bold')
    ax.annotate('', xy=(1.5, 4.8), xytext=(10.5, 4.8),
                arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=1.5, linestyle='--'))

    save_fig(fig, 'agile_model.png')


# ── Generate all ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Generating figures...")
    system_architecture()
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    activity_diagram()
    er_diagram()
    agile_model()
    print("\nAll 7 figures generated!")
