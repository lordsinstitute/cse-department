require('dotenv').config();
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');

const db = require('./db/database');

const app = express();

// View engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Flash messages via cookie
app.use((req, res, next) => {
  res.locals.success = req.cookies.flash_success || null;
  res.locals.error = req.cookies.flash_error || null;
  if (req.cookies.flash_success) res.clearCookie('flash_success');
  if (req.cookies.flash_error) res.clearCookie('flash_error');
  res.locals.user = null;
  next();
});

// Routes
app.use('/', require('./routes/auth'));
app.use('/', require('./routes/dashboard'));
app.use('/chat', require('./routes/chat'));
app.use('/mood', require('./routes/mood'));
app.use('/meditations', require('./routes/meditations'));
app.use('/therapists', require('./routes/therapists'));
app.use('/sessions', require('./routes/sessions'));
app.use('/', require('./routes/admin'));

// About page
const { protect } = require('./middleware/auth');
app.get('/about', protect, (req, res) => {
  res.render('about', { title: 'About MindfulPath', page: 'about' });
});

// 404
app.use((req, res) => {
  res.status(404).render('404', { title: '404 — Not Found', page: 'error' });
});

const PORT = process.env.PORT || 5006;
app.listen(PORT, () => {
  console.log(`MindfulPath running on http://127.0.0.1:${PORT}`);
});
