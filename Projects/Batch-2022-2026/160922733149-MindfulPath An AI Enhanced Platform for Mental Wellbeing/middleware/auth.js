const jwt = require('jsonwebtoken');
const db = require('../db/database');

const JWT_SECRET = process.env.JWT_SECRET || 'mindfulpath_secret_key_for_development';

function protect(req, res, next) {
  const token = req.cookies && req.cookies.token;
  if (!token) {
    return res.redirect('/login');
  }
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    const user = db.prepare('SELECT id, name, email, role FROM users WHERE id = ?').get(decoded.id);
    if (!user) return res.redirect('/login');
    req.user = user;
    res.locals.user = user;
    next();
  } catch (err) {
    res.clearCookie('token');
    return res.redirect('/login');
  }
}

function authorize(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).render('layout', {
        title: 'Access Denied',
        body: '<div class="text-center mt-5"><h2>403 — Access Denied</h2><p>You do not have permission to access this page.</p><a href="/dashboard" class="btn btn-accent mt-3">Go to Dashboard</a></div>',
        page: 'error'
      });
    }
    next();
  };
}

module.exports = { protect, authorize };
