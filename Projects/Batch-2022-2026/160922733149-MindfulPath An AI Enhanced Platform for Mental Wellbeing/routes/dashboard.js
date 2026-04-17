const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect } = require('../middleware/auth');

router.get('/dashboard', protect, (req, res) => {
  const data = { title: 'Dashboard', page: 'dashboard' };

  if (req.user.role === 'admin') {
    data.stats = {
      totalUsers: db.prepare('SELECT COUNT(*) as c FROM users WHERE role = ?').get('user').c,
      totalTherapists: db.prepare('SELECT COUNT(*) as c FROM users WHERE role = ?').get('therapist').c,
      totalSessions: db.prepare('SELECT COUNT(*) as c FROM sessions').get().c,
      totalChats: db.prepare('SELECT COUNT(*) as c FROM chat_messages').get().c,
      totalMoodEntries: db.prepare('SELECT COUNT(*) as c FROM mood_entries').get().c
    };
  } else if (req.user.role === 'therapist') {
    const therapist = db.prepare('SELECT id FROM therapists WHERE user_id = ?').get(req.user.id);
    if (therapist) {
      data.upcomingSessions = db.prepare(`
        SELECT s.*, u.name as patient_name FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.therapist_id = ? AND s.status = 'scheduled'
        ORDER BY s.session_date, s.session_time
      `).all(therapist.id);
      data.completedCount = db.prepare("SELECT COUNT(*) as c FROM sessions WHERE therapist_id = ? AND status = 'completed'").get(therapist.id).c;
      data.patientCount = db.prepare('SELECT COUNT(DISTINCT user_id) as c FROM sessions WHERE therapist_id = ?').get(therapist.id).c;
    } else {
      data.upcomingSessions = [];
      data.completedCount = 0;
      data.patientCount = 0;
    }
  } else {
    // User role
    data.moodEntries = db.prepare('SELECT mood_score, mood_label, created_at FROM mood_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 7').all(req.user.id);
    data.recentChats = db.prepare('SELECT id, started_at, message_count, avg_sentiment FROM chat_sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT 5').all(req.user.id);
    data.upcomingSessions = db.prepare(`
      SELECT s.*, t.user_id as t_user_id, u.name as therapist_name FROM sessions s
      JOIN therapists t ON s.therapist_id = t.id
      JOIN users u ON t.user_id = u.id
      WHERE s.user_id = ? AND s.status = 'scheduled'
      ORDER BY s.session_date, s.session_time
    `).all(req.user.id);
  }

  res.render('dashboard', data);
});

// API endpoint for dashboard chart data
router.get('/api/dashboard/mood-trend', protect, (req, res) => {
  const entries = db.prepare('SELECT mood_score, mood_label, created_at FROM mood_entries WHERE user_id = ? ORDER BY created_at ASC LIMIT 30').all(req.user.id);
  res.json(entries);
});

module.exports = router;
