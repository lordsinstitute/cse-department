const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../db/database');

const JWT_SECRET = process.env.JWT_SECRET || 'mindfulpath_secret_key_for_development';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '30d';

// Home — redirect
router.get('/', (req, res) => {
  const token = req.cookies && req.cookies.token;
  if (token) {
    try {
      jwt.verify(token, JWT_SECRET);
      return res.redirect('/dashboard');
    } catch (e) { /* invalid token */ }
  }
  res.redirect('/login');
});

// Login page
router.get('/login', (req, res) => {
  res.render('login', { title: 'Login', page: 'login' });
});

// Login submit
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email);
  if (!user || !bcrypt.compareSync(password, user.password)) {
    res.cookie('flash_error', 'Invalid email or password');
    return res.redirect('/login');
  }
  const token = jwt.sign({ id: user.id, role: user.role }, JWT_SECRET, {
    expiresIn: JWT_EXPIRES_IN
  });
  res.cookie('token', token, { httpOnly: true, maxAge: 30 * 24 * 60 * 60 * 1000 });
  res.redirect('/dashboard');
});

// Register page
router.get('/register', (req, res) => {
  res.render('register', { title: 'Register', page: 'register' });
});

// Register submit
router.post('/register', (req, res) => {
  const { name, email, password, role, specialties, education, experience, license, session_price, approach, languages } = req.body;

  const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
  if (existing) {
    res.cookie('flash_error', 'Email already registered');
    return res.redirect('/register');
  }

  const hash = bcrypt.hashSync(password, 10);
  const userRole = role === 'therapist' ? 'therapist' : 'user';

  const result = db.prepare('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)').run(name, email, hash, userRole);

  if (userRole === 'therapist') {
    const specs = Array.isArray(specialties) ? JSON.stringify(specialties) : JSON.stringify([specialties]);
    db.prepare('INSERT INTO therapists (user_id, specialties, education, experience, license, approach, session_price, languages) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .run(result.lastInsertRowid, specs, education, parseInt(experience) || 1, license, approach || '', parseFloat(session_price) || 500, languages || 'English');
  }

  res.cookie('flash_success', 'Registration successful! Please login.');
  res.redirect('/login');
});

// Logout
router.get('/logout', (req, res) => {
  res.clearCookie('token');
  res.redirect('/login');
});

module.exports = router;
