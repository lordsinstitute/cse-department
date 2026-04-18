/**
 * AgentUI — SocketIO client for live browser screenshots and action logs.
 * Shared by both scraper.html and form_filler.html.
 */
class AgentUI {
    constructor() {
        this.room = 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
        this.socket = io();
        this.onComplete = null;

        this.socket.on('connect', () => {
            this.socket.emit('join', { room: this.room });
        });

        this.socket.on('screenshot', (data) => {
            this._updateScreenshot(data.image);
        });

        this.socket.on('agent_log', (data) => {
            this._appendLog(data.message, data.level, data.step);
        });

        this.socket.on('agent_complete', (data) => {
            this._appendLog(
                `Agent finished: ${data.summary}`,
                data.success ? 'success' : 'error'
            );
            if (this.onComplete) {
                this.onComplete(data);
            }
        });
    }

    _updateScreenshot(base64Image) {
        const img = document.getElementById('screenshot');
        const placeholder = document.getElementById('placeholderText');
        if (img && base64Image) {
            img.src = 'data:image/jpeg;base64,' + base64Image;
            img.style.display = 'block';
            if (placeholder) placeholder.style.display = 'none';
        }
    }

    _appendLog(message, level, step) {
        const container = document.getElementById('logContainer');
        if (!container) return;

        const entry = document.createElement('div');
        entry.className = `log-entry log-${level || 'info'}`;

        const time = new Date().toLocaleTimeString();
        const stepStr = step ? `[Step ${step}] ` : '';
        entry.textContent = `${time} ${stepStr}${message}`;

        container.appendChild(entry);
        container.scrollTop = container.scrollHeight;
    }

    clearLog() {
        const container = document.getElementById('logContainer');
        if (container) {
            container.innerHTML = '';
        }
    }
}
