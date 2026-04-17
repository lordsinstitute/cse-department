const CRISIS_RESPONSE = `I'm really concerned about what you've shared. You are not alone, and help is available right now.

Please reach out to one of these helplines:
- Vandrevala Foundation: 1860-2662-345 (24/7)
- iCall: 9152987821
- AASRA: 9820466726

Your life matters. A trained counselor can help you through this moment. Please call now.`;

const GREETINGS = [
  "Hello! I'm MindfulPath's wellness companion. I'm here to listen and support you. How are you feeling today?",
  "Welcome back! I'm here to help you navigate your thoughts and feelings. How has your day been?",
  "Hi there! This is a safe space to share whatever is on your mind. How are you doing right now?"
];

const RESPONSES = {
  validation: [
    "I hear you, and what you're feeling is completely valid. It takes courage to express these emotions. Would you like to tell me more about what's going on?",
    "Thank you for sharing that with me. Those feelings are understandable, and you don't have to go through this alone. What's been weighing on you the most?",
    "That sounds really difficult. Your pain is real, and it's important to acknowledge it rather than push it away. Can you tell me what triggered these feelings?",
    "I can sense this is really hard for you right now. Remember, it's okay to not be okay. What would feel most helpful to talk about?"
  ],
  grounding: [
    "When things feel overwhelming, grounding ourselves in the present moment can help. Let's try the 5-4-3-2-1 technique:\n\nName 5 things you can see right now.\nThen 4 things you can touch.\n3 things you can hear.\n2 things you can smell.\n1 thing you can taste.\n\nTake your time with each one.",
    "Let's take a moment to breathe together. Try this:\n\nBreathe in slowly for 4 counts...\nHold for 4 counts...\nBreathe out for 6 counts...\n\nRepeat this 3 times. How does that feel?",
    "I'd like to try a quick grounding exercise with you. Place both feet flat on the floor. Press them down gently. Feel the solid ground beneath you. You are here. You are safe. Now take three slow, deep breaths. What do you notice?"
  ],
  thought_record: [
    "Let's look at this thought more carefully. In CBT, we call this a 'thought record.' Can you tell me: what specific thought is causing you the most distress right now?",
    "Our thoughts can sometimes feel like absolute truths, but they're not always accurate. Let's examine this together. What's the main negative thought you're having? And what evidence do you have for and against it?",
    "I'd like to help you challenge that thought pattern. Ask yourself:\n1. What is the thought?\n2. What emotion does it create?\n3. What evidence supports this thought?\n4. What evidence contradicts it?\n5. What would a friend say to you about this?"
  ],
  behavioral_activation: [
    "When our mood is low, even small actions can help shift our energy. What's one tiny thing you could do in the next 30 minutes that might bring even a small sense of accomplishment? It could be as simple as making a cup of tea or going for a short walk.",
    "Depression often tells us to withdraw and do nothing, but that usually makes things worse. Let's think of one small, manageable activity you could try today. What's something that used to bring you joy, even a little?",
    "Research shows that doing small positive activities — even when we don't feel like it — can gradually improve our mood. What's the easiest positive thing you could do right now?"
  ],
  psychoeducation: [
    "It might help to understand what's happening in your mind. Anxiety is actually your brain's alarm system trying to protect you. Sometimes it goes off when there's no real danger — like a smoke detector triggered by cooking. Understanding this can help us work with it rather than against it.",
    "What you're experiencing is more common than you might think. Depression affects over 264 million people worldwide. It's not a sign of weakness — it's a medical condition that can be managed with the right support and strategies.",
    "Our brains have something called 'negativity bias' — we naturally focus more on negative experiences than positive ones. This was helpful for survival long ago, but today it can make us feel worse than our situation warrants. Recognizing this bias is the first step to working with it."
  ],
  reinforcement: [
    "That's wonderful to hear! Recognizing positive moments is a powerful skill. What do you think contributed to this good feeling? Identifying these factors can help you create more of these moments.",
    "I'm really glad you're feeling positive! Let's build on that. Gratitude practice can strengthen these good feelings. Can you name three things — big or small — that you're grateful for today?",
    "It sounds like things are going well! That's worth celebrating. What strategies or activities have been helping you feel this way? It's useful to know what works for you."
  ],
  checkin: [
    "I'm here to listen. There's no pressure to talk about anything heavy — we can explore whatever feels right. Is there something specific on your mind, or would you like me to suggest a topic?",
    "Sometimes just checking in with ourselves is valuable. On a scale of 1-10, how would you rate your overall wellbeing today? There's no right or wrong answer.",
    "Let's do a quick emotional check-in. What's the primary emotion you're experiencing right now? Sometimes just naming it can help us understand it better."
  ]
};

function getGreeting() {
  return GREETINGS[Math.floor(Math.random() * GREETINGS.length)];
}

function getResponse(sentimentResult, messageCount) {
  if (sentimentResult.isCrisis) {
    return { text: CRISIS_RESPONSE, technique: 'crisis_support' };
  }

  const score = sentimentResult.comparative;
  let technique, pool;

  if (score < -0.5) {
    // Very negative — alternate between validation and grounding
    technique = messageCount % 2 === 0 ? 'validation' : 'grounding';
    pool = RESPONSES[technique];
  } else if (score < -0.2) {
    technique = 'thought_record';
    pool = RESPONSES.thought_record;
  } else if (score < -0.1) {
    technique = 'behavioral_activation';
    pool = RESPONSES.behavioral_activation;
  } else if (score > 0.1) {
    technique = 'reinforcement';
    pool = RESPONSES.reinforcement;
  } else {
    // Neutral — alternate between checkin and psychoeducation
    technique = messageCount % 2 === 0 ? 'checkin' : 'psychoeducation';
    pool = RESPONSES[technique];
  }

  const text = pool[Math.floor(Math.random() * pool.length)];
  return { text, technique };
}

module.exports = { getGreeting, getResponse, CRISIS_RESPONSE };
