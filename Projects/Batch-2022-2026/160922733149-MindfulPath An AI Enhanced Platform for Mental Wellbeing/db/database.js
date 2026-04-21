const Database = require('better-sqlite3');
const path = require('path');
const bcrypt = require('bcryptjs');

const dbPath = path.join(__dirname, '..', 'mindfulpath.db');
const db = new Database(dbPath);

// Configure
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    bio TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS therapists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    specialties TEXT NOT NULL,
    education TEXT NOT NULL,
    experience INTEGER NOT NULL,
    license TEXT NOT NULL,
    approach TEXT,
    session_price REAL NOT NULL,
    languages TEXT DEFAULT 'English',
    avg_rating REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    therapist_id INTEGER NOT NULL,
    session_date TEXT NOT NULL,
    session_time TEXT NOT NULL,
    duration INTEGER DEFAULT 60,
    type TEXT DEFAULT 'video',
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    price REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (therapist_id) REFERENCES therapists(id)
  );

  CREATE TABLE IF NOT EXISTS meditations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    duration INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS mood_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mood_score INTEGER NOT NULL,
    mood_label TEXT NOT NULL,
    journal_text TEXT,
    sentiment_score REAL,
    sentiment_label TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS chat_sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    ended_at TEXT,
    avg_sentiment REAL,
    message_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_session_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    sentiment_score REAL,
    sentiment_label TEXT,
    therapy_technique TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_session_id) REFERENCES chat_sessions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
  );
