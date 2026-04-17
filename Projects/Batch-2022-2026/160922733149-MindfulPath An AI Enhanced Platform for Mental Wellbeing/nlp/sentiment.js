const CRISIS_KEYWORDS = [
  'suicide', 'suicidal', 'kill myself', 'end it all', 'ending it all',
  'end my life', 'want to die', 'wanna die', 'no point in living',
  'better off dead', 'self harm', 'self-harm', 'cut myself',
  'hurt myself', 'hopeless', 'no reason to live', 'don\'t want to live'
];

// Lazy-loaded pipeline — initialized once on first use
let classifier = null;

async function getClassifier() {
  if (!classifier) {
    console.log('[MindfulPath] Loading sentiment model (first run may take a moment)...');
    const { pipeline } = await import('@xenova/transformers');
    classifier = await pipeline(
      'sentiment-analysis',
      'Xenova/distilbert-base-uncased-finetuned-sst-2-english'
    );
    console.log('[MindfulPath] Sentiment model ready.');
  }
  return classifier;
}

// Pre-warm the model at startup
getClassifier().catch(err => console.error('[MindfulPath] Model load error:', err));

async function analyzeSentiment(text) {
  const lowerText = text.toLowerCase();
  const isCrisis = CRISIS_KEYWORDS.some(kw => lowerText.includes(kw));

  const clf = await getClassifier();
  const result = await clf(text, { topk: 2 });

  // result = [{ label: 'POSITIVE', score: 0.98 }, { label: 'NEGATIVE', score: 0.02 }]
  const pos = result.find(r => r.label === 'POSITIVE');
  const neg = result.find(r => r.label === 'NEGATIVE');

  const posScore = pos ? pos.score : 0;
  const negScore = neg ? neg.score : 0;

  // Map confidence scores to comparative values matching existing response thresholds:
  // < -0.5 → very negative (validation/grounding)
  // < -0.2 → thought_record
  // < -0.1 → behavioral_activation
  // > 0.1  → reinforcement (positive)
  // else   → neutral (checkin/psychoeducation)
  let comparative;
  let label;

  if (negScore >= 0.85) {
    comparative = -0.6;
    label = 'very_negative';
  } else if (negScore >= 0.65) {
    comparative = -0.3;
    label = 'negative';
  } else if (negScore > 0.5) {
    comparative = -0.15;
    label = 'mildly_negative';
  } else if (posScore >= 0.6) {
    comparative = 0.3;
    label = 'positive';
  } else {
    comparative = 0;
    label = 'neutral';
  }

  return {
    comparative,
    label,
    isCrisis,
    raw: { positive: posScore, negative: negScore }
  };
}

module.exports = { analyzeSentiment };
