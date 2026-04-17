// MindfulPath — Chat Interface JavaScript

let currentSessionId = null;

const chatMessages = document.getElementById('chatMessages');
const chatPlaceholder = document.getElementById('chatPlaceholder');
const chatInputArea = document.getElementById('chatInputArea');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const newChatBtn = document.getElementById('newChatBtn');
const sendBtn = document.getElementById('sendBtn');

// New chat
newChatBtn.addEventListener('click', async () => {
  try {
    const res = await fetch('/chat/new', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = await res.json();
    currentSessionId = data.sessionId;

    chatPlaceholder.style.display = 'none';
    chatInputArea.style.display = 'block';
    chatMessages.innerHTML = '';

    data.messages.forEach(m => appendMessage(m));
    chatInput.focus();

    // Add to sidebar
    const item = document.createElement('div');
    item.className = 'chat-session-item active';
    item.dataset.id = data.sessionId;
    item.innerHTML = `<small class="text-muted">${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small><br><span class="badge bg-secondary">1 messages</span>`;
    const list = document.getElementById('chatSessionsList');
    document.querySelectorAll('.chat-session-item').forEach(el => el.classList.remove('active'));
    list.prepend(item);
    item.addEventListener('click', () => loadSession(data.sessionId));
  } catch (err) {
    console.error('Error starting chat:', err);
  }
});

// Send message
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message || !currentSessionId) return;

  chatInput.value = '';
  sendBtn.disabled = true;

  // Show typing indicator
  const typingEl = document.createElement('div');
  typingEl.className = 'chat-bubble bot';
  typingEl.innerHTML = '<em>Thinking...</em>';
  chatMessages.appendChild(typingEl);
  requestAnimationFrame(() => {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
  });

  try {
    const res = await fetch('/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sessionId: currentSessionId, message })
    });
    const data = await res.json();

    if (chatMessages.contains(typingEl)) chatMessages.removeChild(typingEl);

    if (data.error) throw new Error(data.error);

    appendMessage(data.userMessage);
    appendMessage(data.botMessage);
  } catch (err) {
    if (chatMessages.contains(typingEl)) chatMessages.removeChild(typingEl);
    console.error('Error sending message:', err);
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
});

// Load previous session
document.querySelectorAll('.chat-session-item').forEach(item => {
  item.addEventListener('click', () => loadSession(item.dataset.id));
});

async function loadSession(sessionId) {
  try {
    const res = await fetch(`/chat/history/${sessionId}`);
    const data = await res.json();
    currentSessionId = sessionId;

    chatPlaceholder.style.display = 'none';
    chatInputArea.style.display = 'block';
    chatMessages.innerHTML = '';

    document.querySelectorAll('.chat-session-item').forEach(el => el.classList.remove('active'));
    const activeItem = document.querySelector(`.chat-session-item[data-id="${sessionId}"]`);
    if (activeItem) activeItem.classList.add('active');

    data.messages.forEach(m => appendMessage(m));
    chatInput.focus();
  } catch (err) {
    console.error('Error loading session:', err);
  }
}

function appendMessage(msg) {
  const div = document.createElement('div');
  div.className = `chat-bubble ${msg.role}`;

  let content = msg.message.replace(/\n/g, '<br>');

  if (msg.role === 'user' && msg.sentiment_label) {
    content += ` <span class="sentiment-dot ${msg.sentiment_label}" title="Sentiment: ${msg.sentiment_label}"></span>`;
  }

  if (msg.role === 'bot' && msg.technique) {
    content += `<br><small class="text-muted" style="font-size: 0.75rem;"><i class="bi bi-lightbulb"></i> ${msg.technique.replace(/_/g, ' ')}</small>`;
  }

  div.innerHTML = content;
  chatMessages.appendChild(div);
  requestAnimationFrame(() => {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
  });
}
