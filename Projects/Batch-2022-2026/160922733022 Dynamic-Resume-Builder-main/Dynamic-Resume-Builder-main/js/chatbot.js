/* ============================================
   ResumeForge — AI Chatbot Module
   ============================================ */

let chatHistory = []; // Stores messages { role, content }

// System prompt for the assistant
const CHAT_SYSTEM_PROMPT = `You are a helpful resume assistant for ResumeForge. 
You help users craft better resumes, provide ATS optimization tips, suggest improvements to content, 
and answer questions about resume writing. 
You have access to the user's current resume data (if provided). 
Be concise, professional, and encouraging. 
If the user asks for specific improvements, offer actionable suggestions.`;

// Load chat history from localStorage (optional)
function loadChatHistory() {
    const saved = localStorage.getItem('resumeforge_chat_history');
    if (saved) {
        try {
            chatHistory = JSON.parse(saved);
            // Render existing messages
            chatHistory.forEach(msg => {
                if (msg.role !== 'system') {
                    addMessageToUI(msg.role, msg.content);
                }
            });
        } catch (e) {}
    }
}

// Save chat history to localStorage
function saveChatHistory() {
    // Limit history to last 50 messages to avoid token explosion
    const toSave = chatHistory.slice(-50);
    localStorage.setItem('resumeforge_chat_history', JSON.stringify(toSave));
}

// Add a message to the UI
function addMessageToUI(role, content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    messageDiv.innerHTML = `<div class="message-bubble">${escapeHTMLForChat(content)}</div>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Show loading indicator
function showChatLoading() {
    const messagesDiv = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'chat-message assistant';
    loadingDiv.id = 'chat-loading';
    loadingDiv.innerHTML = `<div class="message-bubble"><div class="spinner-border spinner-border-sm text-warning me-1" role="status"></div> Thinking...</div>`;
    messagesDiv.appendChild(loadingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideChatLoading() {
    const loading = document.getElementById('chat-loading');
    if (loading) loading.remove();
}

// Send message to AI
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    // Add user message to UI and history
    addMessageToUI('user', message);
    chatHistory.push({ role: 'user', content: message });
    saveChatHistory();

    // Clear input
    input.value = '';

    // Check API key
    if (!AI_CONFIG.apiKey) {
        addMessageToUI('assistant', '⚠️ Please set your OpenRouter API key in Settings (gear icon) first.');
        chatHistory.push({ role: 'assistant', content: 'Please set your API key in Settings.' });
        saveChatHistory();
        return;
    }

    showChatLoading();

    try {
        // Build messages for API
        let messages = [
            { role: 'system', content: CHAT_SYSTEM_PROMPT },
            ...chatHistory.slice(-10) // Last 10 messages for context (to keep tokens manageable)
        ];

        // Optionally include resume data as context if it's a relevant question
        if (resumeData && (resumeData.personal.firstName || resumeData.experience.length > 0)) {
            const resumeSummary = `Current resume summary: ${JSON.stringify({
                name: `${resumeData.personal.firstName} ${resumeData.personal.lastName}`,
                title: resumeData.personal.title,
                experienceCount: resumeData.experience.length,
                educationCount: resumeData.education.length,
                skills: resumeData.skills.map(s => s.name).slice(0,5)
            })}`;
            // Add as system message before the main system prompt
            messages.unshift({ role: 'system', content: resumeSummary });
        }

        // Call OpenRouter (use the new chat function)
        const reply = await callOpenRouterChat(messages);

        // Add assistant reply to UI and history
        addMessageToUI('assistant', reply);
        chatHistory.push({ role: 'assistant', content: reply });
        saveChatHistory();

    } catch (error) {
        console.error('Chat error:', error);
        addMessageToUI('assistant', `❌ Error: ${error.message || 'Something went wrong'}. Please try again.`);
        chatHistory.push({ role: 'assistant', content: `Error: ${error.message}` });
        saveChatHistory();
    } finally {
        hideChatLoading();
    }
}

// Escape HTML for chat messages
function escapeHTMLForChat(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
        .replace(/\n/g, '<br>');
}

// Allow pressing Enter to send
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    loadChatHistory();
});