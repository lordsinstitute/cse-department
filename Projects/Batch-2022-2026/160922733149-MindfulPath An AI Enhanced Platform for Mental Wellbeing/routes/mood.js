const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect } = require('../middleware/auth');
const { analyzeSentiment } = require('../nlp/sentiment');

// Mood tracker page
router.get('/', protect, (req, res) => {
  const entries = db.prepare('SELECT * FROM mood_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 20').all(req.user.id);
  res.render('mood', { title: 'Mood Tracker', page: 'mood', entries });
});

// Add mood entry
router.post('/add', protect, (req, res) => {
  const { mood_score, journal_text } = req.body;
  const score = parseInt(mood_score);
  const labels = { 1: 'very_sad', 2: 'sad', 3: 'neutral', 4: 'happy', 5: 'very_happy' };
  const moodLabel = labels[score] || 'neutral';

  let sentimentScore = null;
  let sentimentLabel = null;
  if (journal_text && journal_text.trim()) {
    const result = analyzeSentiment(journal_text);
    sentimentScore = result.comparative;
    sentimentLabel = result.label;
  }

  db.prepare('INSERT INTO mood_entries (user_id, mood_score, mood_label, journal_text, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?, ?)').run(req.user.id, score, moodLabel, journal_text || null, sentimentScore, sentimentLabel);

  res.cookie('flash_success', 'Mood entry logged successfully!');
  res.redirect('/mood');
});

// Mood data API for chart
router.get('/data', protect, (req, res) => {
  const entries = db.prepare('SELECT mood_score, mood_label, sentiment_score, sentiment_label, created_at FROM mood_entries WHERE user_id = ? ORDER BY created_at ASC LIMIT 30').all(req.user.id);
  res.json(entries);
});

module.exports = router;
