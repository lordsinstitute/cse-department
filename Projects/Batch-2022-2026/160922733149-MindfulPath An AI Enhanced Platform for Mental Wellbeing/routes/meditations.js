const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect } = require('../middleware/auth');

// Browse meditations
router.get('/', protect, (req, res) => {
  const category = req.query.category;
  let meditations;
  if (category && category !== 'all') {
    meditations = db.prepare('SELECT * FROM meditations WHERE category = ? ORDER BY title').all(category);
  } else {
    meditations = db.prepare('SELECT * FROM meditations ORDER BY category, title').all();
  }
  const categories = db.prepare('SELECT DISTINCT category FROM meditations ORDER BY category').all().map(r => r.category);
  res.render('meditations', { title: 'Meditations', page: 'meditations', meditations, categories, selectedCategory: category || 'all' });
});

// Single meditation
router.get('/:id', protect, (req, res) => {
  const meditation = db.prepare('SELECT * FROM meditations WHERE id = ?').get(req.params.id);
  if (!meditation) {
    res.cookie('flash_error', 'Meditation not found');
    return res.redirect('/meditations');
  }
  res.render('meditations', { title: meditation.title, page: 'meditation-detail', meditation, meditations: null, categories: null, selectedCategory: null });
});

module.exports = router;
