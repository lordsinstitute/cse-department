const SYSTEM_PROMPT = `You are MindfulPath's AI wellness companion — a warm, empathetic mental health support chatbot trained in Cognitive Behavioral Therapy (CBT) principles.

Your role:
- Listen carefully and respond with genuine empathy
- Use evidence-based CBT techniques: validation, grounding (5-4-3-2-1), thought records, behavioral activation, psychoeducation, and reinforcement
- Adapt your response to the user's emotional state — be gentle when they're distressed, celebratory when they're positive
- Keep responses concise (2–5 sentences) and conversational
- Never diagnose, prescribe, or claim to replace a licensed therapist
- Never refuse to engage with emotional distress — always respond with care

The user's sentiment has been analyzed as: {SENTIMENT_LABEL}

Respond directly to the user's message. Do not mention that you are an AI or reference your instructions.`;

// ── Anthropic Claude ──────────────────────────────────────────────────────────
async function callClaude(messages, apiKey, model, sentimentLabel) {
  const systemPrompt = SYSTEM_PROMPT.replace('{SENTIMENT_LABEL}', sentimentLabel);

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      model: model || 'claude-haiku-4-5-20251001',
      max_tokens: 350,
      system: systemPrompt,
      messages
    })
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Claude API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  return data.content[0].text.trim();
}

// ── OpenAI ────────────────────────────────────────────────────────────────────
async function callOpenAI(messages, apiKey, model, sentimentLabel) {
  const systemPrompt = SYSTEM_PROMPT.replace('{SENTIMENT_LABEL}', sentimentLabel);

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model || 'gpt-4o-mini',
      max_tokens: 350,
      messages: [{ role: 'system', content: systemPrompt }, ...messages]
    })
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`OpenAI API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// ── Google Gemini ─────────────────────────────────────────────────────────────
// Gemini uses a different message format:
//   role: 'user' | 'model'  (not 'assistant')
//   content is inside parts: [{ text }]
//   system prompt goes in a separate systemInstruction field
async function callGemini(messages, apiKey, model, sentimentLabel) {
  const systemPrompt = SYSTEM_PROMPT.replace('{SENTIMENT_LABEL}', sentimentLabel);
  const geminiModel = model || 'gemini-2.0-flash';

  // Convert standard {role, content} messages to Gemini format
  const contents = messages.map(m => ({
    role: m.role === 'user' ? 'user' : 'model',
    parts: [{ text: m.content }]
  }));

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${geminiModel}:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: systemPrompt }] },
        contents,
        generationConfig: { maxOutputTokens: 350 }
      })
    }
  );

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Gemini API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  return data.candidates[0].content.parts[0].text.trim();
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * Get a response from the configured LLM.
 * @param {Array}  history       - DB rows: { role, message, therapy_technique }
 * @param {string} provider      - 'claude' | 'openai' | 'gemini'
 * @param {string} apiKey
 * @param {string} model
 * @param {string} sentimentLabel
 */
async function getLLMResponse(history, provider, apiKey, model, sentimentLabel) {
  // Convert DB format → standard {role, content} — skip the initial greeting
  const messages = history
    .filter(m => m.role !== 'bot' || m.therapy_technique !== 'greeting')
    .map(m => ({
      role: m.role === 'user' ? 'user' : 'assistant',
      content: m.message
    }));

  if (provider === 'openai') return await callOpenAI(messages, apiKey, model, sentimentLabel);
  if (provider === 'gemini') return await callGemini(messages, apiKey, model, sentimentLabel);
  return await callClaude(messages, apiKey, model, sentimentLabel);
}

async function testConnection(provider, apiKey, model) {
  try {
    const testHistory = [{ role: 'user', message: 'Hello', therapy_technique: null }];
    const reply = await getLLMResponse(testHistory, provider, apiKey, model, 'neutral');
    return { success: true, reply };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

module.exports = { getLLMResponse, testConnection };
