const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect } = require('../middleware/auth');

// View sessions
router.get('/', protect, (req, res) => {
  let sessions;
  const therapists = db.prepare('SELECT t.id, u.name FROM therapists t JOIN users u ON t.user_id = u.id ORDER BY u.name').all();

  if (req.user.role === 'therapist') {
    const therapist = db.prepare('SELECT id FROM therapists WHERE user_id = ?').get(req.user.id);
    sessions = therapist ? db.prepare(`
      SELECT s.*, u.name as patient_name FROM sessions s
      JOIN users u ON s.user_id = u.id
      WHERE s.therapist_id = ?
      ORDER BY s.session_date DESC, s.session_time DESC
    `).all(therapist.id) : [];
  } else {
    sessions = db.prepare(`
      SELECT s.*, u.name as therapist_name FROM sessions s
      JOIN therapists t ON s.therapist_id = t.id
      JOIN users u ON t.user_id = u.id
      WHERE s.user_id = ?
      ORDER BY s.session_date DESC, s.session_time DESC
    `).all(req.user.id);
  }

  res.render('sessions', { title: 'Sessions', page: 'sessions', sessions, therapists });
});

// Book session
router.post('/book', protect, (req, res) => {
  const { therapist_id, session_date, session_time, duration, type } = req.body;
  const therapist = db.prepare('SELECT * FROM therapists WHERE id = ?').get(therapist_id);
  if (!therapist) {
    res.cookie('flash_error', 'Therapist not found');
    return res.redirect('/sessions');
  }
  const dur = parseInt(duration) || 60;
  const priceMultiplier = dur / 60;
  const price = therapist.session_price * priceMultiplier;

  db.prepare('INSERT INTO sessions (user_id, therapist_id, session_date, session_time, duration, type, price) VALUES (?, ?, ?, ?, ?, ?, ?)').run(req.user.id, therapist.id, session_date, session_time, dur, type || 'video', price);

  res.cookie('flash_success', 'Session booked successfully!');
  res.redirect('/sessions');
});

// Cancel session
router.post('/:id/cancel', protect, (req, res) => {
  const session = db.prepare('SELECT * FROM sessions WHERE id = ?').get(req.params.id);
  if (!session) {
    res.cookie('flash_error', 'Session not found');
    return res.redirect('/sessions');
  }
  db.prepare("UPDATE sessions SET status = 'cancelled' WHERE id = ?").run(req.params.id);
  res.cookie('flash_success', 'Session cancelled.');
  res.redirect('/sessions');
});

module.exports = router;
