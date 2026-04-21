const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const db = require('../db/database');
const { protect, authorize } = require('../middleware/auth');
const { analyzeSentiment } = require('../nlp/sentiment');
const { getGreeting, getResponse } = require('../nlp/responses');
const { getLLMResponse } = require('../nlp/llm');
const { getSettings } = require('../db/database');

// Chat page
router.get('/', protect, (req, res) => {
  const sessions = db.prepare('SELECT id, started_at, message_count, avg_sentiment FROM chat_sessions WHERE user_id = ? ORDER BY started_at DESC').all(req.user.id);
  res.render('chat', { title: 'AI Chat', page: 'chat', chatSessions: sessions });
});

// Start new chat session
router.post('/new', protect, (req, res) => {
  const sessionId = uuidv4();
  db.prepare('INSERT INTO chat_sessions (id, user_id) VALUES (?, ?)').run(sessionId, req.user.id);

  const greeting = getGreeting();
  db.prepare('INSERT INTO chat_messages (chat_session_id, user_id, role, message, therapy_technique) VALUES (?, ?, ?, ?, ?)').run(sessionId, req.user.id, 'bot', greeting, 'greeting');
  db.prepare('UPDATE chat_sessions SET message_count = 1 WHERE id = ?').run(sessionId);

  res.json({ sessionId, messages: [{ role: 'bot', message: greeting, technique: 'greeting', created_at: new Date().toISOString() }] });
});

// Send message
router.post('/send', protect, async (req, res) => {
  const { sessionId, message } = req.body;
  if (!sessionId || !message) return res.status(400).json({ error: 'Missing sessionId or message' });

  const session = db.prepare('SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?').get(sessionId, req.user.id);
  if (!session) return res.status(404).json({ error: 'Chat session not found' });

  // Analyze user message (async — transformer model)
  const sentiment = await analyzeSentiment(message);

  // Save user message
  db.prepare('INSERT INTO chat_messages (chat_session_id, user_id, role, message, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?, ?)').run(sessionId, req.user.id, 'user', message, sentiment.comparative, sentiment.label);

  // Generate bot response — use LLM if configured, else local CBT rules
  const messageCount = session.message_count || 0;
  let botResponse;

  const settings = getSettings();
  if (settings.nlp_mode === 'api' && settings.api_key) {
    try {
      const history = db.prepare(
        'SELECT role, message, therapy_technique FROM chat_messages WHERE chat_session_id = ? ORDER BY created_at ASC'
      ).all(sessionId);

      const llmText = await getLLMResponse(history, settings.api_provider, settings.api_key, settings.api_model, sentiment.label);
      botResponse = { text: llmText, technique: 'ai_response' };
    } catch (err) {
      console.error('[MindfulPath] LLM error, falling back to local:', err.message);
      botResponse = getResponse(sentiment, messageCount);
    }
  } else {
    botResponse = getResponse(sentiment, messageCount);
  }

  // Save bot message
  db.prepare('INSERT INTO chat_messages (chat_session_id, user_id, role, message, therapy_technique) VALUES (?, ?, ?, ?, ?)').run(sessionId, req.user.id, 'bot', botResponse.text, botResponse.technique);

  // Update session stats
  const allSentiments = db.prepare("SELECT sentiment_score FROM chat_messages WHERE chat_session_id = ? AND role = 'user' AND sentiment_score IS NOT NULL").all(sessionId);
  const avgSentiment = allSentiments.length > 0 ? allSentiments.reduce((sum, m) => sum + m.sentiment_score, 0) / allSentiments.length : 0;
  db.prepare('UPDATE chat_sessions SET message_count = message_count + 2, avg_sentiment = ? WHERE id = ?').run(avgSentiment, sessionId);

  res.json({
    userMessage: { role: 'user', message, sentiment_score: sentiment.comparative, sentiment_label: sentiment.label, created_at: new Date().toISOString() },
    botMessage: { role: 'bot', message: botResponse.text, technique: botResponse.technique, created_at: new Date().toISOString() }
  });
});

// Get chat history for a session
router.get('/history/:sessionId', protect, (req, res) => {
  const session = db.prepare('SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?').get(req.params.sessionId, req.user.id);
  if (!session) return res.status(404).json({ error: 'Chat session not found' });

  const messages = db.prepare('SELECT role, message, sentiment_score, sentiment_label, therapy_technique as technique, created_at FROM chat_messages WHERE chat_session_id = ? ORDER BY created_at ASC').all(req.params.sessionId);
  res.json({ sessionId: session.id, messages });
});

// Admin: list all users with their chat sessions
router.get('/admin/chats', protect, authorize('admin'), (req, res) => {
  const users = db.prepare(`
    SELECT u.id, u.name, u.email, u.role, u.created_at,
      COUNT(DISTINCT cs.id) as session_count,
      SUM(cs.message_count) as total_messages,
      MAX(cs.started_at) as last_chat
    FROM users u
    LEFT JOIN chat_sessions cs ON cs.user_id = u.id
    WHERE u.role != 'admin'
    GROUP BY u.id
    ORDER BY last_chat DESC NULLS LAST
  `).all();

  res.render('admin-chats', { title: 'Chat History — Admin', page: 'admin-chats', users });
});

// Admin: view all sessions for a specific user
router.get('/admin/chats/user/:userId', protect, authorize('admin'), (req, res) => {
  const patient = db.prepare('SELECT id, name, email, role FROM users WHERE id = ? AND role != ?').get(req.params.userId, 'admin');
  if (!patient) return res.status(404).render('404', { title: 'Not Found', page: 'error' });

  const sessions = db.prepare(`
    SELECT id, started_at, message_count, avg_sentiment
    FROM chat_sessions WHERE user_id = ?
    ORDER BY started_at DESC
  `).all(req.params.userId);

  res.render('admin-chats', { title: `${patient.name}'s Chats — Admin`, page: 'admin-chats', patient, sessions });
});

// Admin: view full message log of a specific session
router.get('/admin/chats/session/:sessionId', protect, authorize('admin'), (req, res) => {
  const session = db.prepare(`
    SELECT cs.*, u.name as user_name, u.email as user_email, u.role as user_role
    FROM chat_sessions cs JOIN users u ON cs.user_id = u.id
    WHERE cs.id = ?
  `).get(req.params.sessionId);
  if (!session) return res.status(404).render('404', { title: 'Not Found', page: 'error' });

  const messages = db.prepare(`
    SELECT role, message, sentiment_score, sentiment_label, therapy_technique as technique, created_at
    FROM chat_messages WHERE chat_session_id = ? ORDER BY created_at ASC
  `).all(req.params.sessionId);

  res.render('admin-chats', { title: `Session Log — Admin`, page: 'admin-chats', session, messages });
});

module.exports = router;