`);

// Seed data
function seedDatabase() {
  const existing = db.prepare('SELECT id FROM users WHERE email = ?').get('admin@mindfulpath.com');
  if (existing) return;

  const salt = bcrypt.genSaltSync(10);

  // Users
  const insertUser = db.prepare('INSERT INTO users (name, email, password, role, bio) VALUES (?, ?, ?, ?, ?)');
  const adminId = insertUser.run('Administrator', 'admin@mindfulpath.com', bcrypt.hashSync('admin123', salt), 'admin', 'System administrator').lastInsertRowid;
  const therapist1UserId = insertUser.run('Dr. Sarah Ahmed', 'dr.sarah@mindfulpath.com', bcrypt.hashSync('doctor123', salt), 'therapist', 'Licensed clinical psychologist specializing in depression and anxiety disorders.').lastInsertRowid;
  const therapist2UserId = insertUser.run('Dr. Omar Khan', 'dr.omar@mindfulpath.com', bcrypt.hashSync('doctor123', salt), 'therapist', 'Mindfulness-based stress reduction specialist with focus on holistic wellness.').lastInsertRowid;
  const patientId = insertUser.run('Asiya Ali', 'patient@mindfulpath.com', bcrypt.hashSync('patient123', salt), 'user', 'Seeking support for stress and anxiety management.').lastInsertRowid;

  // Therapist profiles
  const insertTherapist = db.prepare('INSERT INTO therapists (user_id, specialties, education, experience, license, approach, session_price, languages) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
  const t1Id = insertTherapist.run(therapist1UserId, JSON.stringify(['Depression', 'Anxiety', 'Trauma/PTSD', 'Self-Esteem']), 'PhD Clinical Psychology, Osmania University', 8, 'RCI-CL-2018-4521', 'I use Cognitive Behavioral Therapy (CBT) combined with mindfulness techniques to help clients identify and challenge negative thought patterns. My approach is warm, collaborative, and evidence-based.', 800, 'English, Hindi, Urdu').lastInsertRowid;
  const t2Id = insertTherapist.run(therapist2UserId, JSON.stringify(['Stress Management', 'Mindfulness', 'Grief', 'Career Counseling']), 'M.Phil Counseling Psychology, NIMHANS', 5, 'RCI-CL-2020-7832', 'I practice Acceptance and Commitment Therapy (ACT) and mindfulness-based approaches. I believe in helping clients build psychological flexibility and find meaning in their experiences.', 600, 'English, Hindi').lastInsertRowid;

  // Meditations
  const insertMed = db.prepare('INSERT INTO meditations (title, description, category, duration, content) VALUES (?, ?, ?, ?, ?)');

  const meditations = [
    ['Calm Breathing', 'A gentle breathing exercise to reduce stress and bring calm to your mind and body.', 'stress', 5,
      'Welcome to this calm breathing meditation.\n\nFind a comfortable position and gently close your eyes.\n\nTake a deep breath in through your nose... hold for a moment... and slowly exhale through your mouth.\n\nAs you breathe in, imagine drawing in calm, peaceful energy.\nAs you breathe out, release any tension you are holding.\n\nBreathe in... 1... 2... 3... 4...\nHold... 1... 2...\nBreathe out... 1... 2... 3... 4... 5... 6...\n\nContinue this pattern. With each breath, feel your body becoming more relaxed.\n\nNotice the rise and fall of your chest. Feel the air flowing in and out.\n\nIf your mind wanders, gently bring it back to your breath. No judgment.\n\nYou are safe. You are calm. You are present.\n\nTake three more deep breaths at your own pace.\n\nWhen you are ready, slowly open your eyes. Carry this calm with you.'],

    ['Anxiety Release', 'Let go of anxious thoughts with this guided visualization meditation.', 'anxiety', 10,
      'Welcome. This meditation will help you release anxiety.\n\nClose your eyes and take three slow, deep breaths.\n\nImagine yourself standing by a gentle stream. The water flows peacefully.\n\nNow, think of your anxious thoughts as leaves falling from a tree.\nWatch each leaf — each worry — land on the water.\nSee it float away downstream, carried by the gentle current.\n\nYou don\'t need to hold onto these thoughts.\nYou don\'t need to fight them.\nJust watch them float away.\n\nAnother thought comes? Place it on a leaf. Watch it drift away.\n\nNow bring your attention to your body.\nScan from your head down to your toes.\nWherever you feel tension, breathe into that spot.\nImagine warmth and relaxation spreading through that area.\n\nYou are not your anxiety. You are the observer, watching thoughts come and go.\n\nTake a few more moments in this peaceful place by the stream.\n\nWhen you are ready, slowly return to the present moment and open your eyes.'],

    ['Sleep Journey', 'A soothing bedtime meditation to help you drift into peaceful sleep.', 'sleep', 15,
      'Welcome to your sleep meditation.\n\nLie comfortably in bed. Let your body sink into the mattress.\n\nClose your eyes and take a slow, deep breath.\n\nImagine you are lying on a soft cloud, floating gently through a starlit sky.\nThe stars twinkle softly above you. The air is warm and still.\n\nWith each breath, you feel heavier... more relaxed... more at peace.\n\nRelax your forehead... your eyes... your jaw.\nLet your shoulders drop. Release your arms. Soften your hands.\nRelax your chest... your stomach... your hips.\nLet your legs become heavy. Release your feet.\n\nYou are floating... drifting... safe and warm.\n\nImagine a gentle, warm light surrounding you.\nThis light represents safety, comfort, and rest.\nLet it wrap around you like a soft blanket.\n\nThere is nothing you need to do right now.\nNowhere you need to be. No problems to solve.\nJust rest.\n\nLet your mind become quiet.\nLet sleep come naturally.\n\nGoodnight.'],

    ['Focus Booster', 'Sharpen your concentration and mental clarity with this focused attention meditation.', 'focus', 8,
      'Welcome to the focus booster meditation.\n\nSit comfortably with your back straight. Close your eyes.\n\nTake three deep breaths to settle in.\n\nNow, bring your attention to a single point — the sensation of air entering your nostrils.\n\nFocus entirely on this sensation. The coolness of air coming in. The warmth of air going out.\n\nWhen your mind wanders — and it will — simply notice where it went, and gently bring it back.\nNo frustration. No judgment. Just redirect.\n\nThis is the practice of focus. Like building a muscle, each return strengthens your concentration.\n\nNow expand your focus slightly. Notice sounds around you, but don\'t follow them.\nJust acknowledge them and return to your breath.\n\nYour mind is becoming clearer. Sharper. More present.\n\nVisualize your goal for today. See yourself accomplishing it with focus and clarity.\n\nTake a deep breath in... and out.\n\nWhen you are ready, open your eyes. Bring this focused energy into your next task.'],

    ['Gratitude Garden', 'Cultivate gratitude and positive emotions through this heartwarming meditation.', 'mindfulness', 7,
      'Welcome to the gratitude garden meditation.\n\nClose your eyes and take a few calming breaths.\n\nImagine yourself walking into a beautiful garden. Sunlight filters through the trees.\nFlowers bloom in every color. The air smells fresh and sweet.\n\nIn this garden, each flower represents something you are grateful for.\n\nLook around. Pick the first flower that catches your eye.\nWhat does it represent? A person? A moment? A simple pleasure?\nHold it gently and feel the warmth of gratitude in your heart.\n\nNow find another flower. What are you grateful for today?\nMaybe it is your health. Maybe a kind word someone said. Maybe a meal you enjoyed.\n\nPick a third flower. Something small that you often overlook.\nThe ability to see. Clean water. A warm bed.\n\nHold all three flowers close to your heart.\nFeel the gratitude expanding, filling your chest with warmth.\n\nThis garden is always here for you. You can visit anytime.\n\nTake a deep breath of gratitude... and slowly open your eyes.'],

    ['Body Scan for Depression', 'A gentle body scan to reconnect with your physical self during low mood.', 'depression', 12,
      'Welcome. This meditation is designed to help when your mood feels low.\n\nFind a comfortable position. You can lie down or sit — whatever feels right.\n\nTake a slow breath in... and out. No rush.\n\nWhen we feel depressed, we can become disconnected from our bodies.\nThis meditation gently helps you reconnect.\n\nBring your attention to the top of your head.\nNotice any sensations there. Tingling? Warmth? Heaviness? Nothing at all?\nWhatever you notice is okay.\n\nSlowly move your attention to your forehead... your eyes... your cheeks.\nNotice without judging. You are simply observing.\n\nMove to your jaw. Many of us hold tension here. See if you can soften it slightly.\n\nNow your neck... your shoulders.\nTake a breath and imagine sending warmth to your shoulders.\n\nMove down your arms... your hands... your fingertips.\n\nNotice your chest. Feel your heartbeat. It has been beating for you every moment of your life.\nTake a moment to appreciate that.\n\nMove to your stomach... your hips... your legs... your feet.\n\nYou have just traveled through your entire body with kindness and attention.\nThis is an act of self-care.\n\nRemember: you deserve compassion, especially on difficult days.\n\nTake three slow breaths... and gently return to the room.'],

    ['Stress Melt', 'Progressive muscle relaxation to physically release stress from your body.', 'stress', 10,
      'Welcome to the stress melt meditation.\n\nThis technique uses progressive muscle relaxation to release tension.\n\nSit or lie comfortably. Close your eyes.\n\nWe will tense and then relax different muscle groups.\n\nStart with your hands. Make tight fists. Squeeze for 5 seconds.\n5... 4... 3... 2... 1... Release. Feel the difference.\n\nNow your arms. Tense your biceps. Hold tightly.\n5... 4... 3... 2... 1... Release. Let them go completely.\n\nShrug your shoulders up to your ears. Hold.\n5... 4... 3... 2... 1... Drop them down. Feel the tension melting away.\n\nScrunch your face tightly — forehead, eyes, mouth. Hold.\n5... 4... 3... 2... 1... Release. Smooth out your face.\n\nTense your stomach muscles. Hold.\n5... 4... 3... 2... 1... Release.\n\nPress your legs together tightly. Hold.\n5... 4... 3... 2... 1... Release.\n\nCurl your toes. Hold.\n5... 4... 3... 2... 1... Release.\n\nNow notice your entire body. Heavy. Warm. Relaxed.\n\nThe stress is melting away with each breath.\n\nStay here as long as you need.'],

    ['Mindful Walking', 'Practice mindfulness during everyday movement with this walking meditation guide.', 'mindfulness', 10,
      'Welcome to the mindful walking meditation.\n\nYou can practice this indoors or outdoors.\n\nStand still for a moment. Feel the ground beneath your feet.\nNotice your weight distributed between both feet.\n\nNow begin to walk slowly — much slower than normal.\n\nAs you lift your right foot, notice the sensation.\nThe muscles in your leg engaging. The foot leaving the ground.\nMoving through the air. Placing down. Feeling the floor again.\n\nNow the left foot. Lift... move... place.\n\nYour entire attention is on the act of walking.\nSomething you do every day without thinking — now you are fully present in it.\n\nNotice the rhythm. Lift... move... place. Lift... move... place.\n\nIf your mind wanders to thoughts about the past or future,\ngently bring it back to your feet.\n\nFeel the texture of the ground. The temperature of the air on your skin.\n\nYou are here. You are now. You are walking.\n\nThis simple act of mindful attention can be practiced anytime — walking to work, in a hallway, in your home.\n\nContinue for a few more minutes, then gradually return to your normal pace.'],

    ['Anxiety Grounding', 'A 5-4-3-2-1 grounding technique to anchor yourself during anxious moments.', 'anxiety', 5,
      'Welcome. If you are feeling anxious right now, this exercise will help ground you.\n\nTake a slow, deep breath. You are safe in this moment.\n\nWe are going to use your five senses to bring you back to the present.\n\n5 THINGS YOU CAN SEE:\nLook around you. Name five things you can see.\nA wall. A window. Your hands. A light. A color.\nReally look at each one.\n\n4 THINGS YOU CAN TOUCH:\nReach out and touch four things.\nThe chair you sit on. Your clothing. The table. Your hair.\nNotice the texture, temperature, and weight.\n\n3 THINGS YOU CAN HEAR:\nListen carefully. What three sounds do you notice?\nTraffic outside? A fan humming? Your own breathing?\n\n2 THINGS YOU CAN SMELL:\nTake two slow breaths through your nose.\nWhat do you smell? The air? Food? Soap?\n\n1 THING YOU CAN TASTE:\nNotice what you taste right now. Even if it is just the inside of your mouth.\n\nYou have just used all five senses to anchor yourself to the present moment.\n\nAnxiety lives in the future — in "what ifs."\nBut right now, in this moment, you are okay.\n\nTake one more deep breath. You did great.'],

    ['Self-Compassion', 'Learn to treat yourself with the same kindness you would offer a good friend.', 'depression', 8,
      'Welcome to the self-compassion meditation.\n\nThis is especially helpful when you are being hard on yourself.\n\nClose your eyes. Place one hand on your heart.\n\nFeel the warmth of your hand. Feel your heartbeat.\n\nNow think of a close friend who is going through a difficult time.\nWhat would you say to them?\n\nYou might say: "I am here for you. You are not alone. This is hard, but you will get through it."\n\nNow — can you say those same words to yourself?\n\nPlace your hand on your heart and say silently:\n"This is a moment of suffering."\n"Suffering is a part of being human."\n"May I be kind to myself in this moment."\n"May I give myself the compassion I need."\n\nThese words are from Dr. Kristin Neff, a researcher on self-compassion.\n\nYou deserve the same kindness you give to others.\nYou are not weak for struggling. You are human.\n\nRepeat these phrases as many times as you need.\n\nWhen you are ready, take a deep breath and gently open your eyes.\n\nCarry this compassion with you today.']
  ];

  for (const m of meditations) {
    insertMed.run(...m);
  }

  // Mood entries for patient (last 5 days)
  const insertMood = db.prepare('INSERT INTO mood_entries (user_id, mood_score, mood_label, journal_text, sentiment_score, sentiment_label, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)');
  const now = new Date();
  const days = [
    [patientId, 2, 'sad', 'Had a rough day. Felt overwhelmed at work and could not focus.', -0.45, 'negative', new Date(now - 4 * 86400000).toISOString()],
    [patientId, 3, 'neutral', 'Today was okay. Nothing special happened but I managed to get through.', 0.05, 'neutral', new Date(now - 3 * 86400000).toISOString()],
    [patientId, 2, 'sad', 'Anxiety kept me up last night. Feeling tired and low.', -0.52, 'negative', new Date(now - 2 * 86400000).toISOString()],
    [patientId, 4, 'happy', 'Tried the breathing meditation today. Actually felt better afterward!', 0.35, 'positive', new Date(now - 1 * 86400000).toISOString()],
    [patientId, 3, 'neutral', 'Mixed feelings today. Glad I am using this app to track my moods.', 0.08, 'neutral', now.toISOString()]
  ];
  for (const d of days) {
    insertMood.run(...d);
  }

  // Sessions
  const insertSession = db.prepare('INSERT INTO sessions (user_id, therapist_id, session_date, session_time, duration, type, status, notes, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
  const tomorrow = new Date(now.getTime() + 86400000);
  const tomorrowStr = tomorrow.toISOString().split('T')[0];
  const lastWeek = new Date(now.getTime() - 7 * 86400000);
  const lastWeekStr = lastWeek.toISOString().split('T')[0];
  insertSession.run(patientId, t1Id, tomorrowStr, '10:00', 60, 'video', 'scheduled', 'First consultation for anxiety management', 800);
  insertSession.run(patientId, t2Id, lastWeekStr, '14:00', 45, 'audio', 'completed', 'Introductory session — discussed stress management goals', 600);

  console.log('Database seeded with sample data.');
}

seedDatabase();

// Seed default app settings (idempotent)
const insertSetting = db.prepare('INSERT OR IGNORE INTO app_settings (key, value) VALUES (?, ?)');
insertSetting.run('nlp_mode', 'local');
insertSetting.run('api_provider', 'claude');
insertSetting.run('api_key', '');
insertSetting.run('api_model', 'claude-haiku-4-5-20251001');

// Helper to get all settings as a plain object
function getSettings() {
  const rows = db.prepare('SELECT key, value FROM app_settings').all();
  return Object.fromEntries(rows.map(r => [r.key, r.value]));
}

module.exports = db;
module.exports.getSettings = getSettings;
