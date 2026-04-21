const express = require('express');
const router = express.Router();
const db = require('../db/database');
const { protect, authorize } = require('../middleware/auth');
const { testConnection } = require('../nlp/llm');

// GET /admin/settings
router.get('/admin/settings', protect, authorize('admin'), (req, res) => {
  const settings = db.getSettings();
  res.render('admin-settings', { title: 'AI Settings — Admin', page: 'admin-settings', settings });
});

// POST /admin/settings
router.post('/admin/settings', protect, authorize('admin'), (req, res) => {
  const { nlp_mode, api_provider, api_key, api_model } = req.body;

  const upsert = db.prepare('INSERT INTO app_settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at');

  upsert.run('nlp_mode', nlp_mode === 'api' ? 'api' : 'local');
  upsert.run('api_provider', ['claude', 'openai', 'gemini'].includes(api_provider) ? api_provider : 'claude');

  // Only update the key if a new one was provided (don't wipe existing key with empty string)
  if (api_key && api_key.trim()) {
    upsert.run('api_key', api_key.trim());
  }
  if (api_model && api_model.trim()) {
    upsert.run('api_model', api_model.trim());
  }

  res.cookie('flash_success', 'Settings saved successfully.');
  res.redirect('/admin/settings');
});

// POST /admin/settings/test — test API connection
router.post('/admin/settings/test', protect, authorize('admin'), async (req, res) => {
  const settings = db.getSettings();

  if (!settings.api_key) {
    return res.json({ success: false, error: 'No API key configured.' });
  }

  const result = await testConnection(settings.api_provider, settings.api_key, settings.api_model);
  res.json(result);
});

module.exports = router;
