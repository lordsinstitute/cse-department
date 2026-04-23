{% extends "base.html" %}
{% block title %}Dashboard — HateSpeech Analyzer{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-house"></i> Dashboard</h2>
<p class="text-muted">Welcome back, <strong>{{ session.get('name', '') }}</strong></p>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="stat-card">
            <h3>{{ user_predictions }}</h3>
            <p><i class="bi bi-chat-text"></i> Total Analyses</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05)); border-color: rgba(239, 68, 68, 0.3);">
            <h3 style="color: #ef4444;">{{ hate_count }}</h3>
            <p><i class="bi bi-exclamation-triangle"></i> Hate Speech</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.05)); border-color: rgba(245, 158, 11, 0.3);">
            <h3 style="color: #f59e0b;">{{ offensive_count }}</h3>
            <p><i class="bi bi-exclamation-circle"></i> Offensive</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.05)); border-color: rgba(34, 197, 94, 0.3);">
            <h3 style="color: #22c55e;">{{ clean_count }}</h3>
            <p><i class="bi bi-check-circle"></i> Clean</p>
        </div>
    </div>
</div>

{% if admin_stats %}
<div class="card mb-4">
    <div class="card-header"><i class="bi bi-gear"></i> Admin Statistics</div>
    <div class="card-body">
        <div class="row g-4">
            <div class="col-md-4">
                <div class="stat-card">
                    <h3>{{ admin_stats.total_users }}</h3>
                    <p><i class="bi bi-people"></i> Registered Users</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card">
                    <h3>{{ admin_stats.total_predictions }}</h3>
                    <p><i class="bi bi-chat-text"></i> Total Analyses</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05)); border-color: rgba(239, 68, 68, 0.3);">
                    <h3 style="color: #ef4444;">{{ admin_stats.total_hate }}</h3>
                    <p><i class="bi bi-exclamation-triangle"></i> Total Hate Speech Detected</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}

<div class="card mb-4">
    <div class="card-header"><i class="bi bi-clock-history"></i> Recent Analyses</div>
    <div class="card-body">
        {% if recent %}
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Text</th>
                        <th>Result</th>
                        <th>Confidence</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in recent %}
                    <tr>
                        <td style="max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{{ p['input_text'] }}">{{ p['input_text'][:80] }}{% if p['input_text']|length > 80 %}...{% endif %}</td>
                        <td>
                            {% if p['prediction'] == 'Hate Speech' %}
                            <span class="badge badge-hate"><i class="bi bi-exclamation-triangle"></i> {{ p['prediction'] }}</span>
                            {% elif p['prediction'] == 'Offensive' %}
                            <span class="badge badge-offensive"><i class="bi bi-exclamation-circle"></i> {{ p['prediction'] }}</span>
                            {% else %}
                            <span class="badge badge-clean"><i class="bi bi-check-circle"></i> {{ p['prediction'] }}</span>
                            {% endif %}
                        </td>
                        <td>{{ p['confidence'] }}%</td>
                        <td>{{ p['created_at'][:16] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <p class="text-muted mb-0">No analyses yet. <a href="{{ url_for('predict') }}">Analyze your first text</a></p>
        {% endif %}
    </div>
</div>

<div class="row g-3">
    <div class="col-md-3">
        <a href="{{ url_for('predict') }}" class="btn btn-danger w-100 py-3">
            <i class="bi bi-search"></i><br>Analyze Text
        </a>
    </div>
    <div class="col-md-3">
        <a href="{{ url_for('history') }}" class="btn btn-outline-danger w-100 py-3">
            <i class="bi bi-clock-history"></i><br>View History
        </a>
    </div>
    <div class="col-md-3">
        <a href="{{ url_for('visualize') }}" class="btn btn-outline-danger w-100 py-3">
            <i class="bi bi-bar-chart"></i><br>Visualize Data
        </a>
    </div>
    <div class="col-md-3">
        <a href="{{ url_for('dashboard') }}" class="btn btn-outline-danger w-100 py-3">
            <i class="bi bi-speedometer2"></i><br>Model Dashboard
        </a>
    </div>
</div>
{% endblock %}
