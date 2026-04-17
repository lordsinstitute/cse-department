const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect } = require('../middleware/auth');

// Browse therapists
router.get('/', protect, (req, res) => {
  const therapists = db.prepare(`
    SELECT t.*, u.name, u.bio, u.email FROM therapists t
    JOIN users u ON t.user_id = u.id
    ORDER BY t.avg_rating DESC, t.experience DESC
  `).all();
  // Parse specialties JSON
  therapists.forEach(t => { t.specialties_arr = JSON.parse(t.specialties); });
  res.render('therapists', { title: 'Therapists', page: 'therapists', therapists, therapist: null });
});

// Therapist profile
router.get('/:id', protect, (req, res) => {
  const therapist = db.prepare(`
    SELECT t.*, u.name, u.bio, u.email FROM therapists t
    JOIN users u ON t.user_id = u.id
    WHERE t.id = ?
  `).get(req.params.id);
  if (!therapist) {
    res.cookie('flash_error', 'Therapist not found');
    return res.redirect('/therapists');
  }
  therapist.specialties_arr = JSON.parse(therapist.specialties);
  res.render('therapists', { title: therapist.name, page: 'therapist-detail', therapist, therapists: null });
});

module.exports = router;
